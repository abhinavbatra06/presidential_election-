# Import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

# Load data
def load_data():
    # Presidential election data
    file_id = '142QETIzMmGo-DLlj4fcjZVXcd_QMLvf7'
    direct_url = f'https://drive.google.com/uc?id={file_id}'
    data = pd.read_csv(direct_url)

    # Electoral college weightage
    file_id = '1AcHgjAHhMqRyAB0pHkA9cD9lJm4TaixV'
    direct_url = f'https://drive.google.com/uc?id={file_id}'
    election_college_wt = pd.read_csv(direct_url)

    return data, election_college_wt

# Data preparation for presidential election results
def dataprep_presedential_election_results(input_df):
    data = input_df.copy()
    data_trimmed_v1 = data[['year', 'state', 'state_po', 'state_fips', 'party_simplified', 'candidatevotes', 'totalvotes']]
    data_trimmed_v1.loc[:, ['perc_voteshare']] = data_trimmed_v1['candidatevotes'] / data_trimmed_v1['totalvotes']
    data_f1 = data_trimmed_v1.loc[data_trimmed_v1['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])]
    data_s1 = data_f1.sort_values(by=['year', 'state', 'candidatevotes'], ascending=False)
    data_transform_v1 = data_s1.groupby(['year', 'state', 'state_po'], group_keys=False).apply(
        lambda x: pd.Series({
            'winner_party': x.iloc[0, 4],
            'losing_party': x.iloc[1, 4],
            'winning_party_candidatevotes': x.iloc[0, 5],
            'winning_party_percvoteshare': x.iloc[0, 7],
            'voteshare_perc_diff': x.iloc[0, 7] - x.iloc[1, 7]
        })
    ).reset_index()
    data_transform_v1['year'] = data_transform_v1['year'].astype('int')
    return data_transform_v1

# Data preparation for electoral college
def dataprep_electoral_college(df_input):
    election_college_wt = df_input.copy()
    election_college_tranform_1 = election_college_wt.melt(
        id_vars=['State'],
        value_vars=['1976', '1980', '1984', '1988', '1992', '1996', '2000', '2004', '2008', '2012', '2016', '2020', '2024'],
        var_name='year',
        value_name='no_of_seats'
    )
    election_college_tranform_1['State'] = election_college_tranform_1['State'].str.upper()
    election_college_tranform_1['year'] = election_college_tranform_1['year'].astype(int)
    election_college_tranform_1.rename(columns={'State': 'state'}, inplace=True)
    election_college_tranform_1['perc_ec_seats'] = election_college_tranform_1['no_of_seats'] / 538.0
    return election_college_tranform_1

# Add flip flag
def add_flipflag(df_input):
    data_transform_v2 = df_input.copy()
    data_transform_v3 = data_transform_v2.sort_values(by=['state', 'year'])
    data_transform_v3['prev_election_winner'] = data_transform_v3['winner_party'].shift(1)
    data_transform_v3['flip_flag'] = np.where(data_transform_v3['prev_election_winner'] == data_transform_v3['winner_party'], 0, 1)
    return data_transform_v3

# Feature engineering
def feature_engineering(df_input, from_year, min_no_of_seats):
    data_transform_v3 = df_input.copy()
    condition_set_1 = (data_transform_v3['year'] >= from_year) & (data_transform_v3['no_of_seats'] >= min_no_of_seats)
    data_transform_v4 = data_transform_v3[condition_set_1].groupby(['state']).agg({
        'voteshare_perc_diff': ['mean', 'std'],
        'perc_ec_seats': 'min',
        'flip_flag': 'sum'
    })
    data_transform_v4.columns = data_transform_v4.columns.droplevel(0)
    data_transform_v4.rename(columns={
        'mean': 'avg_voteshare_pct_diff',
        'std': 'std_voteshare_pct_diff',
        'sum': 'total_flips',
        'min': 'ec_pct_share'
    }, inplace=True)
    condition_set_2 = (data_transform_v4['total_flips'] >= 1)
    data_transform_v4 = data_transform_v4[condition_set_2].reset_index()
    scaler = MinMaxScaler()
    data_transform_v4[['norm_avg_voteshare_pct_diff', 'norm_std_voteshare_pct_diff', 'norm_ec_pct_share', 'norm_total_flips']] = (
        0.1 + scaler.fit_transform(data_transform_v4[['avg_voteshare_pct_diff', 'std_voteshare_pct_diff', 'ec_pct_share', 'total_flips']]))
    return data_transform_v4

# Calculate swing score
def calc_swing_score(data_transform_v4, norm_avg_voteshare_pct_diff_wt, norm_std_voteshare_pct_diff_wt, norm_ec_pct_share_wt, norm_total_flips_wt):
    data_transform_v4['swing_score'] = (
        (1 - data_transform_v4['norm_avg_voteshare_pct_diff']) * norm_avg_voteshare_pct_diff_wt +
        (1 - data_transform_v4['norm_std_voteshare_pct_diff']) * norm_std_voteshare_pct_diff_wt +
        data_transform_v4['norm_ec_pct_share'] * norm_ec_pct_share_wt +
        data_transform_v4['norm_total_flips'] * norm_total_flips_wt
    )
    return data_transform_v4

# Custom Swing Score Calculator

# Custom Swing Score Calculator
def swing_score_calculator(data_transform_v4, data_transform_v3):
    st.title("Swing Score Calculator for 2024")
    st.write("""
    This tool calculates the swing score for each state based on the following parameters:
    - **Average Vote Share Difference**: Measures the average margin of victory/defeat.
    - **Standard Deviation of Vote Share Difference**: Indicates the consistency of vote share difference.
    - **Electoral College Weight**: The state's share  in the Electoral College.
    - **Total Flips**: Counts how many times the state has flipped between parties.
    - **Flipped Last Time**: Indicates whether the state flipped in the previous election.
    """)

    # Text inputs for weights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_voteshare_wt = st.number_input("Avg Vote Share Diff Weight", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    with col2:
        std_voteshare_wt = st.number_input("Std Vote Share Diff Weight", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    with col3:
        ec_weight = st.number_input("Electoral College Weight", min_value=0.0, max_value=1.0, value=0.4, step=0.1)
    with col4:
        flips_wt = st.number_input("Total Flips Weight", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

    # Calculate the sum of weights
    total_weight = avg_voteshare_wt + std_voteshare_wt + ec_weight + flips_wt

    # Validate if weights sum to 1
    if not np.isclose(total_weight, 1.0, atol=1e-5):  # Allow for small floating-point errors
        st.error("⚠️ The weights must add up to 1. Please adjust the weights.")
    else:
        # Calculate swing score with updated weights
        data_transform_v4 = calc_swing_score(data_transform_v4, avg_voteshare_wt, std_voteshare_wt, ec_weight, flips_wt)

        # Add "Flipped Last Time" flag
        latest_year = data_transform_v3['year'].max()
        flipped_last_time = data_transform_v3[data_transform_v3['year'] == latest_year][['state', 'state_po', 'flip_flag']]
        flipped_last_time.rename(columns={'flip_flag': 'flipped_last_time'}, inplace=True)
        data_transform_v4 = pd.merge(data_transform_v4, flipped_last_time, on='state', how='left')

        # Display updated top swing states
        st.subheader("Top Swing States Based on Custom Weights")
        top_states = data_transform_v4.sort_values(by='swing_score', ascending=False).head(10)

        # Visualize swing scores on a US map
        st.subheader("Swing States on US Map")
        if not top_states.empty:
            fig = px.choropleth(top_states,
                                locations="state_po",  # Use state abbreviations (e.g., "FL", "TX")
                                locationmode="USA-states",  # Set to plot US states
                                color="swing_score",  # Color based on swing score
                                hover_name="state",  # Display full state name on hover
                                hover_data=["swing_score", "flipped_last_time"],  # Additional data to display
                                scope="usa",  # Limit map to USA
                                color_continuous_scale=px.colors.sequential.Plasma,  # Color scale
                                title="Top Swing States by Custom Swing Score")
            st.plotly_chart(fig)
        else:
            st.warning("No data available to display on the map.")

        # Display the top states in a table (without index)
        st.write("Top Swing States Table:")
        st.dataframe(top_states[['state', 'state_po', 'swing_score', 'flipped_last_time']], hide_index=True)


# Main function to run the Streamlit app
def main():
    # Load and preprocess data
    data, election_college_wt = load_data()
    data_transform_v1 = dataprep_presedential_election_results(data)
    election_college_tranform_1 = dataprep_electoral_college(election_college_wt)
    data_transform_v2 = pd.merge(data_transform_v1, election_college_tranform_1, on=['state', 'year'], how='inner')
    data_transform_v3 = add_flipflag(data_transform_v2)
    data_transform_v4 = feature_engineering(data_transform_v3, from_year=2004, min_no_of_seats=5)

    # Streamlit App Layout
    swing_score_calculator(data_transform_v4, data_transform_v3)

if __name__ == "__main__":
    main()
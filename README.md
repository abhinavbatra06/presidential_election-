# Overview
This project is focused on analyzing U.S. presidential elections to identify swing states, explore key demographic impacts. By examining historical voting patterns and integrating demographic data, the project aims to provide insights into factors influencing swing state behavior.

# Objectives

- Identify Swing States
  - Analyze historical voting data to classify states as swing states or non-swing states.
  - Define criteria for swing state identification based on election results across multiple terms.
- Demographic Impact Analysis
  - For selected swing states, identify key demographic factors (e.g. - urban vs rural).
  - Analyze how these demographics impact voting preferences and outcomes within swing states.

 
# Results 

Insight:
-  Swing states identified according to swing score are : ['FLORIDA', 'PENNSYLVANIA', 'OHIO', 'NORTH CAROLINA', 'IOWA', 'MICHIGAN', 'VIRGINIA', 'WISCONSIN', 'GEORGIA', 'ARIZONA']	
- The semi-urban vote acts as a critical swing demographic in battleground states. When Democrats lose the semi-urban vote, they are more likely to lose the state, as seen in 2016.
- Urban areas provide a strong base, and rural areas remain a challenge, but semi-urban areas are pivotal for tipping the balance.

Visualization:
- [Interactive swing score calculator](https://aizqnvqgc8sdtgpmdg22yv.streamlit.app/)
- [Rural vs Urban divide](https://drive.google.com/open?id=11Ek34wMYJop7fVSabn00TSn5zb7x_oi0&usp=drive_fs)
- [Swing states over the years](https://drive.google.com/open?id=1LnQBNN1BYKch0-UcHW7MFUq-tAgd7PqW&usp=drive_fs)


# Data Sources

- U.S. President 1976–2020
	- **Title:** U.S. President 1976–2020
	- **Author:** MIT Election Data and Science Lab
	- **Publisher:** Harvard Dataverse
	- **URL:** [https://doi.org/10.7910/DVN/42MVDX](https://doi.org/10.7910/DVN/42MVDX)
	- **Edition:** Version 8
	- **Year Published:** 2017
	- **Keywords:** Elections
	- **Description:** Comprehensive dataset containing U.S. presidential election data from 1976 to 2020, published by the MIT Election Data 	and Science Lab.


- County Presidential Election Returns 2000-2020
	- **Title:** County Presidential Election Returns 2000-2020
	- **Author:** MIT Election Data and Science Lab
	- **Publisher:** Harvard Dataverse
	- **URL:** [https://doi.org/10.7910/DVN/VOQCHQ](https://doi.org/10.7910/DVN/VOQCHQ)
	- **Edition:** Version 13
	- **Year Published:** 2018
	- **Description:** Dataset providing county-level U.S. presidential election returns for the years 2000 through 2020.

- Consumer Price Index (CPI) Data
	- **Title:** Consumer Price Index and Annual Percent Changes from 1913 to 2008
	- **Source:** US Inflation Calculator
	- **URL:** [https://www.usinflationcalculator.com/inflation/	consumer-price-index-and-annual-percent-changes-from-1913-to-2008/#google_vignette](https://www.usinflationcalculator.com/inflation/	consumer-price-index-and-annual-percent-changes-from-1913-to-2008/#google_vignette)
	- **Description:** Historical Consumer Price Index (CPI) data from 1913 to 2008, including annual percent changes.

 - U.S. Census Data (ACS 5-Year Estimates)
	- **Title:** American Community Survey (ACS) 5-Year Estimates API
	- **Source:** U.S. Census Bureau
	- **API Endpoint:** [https://api.census.gov/data/{year}/acs/acs5](https://api.census.gov/data/)
	- **Description:** Access to detailed economic collected by the American Community Survey for 	various years.
	- **Usage:** Queries were made to retrieve state and county-level data for demographic analysis.

# Methodology

- Calculate swing score for each US state
	- Logic used
   		- Average vote share difference = 20%
   		- Standard Deviation vote share = 20%
   		- Electoral seat share (40%)
   		- Flip frequency (20%)
     		- Sort in order of most recenty flipped (Recency Bias) 	
     	- Identify swing state using the above logic (Top swing score)  
- Demographic Analysis
  	- Overlay demographic data with voting trends.
- Tools used
	- Python (Pandas , Numpy , Matplotlib , Scipy , plotly)  


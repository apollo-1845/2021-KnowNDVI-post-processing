# Analysis
## *Our Aim*

> We are going to calculate plant health on Earth and compare it to factors from NASA datasets and datasets we create, like air pollution, population density, temperature, humidity, daylight time, cloud cover, longitude and latitude, to get an idea of how limiting factors work on a large scale. This could help farmers maximise production and help analyse the reasons for deforestation, and help people find the optimal areas and conditions to plant crops or carry out reforestation.

## Datasets used (from <https://search.earthdata.nasa.gov>)

| Dataset name in `data/datasets` | Dataset name on EarthData              | Use                                                                                    |
|---------------------------------|----------------------------------------|----------------------------------------------------------------------------------------|
| ndvi                            | ISLSCP_II_GIMMS_NDVI_973               | NDVIs used as fallback                                                                 |
| land_cover                      | ISLSCP_II_MODISLC_968                  | Getting land cover categories                                                          |
| population_density              | CIESIN_SEDAC_GPWv4_APDENS_WPP_2015_R11 | Human - Population Density                                                             |
| co2_emissions                   | ISLSCP_CO2_EMISSIONS_1021              | Human - Carbon Dioxide Emissions from Fossil Fuels, Cement, and Gas Flaring as of 1995 |
| historical_land_use             | ISLSCP_II_HLANDCOVER_967               | Human - Historical Land Use 1700-1900?                                                 |
| gdp                             | ISLSCP_II_GDP_974                      | Human - Gross Domestic Product as of 1990?                                             |
| precipitation                   | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean precipitation as of May 1961-90                                 |
| temperature                     | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean temperature as of May 1961-90                                   |
| radiation                       | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean radiation as of May 1961-90                                     |


## Notes

* Number of images to process:
  * Takes around 2.5 seconds to open (but not process) 100 photo pairs
  * We have 4146 photos
  * Therefore, opening all the images would take around 2 minutes
* Land/sea
  * Use location?
  * Then filter by colour?
# Installation
1. Clone the repository: `git clone https://github.com/apollo-1845/Team-2-post-processing.git`
2. Download the data files: https://we.tl/t-SQBfFJt4SP and put the vis and nir pictures into the vis and nir directories under `data/images`
3. Please add any PIP-installed libraries here with their use:

| Dependency | Use                                |
|------------|------------------------------------|
| numpy      | Image processing & analysis        |
| opencv     | Image processing                   |
| skyfield   | ISS Location                       |
| tensorflow | Land classification neural network |
| keras      | Land classification neural network |
| matplotlib | Plotting graphs of results         |

> One way to do this is to save the `out` folder's contents in `data/out` then run the following shell script at the root directory of the project:
> ```bash
  > cd ./data
  > cp ./out/*_nir.png ./images/nir
  > cp ./out/*_vis.png ./images/vis
  > rm -r ./out
  > ```

TODO: finish this

# Analysis
## *Our Aim*

> We are going to calculate plant health on Earth and compare it to factors from NASA datasets and datasets we create, like air pollution, population density, temperature, humidity, daylight time, cloud cover, longitude and latitude, to get an idea of how limiting factors work on a large scale. This could help farmers maximise production and help analyse the reasons for deforestation, and help people find the optimal areas and conditions to plant crops or carry out reforestation.

## Datasets used (from <https://search.earthdata.nasa.gov>)

| Dataset name in `data/datasets` | Dataset name on EarthData              | Use                                                                                    | Citation |
|---------------------------------|----------------------------------------|----------------------------------------------------------------------------------------|-----------|
| ndvi                            | ISLSCP_II_GIMMS_NDVI_973               | NDVIs used as fallback                                                                 | TUCKER, C. J., PINZON, J., & BROWN, M. (2010). ISLSCP II GIMMS Monthly NDVI, 1981-2002. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/973 |
| land_cover                      | ISLSCP_II_MODISLC_968                  | Getting land cover categories                                                          | FRIEDL, M. A., STRAHLER, A. H., & HODGES, J. (2010). ISLSCP II MODIS (Collection 4) IGBP Land Cover, 2000-2001. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/968 |
| population_density              | CIESIN_SEDAC_GPWv4_APDENS_WPP_2015_R11 | Human - Population Density                                                             | Center For International Earth Science Information Network-CIESIN-Columbia University. (2018). Gridded Population of the World, Version 4 (GPWv4): Population Density Adjusted to Match 2015 Revision UN WPP Country Totals, Revision 11 [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4F47M65 |
| co2_emissions                   | ISLSCP_CO2_EMISSIONS_1021              | Human - Carbon Dioxide Emissions from Fossil Fuels, Cement, and Gas Flaring as of 1995 | ANDRES, R. J., MARLAND, G., FUNG, I., MATTHEWS, E., & BRENKERT, A. L. (2011). ISLSCP II Carbon Dioxide Emissions from Fossil Fuels, Cement, and Gas Flaring. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/1021 |
| historical_land_use             | ISLSCP_II_HLANDCOVER_967               | Human - Historical Land Use 1700-1900?                                                 | GOLDEWIJK, K. K. (2010). ISLSCP II Historical Land Cover and Land Use, 1700-1990. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/967 |
| gdp                             | ISLSCP_II_GDP_974                      | Human - Gross Domestic Product as of 1990?                                             | YETMAN, G., GAFFIN, S., & BALK, D. (2010). ISLSCP II Global Gridded Gross Domestic Product (GDP), 1990. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/974 |
| precipitation                   | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean precipitation as of May 1961-90                                 | NEW, M., JONES, P. D., & HULME, M. (2011). ISLSCP II Climate Research Unit CRU05 Monthly Climate Data. ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/1015 |
| temperature                     | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean temperature as of May 1961-90                                   | *Please see above* |
| radiation                       | ISLSCP_CRU5_MONTHLY_MEAN_1015          | Natural - Monthly mean radiation as of May 1961-90                                     | *Please see above* |


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

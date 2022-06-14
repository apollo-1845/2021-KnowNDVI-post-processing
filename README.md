# Analysis
## *Our Aim*

> We are going to calculate plant health on Earth and compare it to factors from NASA datasets and datasets we create, like air pollution, population density, temperature, humidity, daylight time, cloud cover, longitude and latitude, to get an idea of how limiting factors work on a large scale. This could help farmers maximise production and help analyse the reasons for deforestation, and help people find the optimal areas and conditions to plant crops or carry out reforestation.

## Datasets used

| Dataset               | Use                           |
|-----------------------|-------------------------------|
| ISLSCP_II_MODISLC_968 | Getting land cover categories |

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
| keras      | Land classification neural network|

> One way to do this is to save the `out` folder's contents in `data/out` then run the following shell script at the root directory of the project:
> ```bash
  > cd ./data
  > cp ./out/*_nir.png ./images/nir
  > cp ./out/*_vis.png ./images/vis
  > rm -r ./out
  > ```

TODO: finish this

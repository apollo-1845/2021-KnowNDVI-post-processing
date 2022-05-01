import datasets.main as datasets
import datasets.auth # Authentication for NASA Earthdata datasets

auth.authenticate("urs.earthdata.nasa.gov")

dataset = datasets.Dataset("https://cmr.earthdata.nasa.gov/stac/ASF/", ["SENTINEL-1_INTERFEROGRAMS.v1"])

def print_img(img):
    img.show()
    print(img)

for feature in dataset.get_features([-122.4, 41.3, -122.1, 41.5], "2020-01-01/2020-12-31"):
    feature.process_asset("browse", print_img)

auth.remove()
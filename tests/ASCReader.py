#!/usr/bin/env python

from misc.dataset_reader import ASCReader


def run_test():
    landtype = ASCReader(
        "data/datasets/modis_landcover_class_qd.asc"
    )  # Legend: https://www.researchgate.net/profile/Annemarie_Schneider/publication/261707258/figure/download/fig3/AS:296638036889602@1447735427158/Early-result-from-MODIS-showing-the-global-map-of-land-cover-based-on-the-IGBP.png

    assert landtype.get(-89, -180) == 15
    assert landtype.get(90, -180) == 0
    assert landtype.get(90, 179) == 0
    assert landtype.get(-89, 179) == 15

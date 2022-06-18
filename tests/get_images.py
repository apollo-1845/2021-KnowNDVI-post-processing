from debug_funcs import get_datapoints

def run_test():
    print("Getting DPs")
    for id, dp in get_datapoints(2000, 4146, step=100):  # landtype=0 for sea
        print(id, dp.get_coordinates())
        print("Landtype", dp.get_landtype())
        img = dp.get_camera_data()
        img.display()
        ndvi = dp.get_ndvi()
        ndvi.contrast()
        ndvi.display()
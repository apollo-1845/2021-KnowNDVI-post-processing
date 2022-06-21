from debug_funcs import get_datapoints

def run_test():
    print("Getting DPs")
    for id, dp in get_datapoints(1865):
        if(dp.get_land_cover() != 0):
            # Not sea
            print(id, dp.get_coordinates())
            print("Landtype", dp.get_land_cover())
            img = dp.get_camera_data()
            img.display()
            ndvi = dp.get_ndvi()
            ndvi.contrast()
            ndvi.display()
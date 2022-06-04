# Apply filtering for clouds + sea

def run(data_points):
    """Filter images from data point iterator, creating discarding masks with np.nan"""
    for point in data_points:
        print(point)

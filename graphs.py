#!/usr/bin/env python

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from remove_overlapping_pictures import get_spherical_distance

from misc.serialise_data_points import deserialise_from_prompt, deserialise_from_file


def compare_old_and_new(data_points):
    # timestamps = [point.get_timestamp().get_raw() for point in data_points]
    latitudes = [point.get_coordinates()[0] for point in data_points]
    longitudes = [point.get_coordinates()[1] for point in data_points]

    data_points_full = deserialise_from_file(f"./intermediates/full_data.json")
    data_points_full = [point for point in data_points_full]

    # timestamps_full = [point.get_timestamp().get_raw() for point in data_points_full]
    latitudes_full = [point.get_coordinates()[0] for point in data_points_full]
    longitudes_full = [point.get_coordinates()[1] for point in data_points_full]

    # Show the picture of the Earth
    plt.imshow(plt.imread("data/other/world_map.png"), extent=[-180, 180, -90, 90])

    plt.scatter(
        longitudes_full, latitudes_full, c="blue", label="Data received from the ISS"
    )
    plt.scatter(
        longitudes,
        latitudes,
        c="orange",
        label="Pictures of land received from the ISS",
    )
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()


def overall_hist(values, labels, row_id):
    label = labels[row_id]
    values = filter_rows(values, [row_id]).flatten()
    # fig, ax = plt.subplots()  # Create a figure containing a single axes.

    plt.hist(values, bins=30)
    plt.ylabel("Relative frequency")
    plt.xlabel(label)

    # fig.legend(loc="upper left")
    # fig.show()


def mean_plot(values, labels, bins, x_id, y_id, label_on_right=False):
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures

    x_label = labels[x_id]
    y_label = labels[y_id]
    (x, y) = filter_rows(values, [x_id, y_id])
    min = np.min(x)
    max = np.max(x)

    arr_range = max - min

    bin_indices = np.digitize(
        x,
        np.linspace(
            min,
            # to avoid including the max
            max + np.abs(max) * (10 ** -6),
            bins + 1,
        ),
    )
    # move from (1 to n) to (0 to n - 1)
    bin_indices -= 1

    means = []
    standard_deviations = []
    midpoints = []
    for bin_index in range(bins):
        values = y[bin_indices == bin_index]
        if values.size != 0:
            midpoint = min + (bin_index + 0.5) / bins * arr_range
            midpoints.append(midpoint)
            means.append(np.mean(values))
            standard_deviations.append(np.std(values))

    plt.errorbar(midpoints, means, yerr=standard_deviations, c="blue", ecolor="silver")

    # linear regression
    x_reshaped = x.reshape((-1, 1))
    model = LinearRegression().fit(x_reshaped, y)
    coef = model.coef_
    intercept = model.intercept_

    x_regression = np.linspace(min, max, bins)
    y_regression = coef * x_regression + intercept
    plt.plot(x_regression, y_regression, c="green")

    # polynomial regression
    degree = 2
    # get the different degrees
    x_transformed = PolynomialFeatures(degree=degree, include_bias=False).fit_transform(
        x_reshaped
    )
    model = LinearRegression().fit(x_transformed, y)
    coef = model.coef_
    intercept = model.intercept_

    # substitute into the calculation
    x_regression_transformed = PolynomialFeatures(
        degree=degree, include_bias=False
    ).fit_transform(x_regression.reshape((-1, 1)))
    y_regression = np.sum(x_regression_transformed * coef, axis=1) + intercept

    plt.plot(x_regression, y_regression, c="orange")

    pmcc = np.corrcoef(x, y)[0, 1]
    print(f"Label: {x_label}, r={pmcc}, n={x.size}")
    if label_on_right:
        label_x = 0.7
    else:
        label_x = 0.1
    plt.text(
        label_x,
        0.9,
        f"r = {pmcc:.2f}",
        # horizontalalignment="center",
        # verticalalignment="center",
        transform=plt.gca().transAxes,
    )
    plt.ylabel(y_label)
    plt.xlabel(x_label)


def linear_plot(x, y, x_label, y_label):
    pmcc = np.corrcoef(x, y)[0, 1]

    plt.text(
        0.1,
        0.9,
        f"r = {pmcc:.2f}",
        horizontalalignment="center",
        verticalalignment="center",
        transform=plt.gca().transAxes,
    )

    plt.scatter(x, y)
    plt.ylabel(y_label)
    plt.xlabel(x_label)


def plot_3d(data, labels, rows, bins):
    ((x, y), values) = to_frequencies(filter_rows(data, rows), bins=bins)
    x_label = labels[rows[0]]
    y_label = labels[rows[1]]

    ax = plt.gca()

    ax.contour3D(x, y, values, 50)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel("Frequency")


def filter_rows(values, axes):
    out = values[axes, ...]
    # Remove all columns with at least one NaN value
    mask = ~np.isnan(out).any(axis=0)
    return out[:, mask]


def take_log(vals):
    out = []
    for val in vals:
        if val is None or val == 0:
            out.append(None)
        else:
            out.append(np.log(val))
    return out


def to_frequencies(values, bins):
    assert len(bins) == values.shape[0]

    bins = np.array(bins)
    min = np.min(values, axis=1)
    max = np.max(values, axis=1)

    arr_range = max - min

    bin_width = arr_range / bins

    frequencies = np.zeros(bins)
    for el in values.T:
        bin_index = np.floor((el - min) / arr_range * bins).astype(int)
        # avoid out of bounds with min or max
        bin_index = np.clip(bin_index, 0, bins - 1)
        # A tuple allows us to index the proper position
        frequencies[tuple(bin_index)] += 1

    argmax = np.unravel_index(np.argmax(frequencies, axis=None), frequencies.shape)

    # return the positions of the buckets and the frequencies
    bucket_points = [np.linspace(min[i], max[i], bin) for i, bin in enumerate(bins)]
    return (bucket_points, frequencies.T)

    # out = []
    # for index, el in np.ndenumerate(frequencies):
    #     middle_point = min + (index + 0.5) / bins * arr_range
    #     out.append([*middle_point, el])
    # return np.array(out).T


data_points = deserialise_from_prompt()


# expected_ndvi_values = [point.get_expected_ndvi() for point in data_points]
# population_densities = [point.get_population_density() for point in data_points]
# latitudes = [point.get_latitude() for point in data_points]
# co2_emissions = [point.get_co2_emissions() for point in data_points]
# historical_land_use = [point.get_historical_land_use() for point in data_points]
# gdp = [point.get_gdp() for point in data_points]
# precipitation = [point.get_precipitation() for point in data_points]
# temperature = [point.get_temperature() for point in data_points]
# radiation = [point.get_radiation() for point in data_points]

# data = np.array(
#     [
#         expected_ndvi_values,
#         take_log(population_densities),
#         latitudes,
#         take_log(co2_emissions),
#         take_log(gdp),
#         take_log(precipitation),
#         temperature,
#         radiation,
#         # historical_land_use,
#     ],
#     dtype=float,
# )

# labels = [
#     "Dataset NDVI value",  # 0
#     "ln(population density)",  # 1
#     "latitude",  # 2
#     "ln(CO2 emissions)",  # 3
#     "ln(GDP)",  # 4
#     "ln(Precipitation)",  # 5
#     "Temperature",  # 6
#     "Radiation",  # 7
#     # "Historical land use",  # 8
# ]

# # Histograms of each datapoint
# for i in range(0, len(data)):
#     plt.subplot(3, 3, i + 1)
#     overall_hist(data, labels, i)

# # plots of means and standard deviations
# fig = plt.figure()
# for i in range(1, len(data)):
#     plt.subplot(3, 3, i)
#     mean_plot(data, labels, 20, i, 0, label_on_right=(labels[i] == "Radiation"))

# fig.legend(
#     [
#         "Linear regression line",
#         "Polynomial regression line",
#         "Mean dependent variable",
#     ],
#     loc="upper center",
#     bbox_to_anchor=(0, 0.0, 1, 0.3),
# )

# # pairwise histograms
# plt.figure()
# for i in range(1, len(data)):
#     plt.subplot(3, 3, i, projection="3d")

#     plot_3d(
#         data,
#         labels,
#         [i, 0],
#         [30, 30],
#     )

# path of the ISS
plt.figure()
compare_old_and_new(data_points)

plt.show()

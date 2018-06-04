# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Brighton Ancelin
# Collaborators (discussion):
# Time:
# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS

import pylab
import numpy as np
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # MY_CODE
    return [pylab.polyfit(x, y, deg) for deg in degs]


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # MY_CODE
    return 1 - (np.sum((y - estimated) ** 2) / np.sum((y - np.mean(y)) ** 2))


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # MY_CODE
    for model in models:
        pylab.figure()
        e = np.polyval(model, x)
        pylab.plot(x, y, 'b.')
        pylab.plot(x, e, 'r-')
        pylab.xlim(np.min(x)-1, np.max(x)+1)
        pylab.ylim(np.min(y)-1, np.max(y)+1)
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (C)')
        deg = len(model) - 1
        pylab.title('R^2={}, Deg={}'.format(r_squared(y, e), deg) +
                (', SE/slope={}'.format(
                se_over_slope(x, y, e, model)) if 1 == deg else ''))
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # MY_CODE
    return np.array([np.mean([np.mean(climate.get_yearly_temp(city, year))
                              for city in multi_cities]) for year in years])


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # MY_CODE
    arr1 = np.array([np.mean(y[:(k+1)]) for k in range(window_length-1)])
    arr2 = np.zeros((len(y) - window_length + 1))
    sum = np.sum(y[:window_length])
    arr2[0] = sum / window_length
    for start in range(len(y) - window_length):
        sum -= y[start]
        sum += y[start + window_length]
        arr2[start+1] = sum / window_length
    return np.concatenate((arr1, arr2))


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # MY_CODE
    return np.sqrt(np.mean((y - estimated) ** 2))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    # MY_CODE
    # clim_arr = np.array([np.array([climate.get_yearly_temp(city, year)
    #         for city in multi_cities]) for year in years])
    # clim_arr = np.mean(clim_arr, axis=1)
    # clim_arr = np.std(clim_arr, axis=1)
    clim_arr = np.zeros(len(years))
    for i in range(len(years)):
        year = years[i]
        clim_dat = np.array([climate.get_yearly_temp(city, year) for city in
                           multi_cities])
        clim_dat = np.mean(clim_dat, axis=0)
        clim_dat = np.std(clim_dat)
        clim_arr[i] = clim_dat
    return clim_arr

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # MY_CODE
    for model in models:
        pylab.figure()
        e = np.polyval(model, x)
        pylab.plot(x, y, 'b.')
        pylab.plot(x, e, 'r-')
        pylab.xlim(np.min(x)-1, np.max(x)+1)
        pylab.ylim(np.min(y)-1, np.max(y)+1)
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (C)')
        deg = len(model) - 1
        pylab.title('RMSE={}, Deg={}'.format(rmse(y, e), deg))
        pylab.show()


# MY_CODE
# === BEGIN MY CUSTOM CODE
def gen_std_devs_BUT_BETTER(climate, multi_cities, years):
    """
    So I was looking at the way that gen_std_devs computes its values and it
    does it by averaging the temperature across all cities on a particular
    day, then finding the std dev for the population of all days in that year.

    So I was thinking, "Hey, extreme weather doesn't mean that one day the
    entire globe goes cold and the next day the entire globe gets hot. It
    means that in all local regions, the variance in temperature from day to
    day should go up. In other words, we should be looking at the std devs
    of daily temperatures by city, and then averaging those. The way
    implemented in the instructions' version of gen_std_devs is kinda shit.
    It averages away most of our extrema by looking at temperatures all over
    the globe, when we're looking for extrema in local regions of the globe."

    Returns 1-d array where each entry is the average std dev (done this new
    way) for a given year.
    :param climate:
    :param multi_cities:
    :param years:
    :return:
    """
    clim_arr = np.array([np.array([np.std(climate.get_yearly_temp(city, year))
            for city in multi_cities]) for year in years])
    clim_arr = np.mean(clim_arr, axis=1)
    return clim_arr



if __name__ == '__main__':


    # PART 4
    # MY_CODE
    climate = Climate('data.csv')
    x = np.array(TRAINING_INTERVAL[:])
    city = 'NEW YORK'
    assert city in CITIES, 'Unknown city'
    y = np.array([climate.get_daily_temp(city, 1, 10, year) for \
            year in x])
    model = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, model)

    y = np.array([np.mean(climate.get_yearly_temp(city, year)) for year in x])
    model = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, model)



    # Part B
    # MY_CODE
    y = gen_cities_avg(climate, CITIES, x)
    model = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, model)

    # Part C
    # MY_CODE
    y = moving_average(y, 5)
    model = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, model)

    # Part D.2
    # MY_CODE
    models = generate_models(x, y, [1, 2, 20])
    # evaluate_models_on_training(x, y, models)
    test_x = TESTING_INTERVAL[:]
    test_y = moving_average(gen_cities_avg(climate, CITIES, test_x), 5)
    # evaluate_models_on_testing(test_x, test_y, models)


    # Part E
    # MY_CODE
    stds = gen_std_devs(climate, CITIES, x)
    stds = moving_average(stds, 5)
    model = generate_models(x, stds, [1])
    # evaluate_models_on_training(x, stds, model)


    # FURTHER ATTEMPTS
    # MY_CODE
    pylab.plot(climate.get_yearly_temp('NEW YORK', x[0]), 'b-')
    pylab.plot(climate.get_yearly_temp('NEW YORK', x[-1]), 'r-')
    pylab.show()
    # IDK, doesn't seem like the whole extreme weather is backed by data.
    # Std dev in yearly temperatures are slowly decreasing as the earth
    # warms, not the other way around. At least according to my rudimentary
    # analysis.
    # MY_CODE
    stds = gen_std_devs_BUT_BETTER(climate, CITIES, x)
    stds_1 = gen_std_devs(climate, CITIES, x)
    if np.all(stds > stds_1):
        print('Wow, all std devs are larger when done my way')
    stds = moving_average(stds, 5)
    model = generate_models(x, stds, [1])
    evaluate_models_on_training(x, stds, model)
    test_stds = gen_std_devs_BUT_BETTER(climate, CITIES, test_x)
    test_stds = moving_average(test_stds, 5)
    evaluate_models_on_testing(test_x, test_stds, model)

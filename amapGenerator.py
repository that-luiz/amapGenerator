# -*- coding: utf-8 -*-

'''
Input: a map as a matrix of values (separated by semicolon)
Columns are longitudes
Lines are latitudes

Output: values as a AMAP file

TODO: also convert to IONEX file

EXAMPLE USAGE:

data = read_file(filename)
data = create_matrix(data)
data = sort_matrix(data)
write_amap(data)

'''

__version__ = '0.1.0'
__author__ = 'Luiz Felipe Schleder'

import datetime
import numpy as np


def read_file(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        return data


def create_matrix(data):
    return np.array([line.split(';') for line in data.split('\n')])


def sort_matrix(matrix):
    converted_to_180 = False
    for line in matrix :
        longitude = line[0]
        if longitude > 180:
            line[0] -= 360
            converted_to_180 = True

    matrix.sort()

    if converted_to_180:
        for line in matrix:
            longitude = line[0]
            if longitude < 0:
                line[0] += 360
    return matrix


def write_amap(matrix, lat_initial=0.0, long_initial=0.0, incr=0.5, header=True, header_date=None):

    if header_date is None:
        header_date = datetime.datetime.now()

    filename = "{0:0>2}".format(header_date.hour) + '_' + "{0:0>2}".format(header_date.minute) + '_' + \
               "{0:0>2}".format(header_date.month) + "{0:0>2}".format(header_date.day) + '_' + \
               "{0:0>2}".format(header_date.year) + '.amap'

    with open(filename, 'w') as f:
        if header:
            f.write('DATE/TIME: ' + "{0:0>2}".format(header_date.year) + 3 * ' ' + "{0:0>2}".format(header_date.month) \
                    + 3 * ' ' + "{0:0>2}".format(header_date.day) + 3 * ' ' + "{0:0>2}".format(header_date.hour) \
                    + 3 *' ' + "{0:0>2}".format(header_date.minute)+'\n')
            f.write('LONGITUDE / LATITUDE / TEC [x10^16/m^2] \n')

        latitude = lat_initial
        longitude = long_initial
        for row in matrix:
            col = matrix[:, matrix.index(row)]
            for value in col:
                if value == '-1.0000':
                    value = '999.000'
                longitude = "%.2f" % longitude  # sets precision and converts to string.
                latitude = "%.2f" % latitude
                f.write(longitude + 3 * ' ' +  latitude + 3 * ' ' + value + '\n')
                latitude = float(latitude) + incr
                longitude = float(longitude)
            longitude += incr
            latitude = lat_initial

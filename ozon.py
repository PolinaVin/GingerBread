#!/usr/bin/env python3

# pip install netCDF4
# pip install numpy
# pip install json
# pip install matplotlib

from netCDF4 import Dataset
import numpy as np
from numpy import ma
import json
import calendar
import matplotlib.pyplot as plt


'''<==========SET_DEF_VAL==========>'''

lat = 15.46
long = 47.55
city = 'Brasilia'

'''<==========CREATE_MASS==========>'''

max = np.zeros(13)
min = np.zeros(13)
mean = np.zeros(13)
month = []

'''<==========MAIN==========>'''


def ploting():
    fig = plt.figure()
    a1 = fig.add_subplot(111)
    plt.title(f'{city}')
    plt.ylabel('average concentration of ozone')
    a1.legend(['max'])
    a1.plot(max[1:13], color='r')
    a1.set_xticks(np.arange(12))
    a1.set_xticklabels(month[1:13], rotation=20)
    a1.plot(min[1:13], color='b')
    a1.plot(mean[1:13], color='orange')
    a1.legend(['max', ' min', 'mean'])
    plt.savefig('ozon.png')
    # plt.show()


def put_temp():
    max[0] = res_col.max()    # ALL
    min[0] = res_col.min()    # ALL
    mean[0] = res_col.mean()  # ALL
    i = 0
    while i < 12:
        k = 0
        while k < len(res_col):
            res_col.mask[k] = True
            t = k
            while t > 11:
                t -= 12
            if t == i:
                res_col.mask[k] = False
                if res_col[k] == 0:
                    res_col.mask[k] = True
            k += 1
        max[i + 1] = res_col.max()
        min[i + 1] = res_col.min()
        mean[i + 1] = res_col.mean()
        i += 1


def month_arr():
    for name in calendar.month_name:
        month.append(name)


def save_data(dictData):
    print(dictData)
    with open("ozon.json", "w", encoding="utf-8") as file:
        json.dump(dictData, file, indent=4, separators=(',', ': '))


def dict_data():
    dictData = {}
    dictData['city'] = f'{city}'
    dictData['coordinates'] = [lat, long]
    i = 1
    while i < len(month):
        dictData[month[i]] = ({'min': min[i], 'max': max[i], 'mean': mean[i]})
        i += 1
    dictData['all'] = ({'min': min[0], 'max': max[0], 'mean': mean[0]})
    save_data(dictData)


def f_read_val():
    global lat
    global long
    global city
    print(f'Default values:\nlat - {lat} : long - {long} : city - {city}\n')
    print(f'Enter the new values to change the coordinates and the city \n')
    while True:
        try:
            lat_tmp = float(input(f'Type LAT or press ENTER to skip: '))
        except ValueError:
            break
        if (lat_tmp < -90.) or (lat_tmp > 90.):
            break
        try:
            long_tmp = float(input(f'Type LAT or press ENTER to skip: '))
        except ValueError:
            break
        if (long_tmp < -179.5) or (long_tmp > 180.):
            break
        try:
            city_tmp = str(input(f'Type CITY or press ENTER to skip:'))
        except ValueError:
            break
        lat = lat_tmp
        long = long_tmp
        city = city_tmp
        break


def main():
    global res_col
    f_read_val()
    data = Dataset('MSR-2.nc')
    temp_col = data.variables['Average_O3_column']
    # temp_std = data.variables['Average_O3_std'] ### NOT USE ###
    res_col = temp_col[:, lat, long]
    put_temp()
    month_arr()
    dict_data()
    data.close()
    ploting()


main()


'''<==========UNUSED_BLOCK==========>'''

''' CHECK KEYS AND ITEMS
print(data.dimensions.keys())
print('\n')
print(data.variables.keys())
print('\n')
print(data.dimensions.items())
print('\n')
print(data.variables.items())
print('\n')
'''

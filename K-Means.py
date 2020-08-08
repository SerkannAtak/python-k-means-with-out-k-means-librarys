# Author: Serkan Atak
# Works on just numerical points
import random
import sys
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

print("Enter up to 8 clusters...")
quantity = int(input("Enter the cluster number: "))
rows = []
columns = []
selected = []
temp_array = []
clusters = []
chosen_numbers = []
numbers = []
a = []

loc = ('myfile.xlsx')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


for j in range(1, sheet.nrows):
    row = sheet.row_values(j, 0).copy()
    rows.append(row)

for m in range(sheet.ncols):
    column = sheet.col_values(m, 1).copy()
    columns.append(column)

#Chose random centroids by user input
def centroid_selection(quantity):
    numbers.clear()
    chosen_numbers.clear()
    selected.clear()
    temp_array.clear()


    for i in range(len(rows)):
        numbers.append(i)

    for j in range(quantity):
        r = random.choice(numbers)
        chosen_numbers.append(r)
        numbers.remove(r)

    for z in range(len(chosen_numbers)):
        selected.append(rows[chosen_numbers[z]])

    for c in range(len(numbers)):
        temp_array.append(rows[numbers[c]])

#optimum centroid points find
def optimum_centroid_choise():
    centroid_selection(quantity)

    first_calculate = np.array((first_calculation(selected, temp_array)))
    sec_calculate = np.array((second_calculation(first_calculate)))

    comparison = first_calculate == sec_calculate
    equal_arrays = comparison.all()

    while not equal_arrays:

        first_calculate = sec_calculate
        sec_calculate = np.array((second_calculation(first_calculate)))

        comparison = first_calculate == sec_calculate
        equal_arrays = comparison.all()

    global centroids
    centroids = first_calculate.copy()
    clustering(first_calculate)

#calculete with out the first chosen centroids
def first_calculation(selected, temp_array):
    total = 0
    totals_array = []
    temp_array = temp_array.copy()
    selected = selected.copy()
    diveders = []

    for n in range(quantity):
        diveders.append(2)

    #all Euclidean calculations
    for j in range(len(temp_array)):
        for i in range(len(chosen_numbers)):
            for k in range(len(temp_array[i])):
                a = pow(selected[i][k] - float(temp_array[j][k]), 2)
                total += a
            totals_array.append(sqrt(total))
            total = 0
        index = totals_array.index(min(totals_array))

        #calculate wining centroid with new point
        for l in range(sheet.ncols):
            temp = format(((selected[index][l] * (diveders[index] - 1)) + temp_array[j][l]) / diveders[index], '.3f') # işlem
            selected[index][l] = float(temp)
        diveders[index] += 1
        totals_array = []

    return selected
#calculate all points with centroids
def second_calculation(selected_):
    selected = selected_.copy()
    total = 0
    totals_array = []
    diveders = []
    rows = []
    for n in range(quantity):
        diveders.append(2)

    for j in range(1, sheet.nrows):
        row = sheet.row_values(j, 0).copy()
        rows.append(row)
    #all Euclidean calculations
    for j in range(len(rows)):
        for i in range(len(chosen_numbers)):
            for k in range(len(rows[i])):
                euclidean = pow(selected[i][k] - rows[j][k], 2)
                total += euclidean
            totals_array.append(sqrt(total))
            total = 0
        index = totals_array.index(min(totals_array))

        #calculate winning centroid with new point
        for l in range(sheet.ncols):
            temp = format(((selected[index][l] * (diveders[index] - 1)) + rows[j][l]) / diveders[index], '.3f')
            selected[index][l] = float(temp)

        diveders[index] += 1
        totals_array = []

    return selected
#Create clusters from optimum centroids
def clustering(winners):
    selected = winners.copy()
    total = 0
    totals_array = []
    diveders = []
    rows = []

    for n in range(quantity):
        diveders.append(2)

    for j in range(1, sheet.nrows):
        column = sheet.row_values(j, 0).copy()
        rows.append(column)
    for l in range(quantity):
        temp_cluster = []
        for j in range(len(rows)):
            for i in range(len(chosen_numbers)):
                for k in range(len(rows[i])):
                    euclidean = pow(selected[i][k] - rows[j][k], 2)
                    total += euclidean
                totals_array.append(sqrt(total))
                total = 0
            index = totals_array.index(min(totals_array))
            totals_array = []

            if index == l:
                temp_cluster.append(rows[j])
        clusters.append(temp_cluster)

optimum_centroid_choise()

colors = ['b','g','r','c','m','y','k','w']
colors2 = ['bo', 'go', 'ro', 'co', 'mo',"yo", 'ko', 'wo']

print("Lütfen 0 - " + str((sheet.ncols) - 1) + " aralığında giriniz.")
x_axis = int(input("x axis: "))
y_axis = int(input("y axis: "))
z_axis = int(input("z axis: "))
div = 50
#screen size
x_ = int(max(columns[x_axis]) + (max(columns[x_axis]) / div))
y_ = int(max(columns[y_axis]) + (max(columns[y_axis]) / div ))
xx_ = int(min(columns[x_axis]) - (min(columns[x_axis]) / div))
yy_ = int(min(columns[y_axis]) - (min(columns[y_axis]) / div))
centroid_size = 100


def twoD():
    plt.title("K- Means Kümeleme \n")
    for aa in range(len(clusters)):
        for aa2 in range(len(clusters[aa])):
            plt.scatter(clusters[aa][aa2][x_axis], clusters[aa][aa2][x_axis], c=colors[aa])
    for bb in range(quantity):
        plt.scatter(centroids[bb][x_axis], centroids[bb][x_axis], c=colors[bb], s=centroid_size,
                    edgecolors='k', marker="s")

    plt.axis([xx_, x_, yy_, y_])
    plt.show()
def threeD():
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    plt.title("K- Means Kümeleme \n")
    for a in range(len(clusters)):
        for a2 in range(len(clusters[a])):
            ax.scatter3D(clusters[a][a2][x_axis], clusters[a][a2][x_axis], clusters[a][a2][z_axis], color=colors[a]);

    for b in range(quantity):
        ax.scatter3D(centroids[b][x_axis], centroids[b][x_axis], centroids[b][z_axis], color=colors[b], marker="s",
                     s=centroid_size,
                     edgecolors='k');

    fig.show()
def screenWriter():
    print("Clusters :")
    print("")
    for clu in range(len(clusters)):
        print("Centroid " + str(clu) + ": " + str(selected[clu]))
        print("This centroids cluster :")
        print("There are " + str(len(clusters[clu])) + " points")
        cluu = 0
        while cluu < len(clusters[clu]):
            if cluu < len(clusters[clu]):
                sys.stdout.write(str(clusters[clu][cluu]) + " - ")
                cluu += 1
            if cluu % 3 == 0:
                print("")
        print("")
        print("")
twoD()
threeD()
screenWriter()
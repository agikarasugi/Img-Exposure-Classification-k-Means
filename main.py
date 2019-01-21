from PIL import Image, ImageStat
import sys
import os
import random
from datetime import datetime
import math
import shutil

avgBrightness = list()
filenameList = list()

def moveClustFiles(Clust):
    ### print(Clust)

    dest1 = os.getcwd() + '/_cluster1'
    dest2 = os.getcwd() + '/_cluster2'
    dest3 = os.getcwd() + '/_cluster3'

    for i in Clust[0]:
        shutil.move(filenameList[i], dest1)
    for i in Clust[1]:
        shutil.move(filenameList[i], dest2)
    for i in Clust[2]:
        shutil.move(filenameList[i], dest3)

    return

def FindNewCentroid(lst):
    sum = 0

    for i in range(len(lst)):
        sum = sum + avgBrightness[lst[i]]

    return sum / len(lst)

def KMeansNext(m1, m2, m3, Clust):
    # calculate distance to centroid from each data points
    distTo_m1 = list()
    distTo_m2 = list()
    distTo_m3 = list()

    for i in range(len(avgBrightness)):
        distTo_m1.append(math.sqrt((m1-avgBrightness[i])**2))
        distTo_m2.append(math.sqrt((m2-avgBrightness[i])**2))
        distTo_m3.append(math.sqrt((m3-avgBrightness[i])**2))

    # label data points into clusters
    clusters = [list(), list(), list()]

    for i in range(len(avgBrightness)):
        if distTo_m1[i] <= distTo_m2[i] and distTo_m1[i] <= distTo_m3[i]:
            clusters[0].append(i)
        elif distTo_m2[i] <= distTo_m1[i] and distTo_m2[i] <= distTo_m3[i]:
            clusters[1].append(i)
        elif distTo_m3[i] <= distTo_m2[i] and distTo_m3[i] <= distTo_m1[i]:
            clusters[2].append(i)

    # find new centroids
    m1 = FindNewCentroid(clusters[0])
    m2 = FindNewCentroid(clusters[1])
    m3 = FindNewCentroid(clusters[2])

    if(clusters == Clust):
        moveClustFiles(Clust)
        return
    else:
        KMeansNext(m1, m2, m3, clusters)

def main():
    # loop for every files in subfolder 'images'
    for filename in os.listdir(os.getcwd() + '/images'):
        if filename.endswith('.jpg'):
            # assign imagefile path into variable
            im_file = os.getcwd() + '/images/' + filename

            # save image file path in list
            filenameList.append(im_file)

            # open the image as grayscale and append avg pixel brightness to a list
            im = Image.open(im_file).convert('L')
            stat = ImageStat.Stat(im)
            avgBrightness.append(stat.mean[0])

    if len(filenameList) < 3:
        print('YOU MUST HAVE AT LEAST 3 IMAGES!')
        return

    k = 3
    random.seed(datetime.now())

    # # choose centroid randomly
    # centroids = random.sample(range(0, len(avgBrightness)), k)
    #
    # # assign the centroid values
    # m1 = avgBrightness[centroids[0]]
    # m2 = avgBrightness[centroids[1]]
    # m3 = avgBrightness[centroids[2]]

    # choose centroid by formula
    j = len(avgBrightness) // 3

    m1 = avgBrightness[j-1]
    m2 = avgBrightness[j*2-1]
    m3 = avgBrightness[j*3-1]

    ### print(m1, m2, m3, j)

    # calculate distance to centroid from each data points
    distTo_m1 = list()
    distTo_m2 = list()
    distTo_m3 = list()

    for i in range(len(avgBrightness)):
        distTo_m1.append(math.sqrt((m1-avgBrightness[i])**2))
        distTo_m2.append(math.sqrt((m2-avgBrightness[i])**2))
        distTo_m3.append(math.sqrt((m3-avgBrightness[i])**2))

    # label data points into clusters
    clusters = [list(), list(), list()]

    for i in range(len(avgBrightness)):
        if distTo_m1[i] <= distTo_m2[i] and distTo_m1[i] <= distTo_m3[i]:
            clusters[0].append(i)
        elif distTo_m2[i] <= distTo_m1[i] and distTo_m2[i] <= distTo_m3[i]:
            clusters[1].append(i)
        elif distTo_m3[i] <= distTo_m2[i] and distTo_m3[i] <= distTo_m1[i]:
            clusters[2].append(i)

    ###print(clusters)

    # find new centroids
    m1 = FindNewCentroid(clusters[0])
    m2 = FindNewCentroid(clusters[1])
    m3 = FindNewCentroid(clusters[2])

    ###print(m1, m2, m3)

    KMeansNext(m1, m2, m3, clusters)

if __name__ == '__main__':
    main()

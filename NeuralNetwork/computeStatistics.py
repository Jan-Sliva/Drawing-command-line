import matplotlib.pyplot as plt
import numpy as np
import os, io
import os.path as P
import random
import tensorflow as tf
from pathlib import Path
import csv
from generator import genBuilder
import matplotlib.pyplot as plt

def vecDist(a, b):
    return float(tf.reduce_sum(tf.square(a - b), -1))

FOLDER_MODEL = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\res\\model3.h5"
FOLDER_SYMBOLS = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\dataSet"
FOLDER_SAVE = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak"

BATCH_SIZE = 32
NUM = 3

model = tf.keras.models.load_model(FOLDER_MODEL)

folders = os.listdir(FOLDER_SYMBOLS)

# remove samples which wonť be used in the final product⌈
folders.remove("mute")
folders.remove("brightness")
folders.remove("volume")
folders.remove("wifi")


dict_symbols = {}

for fold in folders:
    dict_symbols[fold] = []
    for file in os.listdir(P.join(FOLDER_SYMBOLS, fold)):
        dict_symbols[fold].append(P.join(FOLDER_SYMBOLS, fold, file))

data = genBuilder.getAll(dict_symbols, BATCH_SIZE)

results = model.predict(data)

coding = {}

for fold in folders:
    coding[fold] = { "file" : [], "vector" : []}
    for i in range(len(results)):
        if data.labels[i] == fold:
            coding[fold]["file"].append(data.samples[i])
            coding[fold]["vector"].append(results[i])

middles = {}
middleFiles = {}

for fold in coding.keys():
    min_dist = 1000000000
    middle = None
    for i in range(len(coding[fold]["file"])):
        dist = 0
        for j in range(len(coding[fold]["vector"])):
            dist += vecDist(coding[fold]["vector"][i], coding[fold]["vector"][j])
        if dist < min_dist:
            min_dist = dist
            middle = coding[fold]["vector"][i]
            file_name = coding[fold]["file"][i]
    middles[fold] = middle
    middleFiles[fold] = file_name

print(middleFiles)

def getCategory(categories, vec):
    min_dist = 1000000000
    ret = None
    for cat in categories.keys():
        dist = vecDist(categories[cat], vec)
        if dist < min_dist:
            min_dist = dist
            ret = cat
    return ret, min_dist

corr = 0
count = 0

res = {}

corrDist = []
uncorrDist = []

for fold in coding.keys():
    res[fold] = {}
    for i in range(len(coding[fold]["vector"])):
        pred, dist = getCategory(middles, coding[fold]["vector"][i])
        count += 1
        if pred == fold:
            corr += 1
            corrDist.append(dist)
        else:
            uncorrDist.append(dist)
        if not pred in res[fold]:
            res[fold][pred] = 1
        else:
            res[fold][pred] += 1

corrDist = sorted(corrDist)
uncorrDist = sorted(uncorrDist)

# print(corrDist)
# print(uncorrDist)

ptrC = -1
ptrU = -1

retX = []
spravnost = []
vyj = []

while (ptrC < len(corrDist)-1) and (ptrU < len(uncorrDist)-1):
    if corrDist[ptrC + 1] < uncorrDist[ptrU + 1]:
        ptrC += 1
        retX.append(corrDist[ptrC])
    else:
        ptrU += 1
        retX.append(uncorrDist[ptrU])
    spravnost.append((ptrC + 1) / (ptrC + ptrU + 2))
    vyj.append((2 + ptrC + ptrU) / (len(corrDist) + len(uncorrDist)))

if ptrC == len(corrDist)-1:
    while ptrU < len(uncorrDist)-1:
        ptrU +=1
        retX.append(uncorrDist[ptrU])
        spravnost.append((ptrC + 1) / (ptrC + ptrU + 2))
        vyj.append((2 + ptrC + ptrU) / (len(corrDist) + len(uncorrDist)))

if ptrU == len(corrDist)-1:
    while ptrC < len(corrDist)-1:
        ptrC +=1
        retX.append(corrDist[ptrC])
        spravnost.append((ptrC + 1) / (ptrC + ptrU + 2))
        vyj.append((2 + ptrC + ptrU) / (len(corrDist) + len(uncorrDist)))

        


# plt.plot(retX, spravnost, "r", retX, vyj, "b")
# plt.ylabel("Správnost / Kolik procent předpoví")
# plt.show()

plt.plot(vyj, spravnost)
plt.xlabel("Jak velkou část vzorků předpoví")
plt.ylabel("Správnost")
plt.show()

print("accuracy: " + str(corr / count))
print("")

for fold in res.keys():
    print(fold + ":")
    for pred in res[fold]:
        print("    " +  pred + " " + str(res[fold][pred]))

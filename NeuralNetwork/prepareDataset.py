import os.path as P
import os, csv

FOLDER = "D:\\HASY"
LABELS_FOLDER = "D:\\HASY\\hasy-data-labels.csv"

DICT = {}

with open(LABELS_FOLDER, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    first = True
    for row in spamreader:
        if first:
            first = False
            continue
        if not row[2] in DICT.keys():
            DICT[row[2]] = [row[0]]
        else:
            DICT[row[2]].append(row[0])




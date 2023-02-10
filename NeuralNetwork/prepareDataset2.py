import os.path as P
import os, csv
import cv2
import numpy as np


DEST_FOLDER = "D:\\symbols-32x32\\data"
FOLDER = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\dataSet"
FOLDS = ["wifi", "skype", "fileExplorer", "texmaker", "oneNote", "brightness", "volume", "mute", "close", "settings", "chrome", "vscode"]

LABELS = "D:\\symbols-32x32\\labels.csv"
IT = 0

with open(LABELS, 'w', newline='') as file:
    writer = csv.writer(file)
     
    writer.writerow(["file", "label"])

    for fold in FOLDS:
        for i in range(50):
            path = P.join(FOLDER, fold, str(i) + ".png")
            img = cv2.imread(path)
            img = img[24:-24, 24:-24, :]
            img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_AREA)
            # for i in range(32):
            #     for j in range(32):
            #         s = sum(img[i, j, :])
            #         if (s > 3*240):
            #             img[i, j, :] = [255, 255, 255]
            #         elif (s > 0):
            #             img[i, j, :] = [0, 0, 0]
            path2 = P.join(DEST_FOLDER, str(IT) + ".png")
            cv2.imwrite(path2, img)
            writer.writerow([path2, fold])
            IT += 1



import imageio, random, math
import os.path as P
import numpy as np
import cv2

FOLDER = "C:\\Users\\honzi\\OneDrive\\Matfyz\\Zapoctak"
DATA_FOLDER = P.join(FOLDER, "tvoricDat", "dataSet")

img = cv2.imread(P.join(DATA_FOLDER, "volume", str(random.randint(0, 50 - 1)) + ".png"),\
    cv2.IMREAD_GRAYSCALE)

img = np.divide(img, 255)
img = np.reshape(img, (192, 192, 1))

print(img.shape)

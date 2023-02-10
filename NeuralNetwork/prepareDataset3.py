import os.path as P
import os, csv
import cv2
import numpy as np


DEST_FOLDER = "D:"
FOLDER = "D:\\HASY\\hasy-data\\v2-00213.png"

img = np.zeros((48, 48, 3), np.uint8)
img.fill(255)
img[8:-8, 8:-8, :] = cv2.imread(FOLDER)
img = cv2.resize(img, dsize=(192, 192), interpolation=cv2.INTER_CUBIC)
cv2.imwrite(P.join(DEST_FOLDER, "test.png"), img)


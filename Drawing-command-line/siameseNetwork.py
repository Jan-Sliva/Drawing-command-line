import math
import numpy as np
import cv2
from tensorflow import reduce_sum, square
from tensorflow.keras.models import load_model
import os.path as P

class siameseNetwork:

    @staticmethod
    def computeDist(a, b):
        return float(reduce_sum(square(a - b), -1))

    def __init__(self, weights_path, pictures, indeces):
        self.model = load_model(P.join("models", weights_path))
        self.pictures = pictures
        self.encodings = self.model.predict(np.array(self.pictures))
        self.indeces = indeces

    def predict(self, picture):
        picture = np.reshape(picture, (1, 32, 32, 1))
        vec = self.model.predict(picture)
        min_dist = 0.1
        ret = None

        for i in range(len(self.encodings)):
            dist = siameseNetwork.computeDist(vec, self.encodings[i])
            if dist < min_dist:
                min_dist = dist
                ret = i
        
        if ret != None:
            return self.indeces[ret]
        else:
            return None

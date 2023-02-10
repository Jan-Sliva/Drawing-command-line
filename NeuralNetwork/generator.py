import tensorflow
import tensorflow.keras.utils
import cv2, random, math
import os.path as P
import numpy as np



class genBuilder():

    def getTrainAndTest(foldersBoth, split, foldersTest, numEx, folder, batch_size):
        """
            split - how much examples from foldersBoth to train data
            numEx - how many examples in one folder

            value - train_dat, test_data
        """
        train_data = []
        test_data = []

        toTrain = int(split*numEx)

        for fold in foldersBoth:
            samples = []
            for i in range(numEx):
                samples.append((i, fold))
            random.shuffle(samples)
            train_data.extend(samples[0:toTrain])
            test_data.extend(samples[toTrain:])

        for fold in foldersTest:
            for i in range(numEx):
                test_data.append((i, fold))

        return generator(folder, train_data, batch_size, False), generator(folder, test_data, batch_size, True)

    def getAll(folders, numEx, folder, batch_size):
        data = []
        for fold in folders:
            for i in range(numEx):
                data.append((i, fold))
        return generator(folder, data, batch_size, True)



class generator(tensorflow.keras.utils.Sequence):
    
    def __init__(self, folder, samples, batch_size, test):
        self.folder = folder
        self.batch_size = batch_size
        self.samples = samples
        self.isTest = test
        random.shuffle(self.samples)

    def on_epoch_end(self):
        if not self.isTest:
            random.shuffle(self.samples)

    def __len__(self):
        return math.ceil(len(self.samples) / self.batch_size)

    def __getitem__(self, idx):
        batch = self.samples[idx * self.batch_size:(idx + 1) * self.batch_size]

        pictures = np.array(list(map(lambda x: self.getSample(x[1], x[0]), batch)))
        labels = np.array(list(map(lambda x: x[1], batch)))

        return pictures, labels

    def getSample(self, name, num):
        return self.readPicture(P.join(self.folder, name, str(num) + ".png"))

    def readPicture(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        img = np.reshape(img, (192, 192, 1))
        img = img.astype("float32") / 255
        return img

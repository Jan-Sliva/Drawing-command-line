import tensorflow
import tensorflow.keras.utils
import cv2, random, math
import os.path as P
import numpy as np

def lmap(*args):
    return list(map(*args))

class genBuilder():

    def getTrainValTest(train_data : dict, split, test_data, batch_size):
        """
            split - how much examples from foldersBoth to train data
            numEx - how many examples in one folder

            value - train_dat, test_data
        """
        training = {}
        validation = {}

        toTrain = math.floor(split*len(train_data))

        all_labels = list(train_data.keys())
        random.shuffle(all_labels)

        for lab in all_labels[:toTrain]:
            training[lab] = train_data[lab]

        for lab in all_labels[toTrain:]:
            validation[lab] = train_data[lab]

        return tripletGenerator(training, batch_size), tripletGenerator(validation, batch_size), singletGenerator(test_data, batch_size)

    def getAll(data, batch_size):
        return singletGenerator(data, batch_size)


class generator(tensorflow.keras.utils.Sequence):
    
    def readPicture(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img.shape == (192, 192):
            img = img[24:-24, 24:-24]
            img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_AREA)
        img = np.reshape(img, (32, 32, 1))
        img = img.astype("float32") / 255
        return img
 

class tripletGenerator(generator):

    def __init__(self, samples, batch_size):
        self.batch_size = batch_size
        self.samples = samples

        self.triplets = []
        for name1 in self.samples.keys():
            for name2 in self.samples.keys():
                if name1 != name2:
                    self.triplets.append((name1, name2))
        random.shuffle(self.triplets)

    def getRandomSample(self, name):
        index = random.randint(0, len(self.samples[name])-1)
        return self.readPicture(self.samples[name][index])

    def getTwoDistinctRandomSamples(self, name):
        ind1 = random.randint(0, len(self.samples[name])-1)
        ind2 = random.randint(0, len(self.samples[name])-2)
        
        if ind2 >= ind1:
            ind2 += 1
        
        return [self.readPicture(self.samples[name][ind1]), self.readPicture(self.samples[name][ind2])]

    def getTriplet(self, triplet):
        return self.getTwoDistinctRandomSamples(triplet[0]) + [self.getRandomSample(triplet[1])]

    def __getitem__(self, idx):
        batch = self.triplets[idx * self.batch_size:(idx + 1) * self.batch_size]
        tri = lmap(lambda x: self.getTriplet(x), batch)
        return [np.array(lmap(lambda x: x[0], tri)), np.array(lmap(lambda x: x[1], tri)), np.array(lmap(lambda x: x[2], tri))], None

    def __len__(self):
        return math.ceil(len(self.triplets) / self.batch_size)


class singletGenerator(generator):

    def __init__(self, samples, batch_size):
            self.batch_size = batch_size
            self.samples = []
            self.labels = []
            for key in samples.keys():
                for val in samples[key]:
                    self.samples.append(val)
                    self.labels.append(key)

    def __len__(self):
        return math.ceil(len(self.samples) / self.batch_size)

    def __getitem__(self, idx):
        batch_S = self.samples[idx * self.batch_size:(idx + 1) * self.batch_size]

        pictures = np.array(lmap(lambda x: self.readPicture(x), batch_S))
        labels = np.array(self.labels[idx * self.batch_size:(idx + 1) * self.batch_size])

        return pictures, labels


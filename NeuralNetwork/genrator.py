import tensorflow
import tensorflow.keras.utils
import cv2, random, math
import os.path as P
import numpy as np

class genrator(tensorflow.keras.utils.Sequence):


    def __init__(self, folder, numEx, batch_size, theMain, comparative = []):
        self.folder = folder
        self.numEx = numEx
        self.batch_size = batch_size

        self.examples = []

        for ex1 in theMain:
            for ex2 in theMain + comparative:
                self.examples.append((ex1, ex2))

        for ex in comparative:
            self.examples.append((ex, ex))

        totLen = len(comparative) + len(theMain) * (len(theMain) + len(comparative))
        self.diffWeight = (len(comparative) + len(theMain)) / totLen
        self.sameWeight = 1 - self.diffWeight

        random.shuffle(self.examples)

    def on_epoch_end(self):
        random.shuffle(self.examples)

    def __len__(self):
        return math.ceil(len(self.examples) / self.batch_size)

    def __getitem__(self, idx):
        batch = self.examples[idx * self.batch_size:(idx + 1) * self.batch_size]

        pictures = list(map(lambda x: self.getRandomCouple(x[0], x[1]), batch))

        ret =  [np.array(list(map(lambda x: x[0], pictures))),\
             np.array(list(map(lambda x: x[1], pictures)))],\
             np.array(list(map(lambda x: x[0] == x[1], batch))),\
             np.array(list(map(lambda x: x[2], pictures)))
        return ret

    def getRandomSample(self, name):
        return self.readPicture(P.join(self.folder, name, str(random.randint(0, self.numEx - 1)) + ".png"))

    def getRandomCouple(self, name1, name2):
        if name1 != name2:
            return self.getRandomSample(name1), self.getRandomSample(name2), self.diffWeight
        
        first = random.randint(0, self.numEx - 1)
        second = random.randint(0, self.numEx - 2)

        if second >= first:
            second += 1
        
        return self.readPicture(P.join(self.folder, name1, str(first) + ".png")), \
                self.readPicture(P.join(self.folder, name1, str(second) + ".png")), self.sameWeight

    def readPicture(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        img = np.reshape(img, (192, 192, 1))
        img = img.astype("float32") / 255
        return img
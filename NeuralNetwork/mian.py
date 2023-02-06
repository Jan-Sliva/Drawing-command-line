import sismese
import imageio
import random
import os.path as P
from genrator import genrator
from sismese import sismese
import tensorflow as tf

def backup_history(history, output_path):
    with open(output_path, "w") as fw:
        # Write the header
        header = "epoch" + "\t" + "\t".join(history.keys()) + "\n"
        fw.write(header)
        # Write data rows
        zipped_data = list(zip(*history.values()))
        for i in range(0, len(history["loss"])):
            line = str(i+1) + "\t" + "\t".join(map(str, zipped_data[i])) + "\n"
            fw.write(line)


FOLDER = "C:\\Users\\honzi\\OneDrive\\Matfyz\\Zapoctak"
DATA_FOLDER = P.join(FOLDER, "tvoricDat", "dataSet")
NUM_EX = 50

BATCH_SIZE = 16

TRAIN = ["chrome", "vscode", "fileExplorer", "texmaker", "oneNote", "brightness", "volume", "mute", "close", "settings"]
TEST = ["wifi", "skype"]
SHAPE = (192, 192, 1)


trainSet = genrator(DATA_FOLDER, NUM_EX, BATCH_SIZE, TRAIN)
testSet = genrator(DATA_FOLDER, NUM_EX, BATCH_SIZE, TEST, TRAIN)

sis = sismese(SHAPE)
nn = sis.forward()

# nn.summary()
nn.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=[tf.keras.metrics.BinaryIoU(),
                       tf.keras.metrics.BinaryAccuracy()])

NUM = str(2)

hist = nn.fit(x = trainSet, validation_data = testSet, epochs = 100)
nn.save(P.join(FOLDER, "models", "model" + NUM + ".h5"))

backup_history(hist.history, P.join(FOLDER, "models", "hist" + NUM + ".tsv"))


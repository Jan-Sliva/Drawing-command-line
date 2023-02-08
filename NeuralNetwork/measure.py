import io
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow_datasets as tfds
from generator import generator, genBuilder
import os.path as P

NUM = 2

FOLDER = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak"
DATA_FOLDER = P.join(FOLDER, "dataSet")
NUM_EX = 50

BATCH_SIZE = 32

TRAIN = ["wifi", "skype", "fileExplorer", "texmaker", "oneNote", "brightness", "volume", "mute", "close", "settings"]
TEST = ["chrome", "vscode"]
ALL = TRAIN + TEST

model = tf.keras.models.load_model(P.join(FOLDER, "res", "model" + str(NUM) + ".h5"))
data = genBuilder.getAll(ALL, NUM_EX, DATA_FOLDER, BATCH_SIZE)

results = model.predict(data)

# Save test embeddings for visualization in projector
np.savetxt(P.join(FOLDER, "res", "vecs" + str(NUM) + "-all.tsv"), results, delimiter='\t')

out_m = io.open(P.join(FOLDER, "res", 'meta' + str(NUM) + '-all.tsv'), 'w', encoding='utf-8')
for img, labels in list(data):
    [out_m.write(str(ALL.index(x)) + "\n") for x in labels]
out_m.close()


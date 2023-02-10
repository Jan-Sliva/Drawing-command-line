import matplotlib.pyplot as plt
import numpy as np
import os, io
import os.path as P
import random
import tensorflow as tf
from pathlib import Path
import csv
from genResnet import genBuilder


FOLDER_MODEL = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\res\\model3.h5"
FOLDER_SYMBOLS = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\dataSet"
FOLDER_SAVE = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak"

BATCH_SIZE = 32
NUM = 3

model = tf.keras.models.load_model(FOLDER_MODEL)

folders = os.listdir(FOLDER_SYMBOLS)
dict_symbols = {}

for fold in folders:
    dict_symbols[fold] = []
    for file in os.listdir(P.join(FOLDER_SYMBOLS, fold)):
        dict_symbols[fold].append(P.join(FOLDER_SYMBOLS, fold, file))

data = genBuilder.getAll(dict_symbols, BATCH_SIZE)

results = model.predict(data)

# Save test embeddings for visualization in projector
np.savetxt(P.join(FOLDER_SAVE, "res", "vecs" + str(NUM) + "-all.tsv"), results, delimiter='\t')

out_m = io.open(P.join(FOLDER_SAVE, "res", 'meta' + str(NUM) + '-all.tsv'), 'w', encoding='utf-8')
for img, labels in list(data):
    [out_m.write(x + "\n") for x in labels]
out_m.close()


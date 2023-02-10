import matplotlib.pyplot as plt
import numpy as np
import os, io
import os.path as P
import random
import tensorflow as tf
from pathlib import Path
import csv
from tensorflow.keras import applications
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import metrics
from tensorflow.keras import Model

from resnet50 import DistanceLayer, SiameseModel
from genResnet import genBuilder

NUM = 3
SHAPE = (32, 32, 1)
BATCH_SIZE = 32
EPOCHS = 10

FOLDER_SAVE = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak"

FOLDER_HASY = "D:\\HASY"
LABELS_FOLDER = "D:\\HASY\\hasy-data-labels.csv"

dict_hasy = {}

with open(LABELS_FOLDER, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    first = True
    for row in spamreader:
        if first:
            first = False
            continue
        if not row[2] in dict_hasy.keys():
            dict_hasy[row[2]] = [P.join(FOLDER_HASY, row[0])]
        else:
            dict_hasy[row[2]].append(P.join(FOLDER_HASY, row[0]))


FOLDER_SYMBOLS = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak\\dataSet"
folders = os.listdir(FOLDER_SYMBOLS)

dict_symbols = {}



for fold in folders:
    dict_symbols[fold] = []
    for file in os.listdir(P.join(FOLDER_SYMBOLS, fold)):
        dict_symbols[fold].append(P.join(FOLDER_SYMBOLS, fold, file))

train_data = {}
test_data = {}

symbols_labels = list(dict_symbols.keys())
random.shuffle(symbols_labels)

for lab in symbols_labels[:6]:
    test_data[lab] = dict_symbols[lab]

for lab in symbols_labels[6:]:
    train_data[lab] = dict_symbols[lab]

for lab in dict_hasy.keys():
    train_data[lab] = dict_hasy[lab]

train, val, test = genBuilder.getTrainValTest(train_data, 0.9, test_data, BATCH_SIZE)




inputs = layers.Input(SHAPE)

chain = inputs

chain = layers.Conv2D(64, (3,3), activation='relu', padding='same')(chain)
chain = layers.BatchNormalization()(chain)
chain = layers.MaxPooling2D(pool_size=(2, 2))(chain)

chain = layers.Conv2D(128, (3,3), activation='relu', padding='same')(chain)
chain = layers.BatchNormalization()(chain)
chain = layers.MaxPooling2D(pool_size=(2, 2))(chain)

chain = layers.Conv2D(256, (3,3), activation='relu', padding='same')(chain)
chain = layers.BatchNormalization()(chain)

chain = layers.Flatten()(chain)
chain = layers.Dense(32, activation="relu")(chain)

embedding = Model(inputs, chain, name="Embedding")



anchor_input = layers.Input(name="anchor", shape=SHAPE)
positive_input = layers.Input(name="positive", shape=SHAPE)
negative_input = layers.Input(name="negative", shape=SHAPE)

distances = DistanceLayer()(
    embedding(anchor_input),
    embedding(positive_input),
    embedding(negative_input),
)

siamese_network = Model(
    inputs=[anchor_input, positive_input, negative_input], outputs=distances
)

siamese_model = SiameseModel(siamese_network)
siamese_model.compile(optimizer=optimizers.Adam(0.0001))

from tensorflow.keras.callbacks import ReduceLROnPlateau
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
                              patience=3, verbose = 1)
hist = siamese_model.fit(train, epochs=EPOCHS, validation_data=val, callbacks = [reduce_lr])

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

results = embedding.predict(test)

# Save test embeddings for visualization in projector
np.savetxt(P.join(FOLDER_SAVE, "res", "vecs" + str(NUM) + ".tsv"), results, delimiter='\t')

out_m = io.open(P.join(FOLDER_SAVE, "res", 'meta' + str(NUM) + '.tsv'), 'w', encoding='utf-8')
for img, labels in list(test):
    [out_m.write(x + "\n") for x in labels]
out_m.close()

# siamese_model.save(P.join(FOLDER_SAVE, "res", "triplet-model" + str(NUM) + ".h5"))
embedding.save(P.join(FOLDER_SAVE, "res", "model" + str(NUM) + ".h5"))

backup_history(hist.history, P.join(FOLDER_SAVE, "res", "hist" + str(NUM) + ".tsv"))


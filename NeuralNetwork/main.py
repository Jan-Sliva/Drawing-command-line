import io
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow_datasets as tfds
from generator import generator, genBuilder
import os.path as P

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

NUM = 2

FOLDER = "E:\\honzi\\OneDrive\\Matfyz\\Zapoctak"
DATA_FOLDER = P.join(FOLDER, "dataSet")
NUM_EX = 50

BATCH_SIZE = 32
EPOCHS = 100

TRAIN = ["wifi", "skype", "fileExplorer", "texmaker", "oneNote", "brightness", "volume", "mute", "close", "settings"]
TEST = ["chrome", "vscode"]
SPLIT = 0.8

ALL = TRAIN + TEST

train_dataset, test_dataset = genBuilder.getTrainAndTest(TRAIN, SPLIT, TEST, NUM_EX, DATA_FOLDER, BATCH_SIZE)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(192, 192, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=2),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation=None), # No activation on final dense layer
    tf.keras.layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1)) # L2 normalize embeddings
])



# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tfa.losses.TripletSemiHardLoss())

# Train the network
hist = model.fit(
    train_dataset, validation_data = test_dataset,
    epochs=EPOCHS)

# Evaluate the network
results = model.predict(test_dataset)

# Save test embeddings for visualization in projector
np.savetxt(P.join(FOLDER, "res", "vecs" + str(NUM) + ".tsv"), results, delimiter='\t')

out_m = io.open(P.join(FOLDER, "res", 'meta' + str(NUM) + '.tsv'), 'w', encoding='utf-8')
for img, labels in list(test_dataset):
    [out_m.write(str(ALL.index(x)) + "\n") for x in labels]
out_m.close()

model.save(P.join(FOLDER, "res", "model" + str(NUM) + ".h5"))

backup_history(hist.history, P.join(FOLDER, "res", "hist" + str(NUM) + ".tsv"))


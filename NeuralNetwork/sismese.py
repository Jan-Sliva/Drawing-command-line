from keras.models import Model
from keras.layers import Input, concatenate
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import BatchNormalization, Flatten, Dense, Subtract

class sismese:

    def __init__(self, input_shape):
        self.input_shape = input_shape

    def forward_once(self):
        inputs = Input(self.input_shape)

        chain = inputs

        chain = Conv2D(64, (3,3), activation='relu', padding='same')(chain)
        chain = BatchNormalization()(chain)
        chain = MaxPooling2D(pool_size=(2, 2))(chain)

        chain = Conv2D(128, (3,3), activation='relu', padding='same')(chain)
        chain = BatchNormalization()(chain)
        chain = MaxPooling2D(pool_size=(2, 2))(chain)

        chain = Conv2D(256, (3,3), activation='relu', padding='same')(chain)
        chain = BatchNormalization()(chain)

        chain = Flatten()(chain)
        chain = Dense(32, activation="relu")(chain)

        return inputs, chain

    def forward(self):
        input1, output1 = self.forward_once()
        input2, output2 = self.forward_once()

        chain = Subtract()([output1, output2])
        chain = Dense(1, activation = "sigmoid")(chain)

        return Model(inputs = [input1, input2], outputs = [chain])
    

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D

import tensorflow as tf
import numpy as np
import keras as ks
from skimage.transform import resize


def load_classify_image(image, image_size):
    num_channels = 3
    images = []

    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = resize(image, (image_size, image_size))
    image = image * 255
    images.append(image)
    images = np.array(images, dtype=np.uint8)

    # The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
    x_input = images.reshape(1, image_size, image_size, num_channels)
    return x_input

def load_labels(filename):
  # print("Loaded labels: " + str(filename))
  return [line.rstrip() for line in tf.gfile.GFile(filename)]


class ImportGraph():
    def __init__(self, loc):
        self.loc = loc
        if ".h5" in str(loc):
            self.kerasmodel = ks.models.load_model(loc)

    def predict_by_cnn(self, data, probability, labels):
        number_of_labels = len(labels)

        try:
            if ".h5" in self.loc:
                predictions = self.kerasmodel.predict(data)[0]

            # sort predictions
            top_k = predictions.argsort()[-number_of_labels:][::-1]
            this_class = "na"
            this_score = 0
            human_strings = []
            scores = []
            
            # get results
            for node_id in top_k:
                human_strings.append(labels[node_id])
                scores.append(predictions[node_id])

            top_index = scores.index(max(scores))
            top_score = scores[top_index]
            
            if top_score >= probability:
                this_score = top_score
                this_class = human_strings[top_index]
            if top_score < probability:
                this_class = "unknown"

        except Exception as e:
            print(e)

        return this_class, this_score




# cnn
def createCNNModel(img_shape, n_classes, n_layers):
    # Initialize model
    model = Sequential()
    
    # Layer 1
    model.add(Conv2D(64, (5, 5), input_shape=img_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=2))
    
    # Layer 2
    model.add(Conv2D(64, (5, 5), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=2))
    
    # Layer 3♣
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=2))
    
    model.add(Flatten())
    model.add(Dense(n_layers))
    model.add(Activation('relu'))

    model.add(Dense(n_classes))
    model.add(Activation('softmax'))

    return model




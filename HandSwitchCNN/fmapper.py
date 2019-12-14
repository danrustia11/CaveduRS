from keras.optimizers import *
from keras.models import Model, Sequential
from keras.layers import *
from keras.activations import *
from keras.callbacks import *
import keras as ks
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers import GlobalAveragePooling2D, DepthwiseConv2D, Reshape 
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras import models

import numpy as np
import matplotlib.pyplot as plt
import cv2  
import image_classifiers as IC

def show_feature_maps(image, model, dirs):
    layer_outputs = [layer.output for layer in model.layers[:24]]
    activation_model = models.Model(inputs=model.input, outputs=layer_outputs) 

    activations = activation_model.predict(image)
    layer_names = []
    for layer in model.layers[:24]:
        layer_names.append(layer.name) # Names of the layers, so you can have them as part of your plot
        
    images_per_row = 8
    
    for layer_name, layer_activation in zip(layer_names, activations): # Displays the feature maps
        n_features = layer_activation.shape[-1] # Number of features in the feature map
        size = layer_activation.shape[1] #The feature map has shape (1, size, size, n_features).
        n_cols = n_features // images_per_row # Tiles the activation channels in this matrix
        display_grid = np.zeros((size * n_cols, images_per_row * size))
        for col in range(n_cols): # Tiles each filter into a big horizontal grid
            for row in range(images_per_row):
                channel_image = layer_activation[0,
                                                  :, :,
                                                  col * images_per_row + row]
                # print(channel_image)
                channel_image -= channel_image.mean() # Post-processes the feature to make it visually palatable
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size : (col + 1) * size, # Displays the grid
                              row * size : (row + 1) * size] = channel_image
        

        fname = dirs + "/" + layer_name + "_grid.jpg"
        cv2.imwrite(fname, display_grid)
        
        
        scale = 1. / size
        plt.figure(figsize=(scale * display_grid.shape[1],
                            scale * display_grid.shape[0]))
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(display_grid, aspect='auto', cmap='gray')
        
 

def show_feature_map_one(image, model, num, dirs):
    layer_outputs = [layer.output for layer in model.layers[:24]]
    activation_model = models.Model(inputs=model.input, outputs=layer_outputs) 

    activations = activation_model.predict(image)
    layer_names = []
    for layer in model.layers[:24]:
        layer_names.append(layer.name) # Names of the layers, so you can have them as part of your plot
        

    print(len(layer_names))
    for layer_name, layer_activation in zip(layer_names, activations): # Displays the feature maps
        n_features = layer_activation.shape[-1] # Number of features in the feature map
        size = layer_activation.shape[1] #The feature map has shape (1, size, size, n_features).
    
        channel_image = layer_activation[0,
                                         :, :,
                                         num]
        channel_image -= channel_image.mean() # Post-processes the feature to make it visually palatable
        channel_image /= channel_image.std()
        channel_image *= 64
        channel_image += 128
        channel_image = np.clip(channel_image, 0, 255).astype('uint8')
        
        fname = dirs + "/" + layer_name + ".jpg"
        save_image = cv2.resize(channel_image, (128, 128), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(fname, save_image)
        
        fname = dirs + "/" + layer_name + "_original.jpg"
        cv2.imwrite(fname, channel_image)
        
        plt.figure()
        # plt.figure(figsize=(scale * display_grid.shape[1],
        #                     scale * display_grid.shape[0]))
        plt.axis('off')  
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(channel_image,  cmap='gray')       
        
        


img_dir1 = "hand_samples/hand/"
filename1 = "2019_11_16 17_59_10.jpg"
img_filename1 = img_dir1 + filename1
insect1 = cv2.imread(img_filename1)
insect1 = cv2.cvtColor(insect1, cv2.COLOR_BGR2RGB)
insect1 = np.expand_dims(insect1,axis=0)

insect = cv2.imread(img_filename1)
insect = cv2.cvtColor(insect, cv2.COLOR_BGR2RGB)

img_shape = insect.shape






model = Sequential()

# Layer 1
model.add(Conv2D(64, (3, 3), input_shape=img_shape))
# model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=2))

# Layer 2
model.add(Conv2D(64, (3, 3), padding='same'))
# model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=2))

# Layer 3
model.add(Conv2D(128, (3, 3), padding='same'))
# model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=2))
    

print(model.summary())




dirs = "fmap_CNN/"
# show_feature_map_one(insect1, model, 2, dirs)
show_feature_maps(insect1, model, dirs)
# show_feature_maps(insect4, model2, dirs)








#####################################################
# Training program for CNN image classifiers        #
#####################################################


#
# Library and dependencies
#
import matplotlib.pyplot as plt
import keras
import dataset as dataset
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
import image_classifiers as IC



# 
# Arbitrary constants
#

# Define model name
model_name = "hand_cnn"

# Train directories
train_dir = "hand_samples"

# Train settings
batch_size = 16         # number of validation and training samples per step
step_per_epoch = 20     # number of training steps per epoch
epochs = 25           # number of epochs
save_every_epoch = 5  # saves model every epoch
target_size = 128       # resizes images to this size
number_of_layers = 128

# Model saving settings
EVERY_N_EPOCHS = 1
BEST_MODELS = 2
save_model_mode = BEST_MODELS






# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#######################################
# Below contains the training routine #
#######################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #


# Set seed to make reproducible training results
from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)

# Assigns model save directory
model_dir = "generated_models/"             # saves all model (.h5) files to this location
model_save_dir = model_dir + model_name     # saves model to the name assigned in train_path
savemodel_filename = model_save_dir + "/" + str(model_name)

# Scan folder and check number of classes
class_names = os.listdir(train_dir)
class_names = [f for f in class_names if ".jpg" not in f]
num_classes = len(class_names)

# Makes model save directory
try:
    os.mkdir(model_save_dir)
except:
    print("Directory exists!")
    pass

# Make labels .txt file 
label_filename = savemodel_filename + ".txt"
with open(label_filename, 'w') as txt_file:
    for x in range(0,len(class_names)):
        txt_file.write(class_names[x] + "\n")

# Separate training and validation set
data = dataset.read_train_sets(train_path=train_dir, 
                               class_names=class_names,
                               image_size=target_size,
                               validation_size=0.2)

# Prepare training and validation data
train_data = data.train.images.astype('float32')
valid_data = data.valid.images.astype('float32')
nRows,nCols,nDims = train_data.shape[1:]
input_shape = (nRows, nCols, nDims)
train_labels = data.train.labels
valid_labels = data.valid.labels
train_labels_one_hot = to_categorical(data.train.labels)
valid_labels_one_hot = to_categorical(data.valid.labels)













# Set image normalization
datagen = ImageDataGenerator(rescale=1./255)


# Create model and show its structure
# Refer to "image_classifiers.py" for changing the structures
model = IC.createCNNModel((target_size, target_size, 3), num_classes, number_of_layers)

# Compile model
optim = keras.optimizers.Adam(lr=0.00005)
model.compile(optimizer=optim, loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())



#
# Option 1:
# Saves model every 10 epochs
#

if save_model_mode == EVERY_N_EPOCHS:
    mc = keras.callbacks.ModelCheckpoint(str(savemodel_filename) + "_{epoch:d}.h5",
                                          save_weights_only=False, period=save_every_epoch)

# 
# Option 2:
# Save only the best models
# 
if save_model_mode == BEST_MODELS:
    mc = keras.callbacks.ModelCheckpoint(str(savemodel_filename) + "_{epoch:d}.h5",
                                          save_weights_only=False, 
                                          save_best_only=True,
                                          mode='auto')

# Start training
history = model.fit_generator(datagen.flow(train_data, train_labels_one_hot, batch_size=batch_size),
                                epochs=epochs,
                                steps_per_epoch=step_per_epoch,
                                validation_data=datagen.flow(valid_data, valid_labels_one_hot),
                                validation_steps=batch_size,
                                verbose=1,
                                callbacks=[mc])

# Save training summary to csv
import pandas as pd 
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))
summary_dict = {'Epoch': epochs, 'TrainAcc': acc, 'ValAcc': val_acc, 'TrainLoss': loss, 'ValLoss': val_loss}
df = pd.DataFrame(data=summary_dict)
df.to_csv(model_save_dir + "/" + model_name + ".csv")

# Plot accuracy curves
plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.interactive(False)
plt.show()







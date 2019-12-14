import cv2
import os
import numpy as np
from sklearn.utils import shuffle

class DataSet(object):
  def __init__(self, images, labels):
    self._num_examples = images.shape[0]

    self._images = images
    self._labels = labels
    self._epochs_done = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_done(self):
    return self._epochs_done

  def next_batch(self, batch_size):
    start = self._index_in_epoch
    self._index_in_epoch += batch_size

    if self._index_in_epoch > self._num_examples:
      self._epochs_done += 1
      start = 0
      self._index_in_epoch = batch_size
      assert batch_size <= self._num_examples
    end = self._index_in_epoch

    return self._images[start:end], self._labels[start:end]


def load_set(train_dir, image_size, classes):
    images = []
    labels = []

    print('Now reading samples...')
    images = []
    labels = []
    total_number_of_files = []
    for index, class_name  in enumerate(classes):

        target_folder = train_dir + "/" + class_name
        files = os.listdir(target_folder)
        
        # Check if it is a huge folder
        if len(files) > 0:
            maybe_dir = target_folder + "/" + files[0]
            if os.path.isdir(maybe_dir):
                files = []
                sub_dirs = os.listdir(target_folder)
                for sub_folder in sub_dirs:
                    sub_files = os.listdir(target_folder + "/" + sub_folder)
                    for file in sub_files:
                        files.append(target_folder + "/" + sub_folder + "/" + file)
            else:
                for i, file in enumerate(files):
                    files[i] = target_folder + "/" + file
            
        number_of_files = len(files)
        

        for file in files:
            original_image = cv2.imread(file)
            image = cv2.resize(original_image, (image_size, image_size),0,0, cv2.INTER_CUBIC)
            images.append(image)
            labels.append(index)
                  
        print('{} ({}), #: {})'.format(class_name, str(index), number_of_files))   
        total_number_of_files.append(labels.count(index))
              
    images = np.array(images)
    labels = np.array(labels)
    return images, labels, total_number_of_files






def read_train_sets(train_path, class_names, image_size, validation_size):
  class DataSets(object):
    pass

  data_sets = DataSets()
  images, labels, number_of_files = load_set(train_path, image_size, class_names)
  images, labels = shuffle(images, labels)


  if isinstance(validation_size, float):
    validation_size = int(validation_size * images.shape[0])


  validation_images = images[:validation_size]
  validation_labels = labels[:validation_size]
  train_images = images[validation_size:]
  train_labels = labels[validation_size:]
  data_sets.train = DataSet(train_images, train_labels)
  data_sets.valid = DataSet(validation_images, validation_labels)
  return data_sets



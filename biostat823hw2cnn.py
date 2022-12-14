# -*- coding: utf-8 -*-
"""BIOSTAT823HW2CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cdanV-ZOyrQqUbn2o3H9Gj-mjqt55mCq

# Read in Data
"""

from tensorflow import keras
import tensorflow as tf
import os, datetime
import tensorflow_datasets as tfds
from sklearn.metrics import classification_report
import numpy as np

from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Dense,
    Flatten,
    BatchNormalization,
    Dropout,
)
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import GaussianDropout


pcam, pcam_info = tfds.load("patch_camelyon", with_info=True, as_supervised=True)

train_data = pcam["train"]
valid_data = pcam["validation"]
test_data = pcam["test"]

"""# Pre-Processing"""

# This function will scale the images
def preprocess(image, labels):
    image = tf.cast(image, tf.float32)
    image /= 255.0
    return image, labels


# Using the map attribute of the data will allow us to scale the images using the preprocess function from above
train_data = train_data.map(preprocess)
valid_data = valid_data.map(preprocess)
test_data = test_data.map(preprocess)

# This will randomize the order of the training images
buffer_size = 1000
train_data = train_data.shuffle(buffer_size)

tr_len = len(train_data)
vd_len = len(valid_data)
ts_len = len(test_data)
print(tr_len, vd_len, ts_len)

# batch size refers to the number of images to be used in each epoch of the model
# the total size of train is 262,144 validation is 32,768 and test is 32,768
# thus a batch_size of 256 seems satisfactory.
batch_size = 256
train_data = train_data.batch(batch_size).prefetch(1)
valid_data = valid_data.batch(batch_size).prefetch(1)
test_data = test_data.batch(batch_size).prefetch(1)

# Seperating image and label into different variables
train_images, train_labels = next(iter(train_data))
valid_images, valid_labels = next(iter(valid_data))
test_images, test_labels = next(iter(test_data))

# Checking the label shape
valid_labels.shape

# Checking the shape of our tensor objects
train_images.shape

# Using the iter() function separates the image from the label

# the shape of each of our tensor objects is [256, 96, 96, 3]
# meaning there are 256 images, each with length and width of 96
# and a depth of 3 (rgb)

train_images.shape

"""# Model Building

## Architecture 1
"""

# Our input shape is [96,96,3]
# import the necessary libraries


model1 = Sequential(
    [
        Conv2D(
            256,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
            input_shape=[96, 96, 3],
        ),
        MaxPooling2D(2),
        Conv2D(
            256,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(2),
        Conv2D(
            512,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(2),
        Conv2D(
            512,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(2),
        Conv2D(
            1024,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(2),
        Conv2D(
            1024,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(2),
        Flatten(),
        Dense(1028, kernel_initializer="he_uniform", activation="relu"),
        Dense(512, kernel_initializer="he_uniform", activation="relu"),
        Dense(128, kernel_initializer="he_uniform", activation="relu"),
        Dense(1, activation="sigmoid"),
    ]
)

# Compiling our model
model1.compile(
    optimizer=optimizers.Adam(1e-4), loss="binary_crossentropy", metrics=["acc"]
)

# Callbacks
early_stopping_cb1 = keras.callbacks.EarlyStopping(monitor="val_loss", patience=7)

# , callbacks=[early_stopping_cb1]

# Fitting our model
history1 = model1.fit(
    train_data, epochs=100, steps_per_epoch=10, validation_data=valid_data, verbose=2
)


acc1 = history1.history["acc"]
val_acc1 = history1.history["val_acc"]
loss1 = history1.history["loss"]
val_loss1 = history1.history["val_loss"]
epochs1 = range(1, len(acc1) + 1)
plt.plot(epochs1, acc1, "bo", label="Training acc")
plt.plot(epochs1, val_acc1, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs1, loss1, "bo", label="Training loss")
plt.plot(epochs1, val_loss1, "r", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""## Architecture 2"""

# changes:
# the activation functions to hyperbolic tangent from relu
# kernel_initializer stayed as he_uniform because the activation function is tanh
# average pooling with stride of 2 instead of max pooling
# added dropout layers after each pooling with a percentage of .2
# removed two dense layers

model2 = Sequential(
    [
        Conv2D(
            256,
            3,
            kernel_initializer="he_uniform",
            activation="tanh",
            input_shape=[96, 96, 3],
        ),
        AveragePooling2D(strides=2),
        Dropout(0.2),
        Conv2D(
            256,
            3,
            kernel_initializer="he_uniform",
            activation="tanh",
        ),
        AveragePooling2D(strides=2),
        Dropout(0.2),
        Conv2D(
            512,
            3,
            kernel_initializer="he_uniform",
            activation="tanh",
        ),
        AveragePooling2D(strides=2),
        Dropout(0.2),
        Conv2D(
            512,
            3,
            kernel_initializer="he_uniform",
            activation="tanh",
        ),
        AveragePooling2D(strides=2),
        Dropout(0.2),
        Flatten(),
        Dense(1028, kernel_initializer="he_uniform", activation="tanh"),
        Dense(1, activation="sigmoid"),
    ]
)

# Compiling our model
# change the learning rate to 0.001
model2.compile(
    optimizer=optimizers.Adam(1e-3), loss="binary_crossentropy", metrics=["acc"]
)

# Callbacks
early_stopping_cb2 = keras.callbacks.EarlyStopping(monitor="val_loss", patience=7)

# Fitting our model
history2 = model2.fit(
    train_data,
    epochs=100,
    steps_per_epoch=10,
    callbacks=[early_stopping_cb2],
    validation_data=valid_data,
    verbose=2,
)


acc2 = history2.history["acc"]
val_acc2 = history2.history["val_acc"]
loss2 = history2.history["loss"]
val_loss2 = history2.history["val_loss"]
epochs2 = range(1, len(acc2) + 1)
plt.plot(epochs2, acc2, "bo", label="Training acc")
plt.plot(epochs2, val_acc2, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs2, loss2, "bo", label="Training loss")
plt.plot(epochs2, val_loss2, "r", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""## Architecture 3"""


# removed one dense layer
# changed the strides
# Added Gaussian Dropout layers
model3 = Sequential(
    [
        Conv2D(
            256,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
            input_shape=[96, 96, 3],
        ),
        MaxPooling2D(strides=1),
        GaussianDropout(0.1),
        Conv2D(
            256,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(strides=(2, 2)),
        GaussianDropout(0.1),
        Conv2D(
            512,
            3,
            padding="same",
            kernel_initializer="he_uniform",
            activation="relu",
        ),
        MaxPooling2D(strides=1),
        GaussianDropout(0.1),
        Flatten(),
        Dense(1028, kernel_initializer="he_uniform", activation="relu"),
        Dense(512, kernel_initializer="he_uniform", activation="relu"),
        Dense(1, activation="sigmoid"),
    ]
)

# Compiling our model
model3.compile(
    optimizer=optimizers.Adam(1e-4), loss="binary_crossentropy", metrics=["acc"]
)

# Callbacks
early_stopping_cb3 = keras.callbacks.EarlyStopping(monitor="val_loss", patience=7)

# Fitting our model
history3 = model3.fit(
    train_data,
    epochs=50,
    steps_per_epoch=10,
    callbacks=[early_stopping_cb3],
    validation_data=valid_data,
    verbose=2,
)


acc3 = history3.history["acc"]
val_acc3 = history3.history["val_acc"]
loss3 = history3.history["loss"]
val_loss3 = history3.history["val_loss"]
epochs3 = range(1, len(acc3) + 1)
plt.plot(epochs3, acc3, "bo", label="Training acc")
plt.plot(epochs3, val_acc3, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs3, loss3, "bo", label="Training loss")
plt.plot(epochs3, val_loss3, "r", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""# Final Architecture"""


y_pred1 = model1.predict(test_data, verbose=1)
y_pred_bool1 = np.argmax(y_pred1, axis=1)

print(classification_report(test_labels, y_pred_bool1))

"""### Confusion matirx"""

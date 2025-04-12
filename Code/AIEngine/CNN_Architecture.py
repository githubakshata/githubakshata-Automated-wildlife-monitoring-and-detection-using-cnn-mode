import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
import random

def GoogleNet_CNN(input_shape=(64, 64, 3), num_classes=10, max_layers=5):
    model = Sequential()
    model.add(layers.InputLayer(input_shape=input_shape))
    
    num_conv_layers = random.randint(1, max_layers)
    
    for _ in range(num_conv_layers):
        filters = random.choice([16, 32, 64, 128])
        kernel_size = random.choice([3, 5])
        model.add(layers.Conv2D(filters, (kernel_size, kernel_size), activation='relu', padding='same'))
        
        if random.choice([True, False]):
            pool_size = random.choice([2, 3])
            model.add(layers.MaxPooling2D(pool_size=(pool_size, pool_size)))
    
    model.add(layers.Flatten())
    
    num_fc_layers = random.randint(1, 2)
    
    for _ in range(num_fc_layers):
        units = random.choice([128, 256, 512])
        model.add(layers.Dense(units, activation='relu'))
        
    model.add(layers.Dense(num_classes, activation='softmax'))
    
    return model
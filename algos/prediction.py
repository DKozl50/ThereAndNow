import numpy as np
import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Reshape, Conv2D, Conv2DTranspose, UpSampling2D
from tensorflow.keras.layers import LeakyReLU, Dropout, ReLU, BatchNormalization, InputLayer, Concatenate
from tensorflow.keras.optimizers import Adam, RMSprop

import tensorflow as tf

class NN():
    def __init__(self, learned):
        
        self.user_data = pd.read_csv('user_data.csv', index_col=0)
        true_data = pd.read_csv('true_data.csv')
        exp = pd.read_csv('exp.csv')

        print('Data imported...')

        dropout = 0.2

        inp = tf.keras.layers.Input((21 + 245,))

        k = Dense(256)(inp)
        k = LeakyReLU(alpha=0.2)(k)
        k = Dropout(dropout)(k)

        k = Dense(128)(k)
        k = LeakyReLU(alpha=0.2)(k)
        k = Dropout(dropout)(k)

        k = Dense(64)(k)
        k = LeakyReLU(alpha=0.2)(k)
        k = Dropout(dropout)(k)

        k = Dense(32)(k)
        k = LeakyReLU(alpha=0.2)(k)
        k = Dropout(dropout)(k)

        k = Dense(16)(k)
        k = LeakyReLU(alpha=0.2)(k)
        k = Dropout(dropout)(k)

        k = Dense(1)(k)

        self.D = tf.keras.Model(
                    inputs=inp, 
                    outputs=Activation('sigmoid')(k))

        optimizer = RMSprop(lr=0.0002, decay=6e-8)
        self.D.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])


        dropout = 0

        inputs_ = tf.keras.layers.Input((20 + 245,))

        dense_1 = Dense(129)(inputs_)
        nonlin_1 = LeakyReLU(alpha=0.2)(dense_1)
        drop_1 = Dropout(dropout)(nonlin_1)

        dense_21 = Dense(64)(drop_1)
        nonlin_21 = LeakyReLU(alpha=0.2)(dense_21)
        drop_21 = Dropout(dropout)(nonlin_21)

        dense_22 = Dense(32)(drop_21)
        nonlin_22 = LeakyReLU(alpha=0.2)(dense_22)
        drop_22 = Dropout(dropout)(nonlin_22)

        dense_3 = Dense(8)(drop_22)
        nonlin_3 = LeakyReLU(alpha=0.2)(dense_3)
        drop_3 = Dropout(dropout)(nonlin_3)

        predictions = Dense(1)(drop_3)

        conc = tf.concat(axis=1, values=[inputs_, predictions])

        optimizer = Adam(1e-4)
        self.G = tf.keras.Model(
                    inputs=inputs_, 
                    outputs=conc)

        def loss(y, y_pred):
            return tf.reduce_mean((y_pred[:, -1:]-y[:, -1:])**2)

        self.G.compile(loss=loss, optimizer=optimizer)

        res_D = self.D(conc)

        self.AM =  tf.keras.Model(
                    inputs=inputs_, 
                    outputs=res_D)
        optimizer = RMSprop(lr=0.0001, decay=3e-8)
        self.AM.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        ids_list = self.user_data.index.unique()

        epochs = 50
        batch_size_noise = 64
        batch_size_true = 128

        true_data = exp[['User_ID', 'TRIP_MAIN_COUNTRY']].join(self.user_data, on = 'User_ID')

        cols = true_data.columns.tolist()
        true_data = true_data[cols[0:1] + cols[2:] + cols[1:2] ]

        if (not learned):
            print('Ready to learn...')

            for j in range(100):
                    r_f = np.random.choice(true_data.shape[0], 
                                                        batch_size_true, 
                                                        replace=False)
                    true_flights = true_data.loc[r_f].values
                    us_id = true_data.loc[r_f]['User_ID'].values
                    fake_batch = user_data.loc[us_id].values
                    
                    self.G.fit(fake_batch.astype('float32'), true_flights.astype('float32'))

            print('Learned to match numbers...')

            for j in range(50):
                true_flights = true_data.loc[np.random.choice(true_data.shape[0], 
                                                        batch_size_true, 
                                                        replace=False)].drop(['User_ID'], axis=1).values
                
                random_ids = np.random.choice(ids_list, batch_size_noise, replace=False)
                fake_batch = self.user_data.loc[random_ids].values
                fake_flights = self.G.predict(fake_batch.astype('float32'))

                x = np.concatenate((true_flights, fake_flights))
                y = np.ones([batch_size_true + batch_size_noise, 1])
                y[batch_size_true:, :] = 0
                
                d_loss = self.D.fit(x.astype('float32'), y.astype('float32'))
                
            print('Descriminator prelearned...')

            for i in range(epochs):
                for j in range(3):
                    true_flights = true_data.loc[np.random.choice(true_data.shape[0], 
                                                        batch_size_true, 
                                                        replace=False)].drop(['User_ID'], axis=1).values
                    
                    random_ids = np.random.choice(ids_list, batch_size_noise, replace=False)
                    fake_batch = self.user_data.loc[random_ids].values
                    fake_flights = self.G.predict(fake_batch.astype('float32'))

                    x = np.concatenate((true_flights, fake_flights))
                    y = np.ones([batch_size_true + batch_size_noise, 1])
                    y[batch_size_true:] = 0
                    
                    self.D.fit(x.astype('float32'), y.astype('float32'))
                
                self.D.trainable = False
                for j in range(5):
                    random_ids = np.random.choice(ids_list, batch_size_noise, replace=False)
                    fake_batch = self.user_data.loc[random_ids].values

                    y = np.ones([batch_size_noise, 1])
                    
                    self.AM.fit(fake_batch.astype('float32'), y.astype('float32'))
                
                self.D.trainable = True

            print('GAN learned')
        else:
            self.G.load_weights('./checkpoints/my_checkpointG')
            self.D.load_weights('./checkpoints/my_checkpointD')
            self.AM.load_weights('./checkpoints/my_checkpointAM')

            print('Weights loaded')

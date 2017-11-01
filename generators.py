import tensorflow as tf
from tensorflow.contrib import layers
from utils import reuse

def get_generator(arch, n_x, n_xl, n_channels, n_z, ngf):
    if arch == 'fc':
        @reuse('transformation')
        def generator(z_ph, n_x, normalizer_params):
            h = layers.fully_connected(z_ph, 500, 
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            h = layers.fully_connected(h, 500, 
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            x = layers.fully_connected(h, n_x, activation_fn=tf.nn.sigmoid)
            return tf.reshape(x, [-1, n_xl, n_xl, n_channels])
    elif arch == 'conv':
        @reuse('transformation')
        def generator(z_ph, n_x, normalizer_params):
            h = tf.reshape(z_ph, [-1, 1, 1, n_z])
            h = layers.conv2d_transpose(h, ngf*4, 3, padding='VALID',
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            h = layers.conv2d_transpose(h, ngf*2, 5, padding='VALID',
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            h = layers.conv2d_transpose(h, ngf, 5, stride=2, 
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            x = layers.conv2d_transpose(h, 1, 5, stride=2, activation_fn=tf.nn.sigmoid)
            return x
    else:
        @reuse('transformation')
        def generator(z_ph, n_x, normalizer_params):
            h = layers.fully_connected(z_ph, 500, 
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            h = layers.fully_connected(h, 500, 
                    normalizer_fn=layers.batch_norm, normalizer_params=normalizer_params)
            x = layers.fully_connected(h, n_x)
            return x

    return generator

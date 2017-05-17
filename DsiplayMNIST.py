import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.animation as animation
fig = plt.figure()
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
ims = []   ### list of images to be given to animation
## See (http://matplotlib.org/examples/animation/dynamic_image2.html)

with tf.Session() as sess:
    for i in range(0,600):
        image = mnist.train.images[i]
        image = np.array(255-image)
        pixels = image.reshape((28, 28))
        im = plt.imshow(pixels, cmap='gray')
        ims.append([im])
        ims.append([im])
        ims.append([im])
ani = animation.ArtistAnimation(fig, ims, interval=250, blit=True, repeat_delay=2000)

plt.show()
 


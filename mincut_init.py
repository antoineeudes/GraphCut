import numpy as np
import imageio
import matplotlib.pyplot as plt
import maxflow as gc

def binary_restore(I, Lambda=50):
    """I: noisy image to be restored.
    Lambda: weight of regularization factor.
    Return the denoised binary image."""
    g = gc.Graph[int]()
    nodeids = g.add_grid_nodes(I.shape)
    g.add_grid_edges(nodeids, Lambda)
    g.add_grid_tedges(nodeids, I, 255-I)
    g.maxflow()
    # Get the source/sink label
    labels = g.get_grid_segments(nodeids)
    I2 = np.int_(np.logical_not(labels))
    return I2

# Binary image restoration
I=imageio.imread('binary_image2.png')[:,:,0]
I2 = np.clip(I+np.random.normal(0, 100, I.shape),0,255).astype(np.uint8)
plt.subplot(131)
plt.imshow(I,cmap='gray')
plt.subplot(132)
plt.imshow(I2,cmap='gray')
plt.subplot(133)
plt.imshow(binary_restore(I2,70),cmap='gray')
plt.show()

# ------------------------------------------------- #

class Scribbler:
    """The scribbler lets you draw red and green zones with left and right mouse
    buttons"""
    def __init__(self, im):
        self.im = im
        self.channel = None
        self.cidpress = self.im.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.im.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.im.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def display(self,event):
        x,y = int(event.xdata),int(event.ydata)
        self.im.get_array()[y-2:y+3,x-2:x+3, self.channel]      = 255
        self.im.get_array()[y-2:y+3,x-2:x+3,(self.channel+1)%3] = 0
        self.im.get_array()[y-2:y+3,x-2:x+3,(self.channel+2)%3] = 0
        self.im.figure.canvas.draw()

    def on_press(self, event):
        if event.button==1:
            self.channel = 1
        else:
            self.channel = 0
        self.display(event)

    def on_motion(self, event):
        if self.channel is None: return
        self.display(event)

    def on_release(self, event):
        self.channel = None

I=imageio.imread('coins.png').astype(np.uint8)
fig = plt.figure()
ax = fig.add_subplot(111)
im=ax.imshow(np.stack((I,)*3, axis=-1))
s = Scribbler(im)
plt.show()

Irg = im.get_array()
plt.subplot(111)
plt.imshow(Irg)
plt.show()

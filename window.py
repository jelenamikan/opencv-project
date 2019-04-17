import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import filters

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.02, bottom=0.30, right=0.50)

img = cv2.imread('flowers.jpg')
color = img.copy()
gray = filters.grayscale(img)
l = plt.imshow(color[:,:,::-1])

axcolor = 'lightgoldenrodyellow'
axcont = plt.axes([0.55, 0.85, 0.38, 0.03], facecolor=axcolor)
axbright = plt.axes([0.55, 0.80, 0.38, 0.03], facecolor=axcolor)
axhue = plt.axes([0.55, 0.75, 0.38, 0.03], facecolor=axcolor)
axsat = plt.axes([0.55, 0.70, 0.38, 0.03], facecolor=axcolor)

scont = Slider(axcont, 'Contrast', 0, 20, valinit=10)
sbright = Slider(axbright, 'Brightness', 0, 100, valinit=50)
shue = Slider(axhue, 'Hue', 0, 20, valinit=10)
ssat = Slider(axsat, 'Saturation', 0, 20, valinit=10)

filtax = plt.axes([0.50, 0.02, 0.45, 0.65], facecolor=axcolor)
filt = RadioButtons(filtax, ('None','Clarendon', 'Gingham', 'Reyes', 'Amaro', 'Inkwell', 'Nashville', 'Toaster', '1977', 'Kelvin'), active=0)

def filter_func(label):
	reset()
	global color, gray
	if(label == 'Clarendon'):
		color = filters.Clarendon(img)
	elif(label == 'Gingham'):
		color = filters.Gingham(img)
	elif(label == 'Reyes'):
		color = filters.Reyes(img)
	elif(label == 'Amaro'):
		color = filters.Amaro(img)
	elif(label == 'Inkwell'):
		ink = filters.Inkwell(img)
	elif(label == 'Nahville'):
		color = filters.Nashville(img)
	elif(label == 'Toaster'):
		color = filters.Toaster(img)
	elif(label == '1977'):
		color = filters._1977(img)
	elif(label == 'Kelvin'):
		color = filters.Kelvin(img)
	else:
		color = filters.Original(img,shue.val/10,ssat.val/10,scont.val/10,sbright.val-50)
	if(radio.value_selected == 'color' and label != 'Inkwell'):
		l.set_data(color[:,:,::-1])
	else:
		if(label != 'Inkwell'):
			gray = filters.grayscale(color[:,:,::-1])
			l.set_data(gray)
			l.set_cmap('gray')
		else:
			l.set_data(ink)
			l.set_cmap('gray')
	fig.canvas.draw_idle()

filt.on_clicked(filter_func)

def reset():
	scont.reset()
	sbright.reset()
	shue.reset()
	ssat.reset()

def update(val):
	global color 
	color = filters.brightness_contrast(img,scont.val/10,sbright.val-50)
	color = filters.hue_saturation(color,shue.val/10,ssat.val/10)
	if(radio.value_selected == 'color'):
		l.set_data(color[:,:,::-1])
	else:
		global gray 
		gray = filters.grayscale(color[:,:,::-1])
		l.set_data(gray)
		l.set_cmap('gray')
	fig.canvas.draw_idle()

scont.on_changed(update)
sbright.on_changed(update)
shue.on_changed(update)
ssat.on_changed(update)

rax = plt.axes([0.1, 0.02, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('color', 'grayscale'), active=0)

def colorfunc(label):
	if(label == 'color'):
		l.set_data(color[:,:,::-1])
	else:
		l.set_data(gray)
		l.set_cmap('gray')
	fig.canvas.draw_idle()

radio.on_clicked(colorfunc)

plt.show()

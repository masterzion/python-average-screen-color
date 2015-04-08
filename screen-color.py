
#!/usr/bin/env python
# 
# Autor: Jairo Moreno
#
# Get One single color to represent the screen
# 


import gtk.gdk
import sys
import wx
from time import sleep
import milight

# interval between pixels
# less interval will increase the cpu usage
interval = 100


# Create an array of points (pixels) to be monitored
def MonitoredPoints(interval):
	app = wx.PySimpleApp()
	screensize = wx.GetDisplaySize()

	countx = screensize[0]/interval
	county = screensize[1]/interval
	actualcolor = (0,0,0)
	totalpoints = countx * county
	monitoredpoints = []

	for x in range(0, countx):
		for y in range(0, county):
			monitoredpoints.append([x * interval, y * interval])

	return monitoredpoints




def CurrentColor(points, pointcount):
    # get screen point colors
    # http://stackoverflow.com/questions/27395968/get-screen-pixel-color-linux-python3
	w = gtk.gdk.get_default_root_window()
	sz = w.get_size()
	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
	pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
	pixel_array = pb.get_pixels_array()

	#sum colors of all monitored pixels
	red = 0
	green = 0
	blue = 0
	for point in points:
		color = pixel_array[point[1]] [point[0]]

		red   = red + color[0]
		green = green + color[1]
		blue  = blue + color[2]

	# divide by point count
	red = red / pointcount
	green = green / pointcount
	blue = blue / pointcount

	return (red, green, blue)


# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
#def hex_to_rgb(value):
#	value = value.lstrip('#')
#	lv = len(value)
#	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#def rgb_to_hex(rgb):
#	return '#%02x%02x%02x' % rgb

points = MonitoredPoints(interval)
pointcount = len(points)
controller = milight.MiLight({'host': '192.168.1.110', 'port': 8899}, wait_duration=0) 

# execute each 0.1 milisecond
while True:
	actualcolor =CurrentColor(points, pointcount)
	milight.color_from_rgb(actualcolor[0], actualcolor[1], actualcolor[2])
#	print  rgb_to_hex( actualcolor )
	sleep(0.1)

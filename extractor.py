from skimage import data, io
import numpy as np

(y_0, x_0) = (500,1062)
tile_radius = 141

# first pass
# for i in range(12,286):
# 	img = io.imread('./frames/img-{}.jpeg'.format(i))
# 	crop = img[y_0-tile_radius:y_0+tile_radius,x_0-tile_radius:x_0+tile_radius]
# 	io.imsave('./frames/out/' +  str(i-11) + '.png',crop)

#ffmpeg -i %d.png -vcodec qtrle og.mov

# 2nd pass to fix
# for i in range(1,275):
# 	img = io.imread('./frames/out/{}.png'.format(i))
# 	img[:,:(tile_radius - 1)] = img[:,:tile_radius:-1]
# 	io.imsave('./frames/out/2/' +  str(i) + '.png',img)

# 3rd pass to fix earlier frames
y_0 -= 2*tile_radius - 2
x_0 -= 2*tile_radius - 2
for i in range(12,91):
	img = io.imread('./frames/img-{}.jpeg'.format(i))
	crop = img[y_0-tile_radius:y_0+tile_radius,x_0-tile_radius:x_0+tile_radius]
	crop[:,:tile_radius:-1] = crop[:,:(tile_radius - 1)]
	crop[:(tile_radius - 1),:] = crop[:tile_radius:-1,:]
	io.imsave('./frames/out/3/' +  str(i-11) + '.png',crop)

# ffmpeg -i %d.png -vcodec qtrle fg.mov

# need 2 integrate w/ the gui i did to make everything possible w/ one script
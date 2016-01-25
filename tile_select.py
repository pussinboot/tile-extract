from skimage import data
from skimage.viewer import ImageViewer
from skimage.viewer.plugins import PlotPlugin
from skimage.viewer.canvastools import RectangleTool
import numpy as np

class TileViewer(ImageViewer):
	"""
	special version of imageviewer that lets you select a rectangle
	that supposedly tiles and see how that looks 
	"""
	def __init__(self,image, useblit=True,x=10,y=10):
		super(TileViewer,self).__init__(image,useblit)
		self.startx, self.starty = x, y

	def _show(self):
		self.move(self.startx, self.starty)
		for p in self.plugins:
			p.show()
		super(ImageViewer, self).show()
		self.activateWindow()
		self.raise_()

def blit(dest, src, loc):
	pos = [i if i >= 0 else None for i in loc]
	neg = [-i if i < 0 else None for i in loc]
	target = dest[[slice(i,None) for i in pos]]
	src = src[[slice(i, j) for i,j in zip(neg, target.shape)]]
	target[[slice(None, i) for i in src.shape]] = src
	return dest

def copy_tile(source_img,extents):
	x0, x1, y0, y1 = np.int64(extents)
	dest = np.zeros(image.shape)
	src_w, src_h = source_img.shape[:2]
	tile_w, tile_h = x1 - x0, y1 - y0
	w_offset = src_w % tile_w
	h_offset = src_h % tile_h
	for w in range(0,src_w // tile_w + 2):
		for h in range(0,src_h // tile_h + 2):
			blit(dest,source_img[y0:y1,x0:x1],(h*tile_h-h_offset,w*tile_w-w_offset))
	return dest

class TilePreview(PlotPlugin):
	def __init__(self,**kwargs):
		super(TilePreview,self).__init__(height=400, width=400,**kwargs)
		
	def attach(self,image_viewer):
		super(TilePreview,self).attach(image_viewer)
		self.rect_tool = RectangleTool(self.image_viewer,
						 on_release = self.update)
		self.ax.set_xticks(())
		self.ax.set_yticks(())
		self.ax.autoscale_view('tight')

	def update(self,extents):
		#print(extents)
		new_img = copy_tile(self.image_viewer.image,extents)
		self.ax.imshow(new_img)
		self.redraw()
if __name__ == '__main__':
	image = data.camera()
	viewer = TileViewer(image,x=50,y=50)
	tp = TilePreview()
	viewer += tp
	viewer.show()


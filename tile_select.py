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
		x0, x1, y0, y1 = np.int64(extents)
		self.ax.imshow(self.image_viewer.image[y0:y1,x0:x1])
		self.redraw()

image = data.camera()
viewer = TileViewer(image,x=50,y=50)
tp = TilePreview()
viewer += tp
viewer.show()

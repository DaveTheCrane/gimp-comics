#!/usr/bin/env python

from gimpfu import *

def comic_grid(image, drawable, rows=3, columns=3, margin=120, gutter=32):
	w=image.width
	h=image.height
	useableW=w-(2*margin)-((columns-1)*gutter)
	useableH=h-(2*margin)-((rows-1)*gutter)
	cellW=useableW/columns
	cellH=useableH/rows
	cellDims=[]
	for i in range(columns):
		for j in range(rows):
			l=margin+((cellW+gutter)*i)
			t=margin+((cellH+gutter)*j)
			cellDims.append({ 'left': l,'top':t,'w':cellW,'h':cellH })
	pdb.gimp_selection_none(image)
	for cell in cellDims:
		pdb.gimp_rect_select(image,cell['left'],cell['top'],cell['w'],cell['h'],0,0,0)

register(
	"pygimp_sunwheel_comic_grid",
	"Select regular rectangular grid suitable for comic strip",
	"Select regular rectangular grid suitable for comic strip",
	"Dave Crane",
	"Dave Crane",
	"2011",
	"<Image>/Filters/Comics/Grid",
	"RGB*, GRAY*",
	[
		(PF_INT, "rows", "No. rows", 3),
		(PF_INT, "cols", "No. columns", 3),
		(PF_INT, "margin", "Outer Margin", 120),
		(PF_INT, "gutter", "Gutter width", 32)
	],
	[],
	comic_grid)

main()
""" usage
img=gimp.image_list()[0]
grid(img,6,4,40,20)
grid(img,6,4,120,32)
"""

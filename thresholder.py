#!/usr/bin/env python

from gimpfu import *

def comic_thresholder(image, drawable, thresholds="63,127,192"):
	source_layer=pdb.gimp_image_get_active_layer(image)
	source_name=pdb.gimp_item_get_name(source_layer)
	#create new layer group
	grp=pdb.gimp_layer_group_new(image)
	pdb.gimp_item_set_name(grp,source_name+" threshold masks")
	pics=pdb.gimp_image_get_layer_by_name(image,"pictures")
	pdb.gimp_image_insert_layer(image,grp,pics,-1)
	thresh_points=thresholds.split(",")
	for thresh in thresh_points:
		#  copy source image
		copy=pdb.gimp_layer_copy(source_layer,1)
		pdb.gimp_item_set_name(copy,source_name+" thresh "+thresh)
		pdb.gimp_image_insert_layer(image,copy,grp,-1)
		#  threshold copied image
		pdb.gimp_threshold(copy,int(thresh),255)
		#  add layer mask to copied image, using greyscale
		mask=pdb.gimp_layer_create_mask(copy,5)  #ADD_COPY_MASK
		pdb.gimp_layer_add_mask(copy,mask)
		#  invert layer mask
		pdb.gimp_image_set_active_layer(image,copy)
		pdb.gimp_layer_set_edit_mask(copy,1)
		pdb.gimp_selection_all(image)
		pdb.gimp_invert(mask)
		#  delete image content
		pdb.gimp_layer_set_edit_mask(copy,0)
		pdb.gimp_edit_clear(copy)
	pdb.gimp_selection_all(image)
	# copy the whole group, to get reference layers
	copy_grp=grp.copy()
	pdb.gimp_image_insert_layer(image,copy_grp,pics,-1)
	# iterate through copied group, filling in black
	pdb.gimp_context_set_sample_transparent(1)
	pdb.gimp_context_set_foreground((0,0,0))
	pic_layer_info=pdb.gimp_item_get_children(copy_grp)
	pic_layer_ids=pic_layer_info[1]
	for pic_layer_id in pic_layer_ids:
		pic_layer=gimp.Item.from_id(pic_layer_id)
		pdb.gimp_drawable_fill(pic_layer,0)
	# set opacity of copied group to 20%
	pdb.gimp_layer_set_opacity(copy_grp,20)


register(
	"pygimp_sunwheel_comic_thresholder",
	"Set up several layer masks from current layer, ready for scribbling",
	"Set up several layer masks from current layer, ready for scribbling",
	"Dave Crane",
	"Dave Crane",
	"2014",
	"<Image>/Filters/Comics/Threshold",
	"RGB*, GRAY*",
	[
		(PF_STRING, "thresholds", "List of Threshold values", "63,127,192")
	],
	[],
	comic_thresholder)

main()
""" usage
img=gimp.image_list()[0]
comic_thresholder(img,"63,127,192")
"""

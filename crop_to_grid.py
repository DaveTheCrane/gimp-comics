#!/usr/bin/env python

from gimpfu import *

def merge_layer_group(image,group):
	#get members of layer group
	layer_info=pdb.gimp_item_get_children(group)
	layer_ids=layer_info[1]
	count=len(layer_ids)
	print layer_ids," (",count,")"
	for index in range(count-2,-1,-1):
		layer_id=layer_ids[index]
		print " + ",layer_id," at ",index
		layer=gimp.Item.from_id(layer_id)
		pdb.gimp_image_merge_down(image,layer,0)
		


def crop_to_grid(image, drawable, target_group, grid_layer, merge_group=1, white_bg=1):
	if (pdb.gimp_item_is_group(target_group)):
		pic_layer_info=pdb.gimp_item_get_children(target_group)
		pic_layer_ids=pic_layer_info[1]
		#print "pic layer ids:",pic_layer_ids 
		pdb.gimp_context_set_sample_transparent(1)
		for pic_layer_id in pic_layer_ids:
			pic_layer=gimp.Item.from_id(pic_layer_id)
			#print pic_layer.offsets, pic_layer.width, pic_layer.height			
			pdb.gimp_layer_add_alpha(pic_layer)
			x=pic_layer.offsets[0]
			y=pic_layer.offsets[1]
			w=pic_layer.width
			h=pic_layer.height			
			centre_x=x+(w/2)
			centre_y=y+(h/2) 
			pdb.gimp_selection_none(image)
			pdb.gimp_image_select_contiguous_color(image,0,grid_layer,centre_x,centre_y)
			pdb.gimp_selection_grow(image,10)
			#print "selected",pdb.gimp_selection_bounds(image)
			pdb.gimp_selection_invert(image)
			pdb.gimp_edit_clear(pic_layer)
		#copy the group
		if (merge_group):
			copy_grp=target_group.copy()
			parent=pdb.gimp_item_get_parent(target_group)
			posn=pdb.gimp_image_get_item_position(image,target_group)
			pdb.gimp_image_insert_layer(image,copy_grp,parent,posn+1)
			#add white bg behind
			if (white_bg):
				w=pdb.gimp_image_width(image)
				h=pdb.gimp_image_height(image)
				whiteout=pdb.gimp_layer_new(image,w,h,0,"whiteout",100,0)
				pdb.gimp_image_insert_layer(image,whiteout,copy_grp,len(pic_layer_ids))
				pdb.gimp_selection_none(image)
				pdb.gimp_invert(whiteout)
			merge_layer_group(image,copy_grp)

		


register(
	"pygimp_sunwheel_crop_to_grid",
	"Crop all images in group to fit a grid",
	"Load all images in folder into template files",
	"Dave Crane",
	"Dave Crane",
	"2015",
	"<Image>/Filters/Comics/Crop To Grid",
	"RGB*, GRAY*",
	[
          (PF_LAYER, "target_group", "Pictures Group", None),
          (PF_LAYER, "grid_layer", "Grid Layer", None),
          (PF_TOGGLE, "merge_group",   "Make flattened copy", 1), 
          (PF_TOGGLE, "white_bg",   "Add White Backdrop?", 1),
	],      
	[],
	crop_to_grid)

main()
""" usage
img=gimp.image_list()[0]
grid(img,6,4,40,20)
grid(img,6,4,120,32)
"""

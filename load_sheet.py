#!/usr/bin/env python

from gimpfu import *
import os
import math

def load_sheet(image, drawable, target_file, target_group, output_file_root="sheet", rows=3, columns=3):
	#open folder/file
	target_dir=os.path.dirname(target_file)
	all_files=os.listdir(target_dir)
	#list contents, get them all
	img_files = [ f for f in all_files if (f.lower().endswith(".jpg") or f.lower().endswith(".png")) ]
	#figure out how many pages needed, use current file as template
	tiles_per_page=rows*columns
	num_pages=int(math.ceil(float(len(img_files))/tiles_per_page))
	output_dir=os.path.join(target_dir,"sheets")
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	print num_pages,"pages of",tiles_per_page,"images each"
	#iterate, saving copies as required 
	for current_page in range(1,num_pages+1,1):
		file_name=os.path.join(output_dir,output_file_root+"_"+str(current_page)+".xcf")
		start_index=(current_page-1)*tiles_per_page
		end_index=start_index+tiles_per_page
		if len(img_files)<end_index:
			end_index=len(img_files)
		img_in_curr_page=img_files[start_index:end_index]
		print "page =",current_page,"images =",img_in_curr_page
		for img_file in img_in_curr_page:
			full_img_path=os.path.join(target_dir,img_file)
			new_img_layer=pdb.gimp_file_load_layer(image,full_img_path)
			pdb.gimp_image_insert_layer(image,new_img_layer,target_group,0)
		pdb.gimp_xcf_save(0,image,image.active_drawable,file_name,file_name)
		pic_layer_info=pdb.gimp_item_get_children(target_group)
		pic_layer_ids=pic_layer_info[1]
		for pic_layer_id in pic_layer_ids:
			pic_layer=gimp.Item.from_id(pic_layer_id)
			pdb.gimp_image_remove_layer(image,pic_layer)


register(
	"pygimp_sunwheel_load_sheet",
	"Load all images in folder into template files",
	"Load all images in folder into template files",
	"Dave Crane",
	"Dave Crane",
	"2015",
	"<Image>/Filters/Comics/Face Sheets",
	"RGB*, GRAY*",
	[
		(PF_FILE, "target_file", "Target File/Dir", 0),
		(PF_LAYER, "target_group", "Pictures Group", None),
		(PF_STRING, "output_file_root", "Base Output Filename", "sheet"),
		(PF_INT, "rows", "No. rows", 3),
		(PF_INT, "cols", "No. columns", 3)
	],
	[],
	load_sheet)

main()
""" usage
img=gimp.image_list()[0]
grid(img,6,4,40,20)
grid(img,6,4,120,32)
"""

import sys
import glob
import os
from wand import image

def apply_mask(img, mask):
    img.alpha_channel = True

    with image.Image(width=img.width, height=img.height, background=image.Color("transparent")) as alpha_image:
        #alpha_image.composite_channel("alpha", mask, "copy_alpha")
        img.composite_channel("alpha", mask, "dst_in")

def convert_image(img_file, out_path):
	mask = image.Image(filename='mask.dds')
	img = image.Image(filename=img_file)

	# Apply alpha mask
	apply_mask(img, mask)

	with img as op:
	    op.compression = 'dxt5'
	    op.save(filename=out_path)


print("spriteTypes = {")
print("\t# This file was auto-generated by mask_icons.py")

for file in glob.glob("../unmasked/*.dds"):
	filename = os.path.basename(file)
	newfile = "../" + filename
	convert_image(file, newfile)

	gfx_id = str.lower(filename[0:len(filename)-4])
	print("\tspriteType = { name = \"GFX_"+gfx_id+"\" texturefile = \"gfx/event_pictures/"+filename+"\" }")

print("}")
exit(0)
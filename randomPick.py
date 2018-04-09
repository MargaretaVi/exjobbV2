import os, shutil, sys, math, pdb, glob
from numpy import random

#Params: input folder with images
# output folder where the images are going to be moved.
# how many percentage are going to be moved
def main(sys):
	print("starting")
	input_folder = os.path.abspath(sys.argv[1])
	output_folder = os.path.abspath(sys.argv[2])
	os.makedirs(output_folder, exist_ok=True)
	how_many_percentage = float(sys.argv[3])

	print('creating list of files to copy')
	all_images_in_dir = glob.glob(os.path.abspath(input_folder)  + '/*.jpeg')
	number_of_files_to_move = math.ceil(len(all_images_in_dir)*how_many_percentage)
	filenames = random.choice(all_images_in_dir, number_of_files_to_move)

	print('starting to copy files')	
	for file in filenames:
		basename = os.path.basename(file)
		name = os.path.splitext(basename)[0]

		scrpath_img = os.path.join(input_folder, basename)
		dstpath_img = os.path.join(output_folder, basename)
		xml_name = name + '.xml'
		scrpath_xml = os.path.join(input_folder, xml_name)
		dstpath_xml = os.path.join(output_folder, xml_name)
		try:
			shutil.move(scrpath_img, dstpath_img)
			shutil.move(scrpath_xml, dstpath_xml)
		except:
			print('couldnt move', name)	

	print("finished")

# counts files in a folder
def filecount(folder_path):
	numfiles = sum(1 for f in os.listdir(folder_path) if (os.path.isfile(os.path.join(folder_path, f)) and os.path.join(folder_path,f).endswith('.jpeg')))
	return numfiles

if __name__ == "__main__":
    main(sys)
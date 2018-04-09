import os, shutil, sys, math
from numpy import random

def main(sys):
	print("starting")
	input_folder = os.path.abspath(sys.argv[1])
	output_folder = os.path.abspath(sys.argv[2])
	os.makedirs(output_folder, exist_ok=True)
	how_many_percentage = float(sys.argv[3])
	
	for subdir in os.listdir(input_folder):
		if subdir != "turnKnob":
			continue
		directory = os.path.join(input_folder, subdir)
		if os.path.isdir(directory):
			directory = directory + '/'
			filecount(os.path.abspath(directory))
			directory_full_path = os.path.abspath(directory)			
			number_of_files_to_move = math.ceil(filecount(directory_full_path)*how_many_percentage)
			all_files_in_dir = os.listdir(directory_full_path)
			filenames = random.choice(all_files_in_dir, number_of_files_to_move)		
			for name in filenames:
				scrpath = os.path.join(directory_full_path,name)
				tmp_folder_name = output_folder + '/' + subdir
				os.makedirs(tmp_folder_name, exist_ok=True)
				dstpath = os.path.join(os.path.abspath(tmp_folder_name) + '/' ,name)
				try:	
					shutil.move(scrpath, dstpath)
				except:
					print("moving file failed", name)
					continue		
	print("finished")

# counts files in a folder
def filecount(folder_path):
	numfiles = sum(1 for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
	return numfiles

if __name__ == "__main__":
    main(sys)
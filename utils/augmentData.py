import os, sys, math, cv2
import numpy as np
from numpy import random
# input folder cannot contain any subdir

def main(sys):
	input_folder = sys.argv[1]
	rotate_angle = sys.argv[2]
	how_many_percentage = float(sys.argv[3])

	input_folder = os.path.abspath(input_folder)
	rotate_angle = int(rotate_angle)

	number_of_files = math.ceil(filecount(input_folder)*how_many_percentage)
	all_files_in_dir = os.listdir(input_folder)
	filenames = random.choice(all_files_in_dir, number_of_files)	

	for file in filenames:
		file_path = input_folder + '/' + file
		img = cv2.imread(file_path)
		img_augmented = contrast_change(img)

		cv2.imwrite(file_path, img_augmented)


def contrast_change(img):
	lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5,5))
	cl = clahe.apply(l)
	
	limg = cv2.merge((cl,a,b))
	
	final_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return final_image


def rot_img(img, rot_angle):
	num_rows, num_cols = img.shape[:2]
	rot_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), rotate_angle, 1)
	img_rotation = cv2.warpAffine(img,rot_matrix, (num_cols, num_rows))
	return img_rotation

# counts files in a folder
def filecount(folder_path):
	numfiles = sum(1 for f in os.listdir(folder_path) if (os.path.isfile(os.path.join(folder_path, f)) and os.path.join(folder_path,f).endswith('.jpeg')))
	return numfiles

if __name__ == '__main__':
	main(sys)
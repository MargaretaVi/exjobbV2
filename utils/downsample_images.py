import sys, os, cv2, math
import numpy as np
# this script an image and resize it to AxA, the image might be cropped. 

def resize_image(image, lenght = None, interpolation_method = cv2.INTER_AREA):
	dimension = None
	(original_height, original_width) = image.shape[:2]
	if lenght is None:
		return image_name
	# crop the width after height is resized 	
	if (original_width <= original_height):
		ratio = lenght /float(original_width)
		dimension = (lenght, int(original_height*ratio))
	elif (original_width > original_height):	
		ratio = lenght / float(original_height)
		dimension = (int(original_width*ratio), lenght)
	resized = cv2.resize(image, dimension, interpolation = interpolation_method)	

	return resized


def main(arg):
	image_folder_path = sys.argv[1]
	saving_folder_path = sys.argv[2]
	os.makedirs(saving_folder_path, exist_ok=True)
	wanted_image_lenght = int(sys.argv[3])
    
	for image_name in os.listdir(image_folder_path):
		image_full_path = os.path.join(image_folder_path, image_name)
		img = cv2.imread(image_full_path,1)
		new_image = resize_image(img, wanted_image_lenght)
		new_width, new_height = new_image.shape[:2]
		if new_width > new_height:
			difference = new_width - wanted_image_lenght
			new_image = new_image[math.ceil(difference/2)+1: int(new_width - difference/2) -1 ,:]
		elif new_width < new_height:
			difference = new_height - wanted_image_lenght
			new_image = new_image[:, math.ceil(difference/2): int(new_height - difference/2)]

		saving_path = os.path.join(saving_folder_path, image_name)
		cv2.imwrite(saving_path, new_image)


if __name__ == "__main__":
    main(sys)



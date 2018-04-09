import cv2, math, sys, os


# crop image to decenter object

def main(arg):
	image_folder_path = sys.argv[1]
	saving_folder_path =sys.argv[2]
	wanted_size = sys.argv[3]
	
	image_folder_path = os.path.abspath(image_folder_path)
	os.makedirs(saving_folder_path, exist_ok=True)

	for subfolder in os.listdir(image_folder_path):
		subfolder_full_name = os.path.join(image_folder_path, subfolder)
		for file in os.listdir(str(subfolder_full_name+'/')):
			print(file)
			if os.path.isfile(os.path.join(image_folder_path,subfolder, file)):
				file_full_name = os.path.join(image_folder_path,subfolder, file)
				img = cv2.imread(os.path.abspath(file_full_name))
				height, width = img.shape[:2]
				diff = abs(int(wanted_size) - height)

				for i in range(1,5):
					image_name = file[:-5] + '_%d' % i + '.jpeg'
					saving_path = os.path.join(saving_folder_path, image_name)
					print(saving_path)
					if i == 1:
						crop_img = img[diff:height, diff:width]
						cv2.imwrite(saving_path, crop_img)
					elif i == 2:	
						crop_img = img[:height-diff, :width-diff]
						cv2.imwrite(saving_path, crop_img)
					elif i == 3:	
						crop_img = img[:height-diff, diff:width]
						cv2.imwrite(saving_path, crop_img)
					else: 	
						crop_img = img[diff:height, :width-diff]
						cv2.imwrite(saving_path, crop_img)	


if __name__ == "__main__":
    main(sys)

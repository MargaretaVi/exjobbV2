import os, sys, math, cv2
import numpy as np
from numpy import random
import pdb
from shutil import copy
# input folder cannot contain any subdir

def main(sys):
	input_folder = sys.argv[1]
	train_folder = sys.argv[2]
	val_folder = sys.argv[3]
	test_folder = sys.argv[4]
	object_names = sys.argv[5]

	input_folder = os.path.abspath(input_folder)
	all_files_in_dir = os.listdir(input_folder)
	all_images = []

	#create a list with only images
	for file in all_files_in_dir:
		if file.endswith(".jpeg"):
			all_images.append(file)

	cabel_lst, car_lst, e_stop_lst, handle_lst, turn_knob_lst = sort_list(all_images)
	cabel_num_files = num_of_files_to_change(cabel_lst)
	car_num_files = num_of_files_to_change(car_lst)
	eStop_num_files = num_of_files_to_change(e_stop_lst)
	handle_num_files = num_of_files_to_change(handle_lst)
	turn_knob_num_files = num_of_files_to_change(turn_knob_lst)


	filenames_cabel = list(random.choice(cabel_lst, cabel_num_files))
	filenames_car = list(random.choice(car_lst, car_num_files))
	filename_eStop = list(random.choice(e_stop_lst, eStop_num_files))
	filenames_handle = list(random.choice(handle_lst, handle_num_files))
	filenames_turn_knob = list(random.choice(turn_knob_lst, turn_knob_num_files))

	all_images_to_change = []
	all_images_to_change.extend(filenames_turn_knob + filenames_handle +
	 filenames_car + filenames_cabel + filename_eStop)

	# these list only contains the images!!
	training_set, validation_set, testing_set = divide_data_test_train_validation(cabel_lst,
		car_lst, e_stop_lst, handle_lst, turn_knob_lst)

	com_training_set,com_validation_set, com_testing_set = create_complete_sets(input_folder,
		training_set, validation_set, testing_set)
	if any(map(lambda v:v in com_testing_set, com_training_set)):
		print('not unique test and training')
	if any(map(lambda v:v in com_testing_set, com_validation_set)):
		print('not unique test and validation')
	if any(map(lambda v:v in com_training_set, com_validation_set)):
		print('not unique training and validation')
	pdb.set_trace()
	copy_files(train_folder, com_training_set)
	copy_files(val_folder, com_validation_set)
	copy_files(test_folder, com_testing_set)

	change_images(all_images_to_change, input_folder)
def dict_with_file_to_change(orig_dict):
	file_change = {}
	for key in orig

def copy_files(output_folder, lst):
	for file in lst:
		copy(file, output_folder)


def create_complete_sets(input_folder, train, validation, test):
	training_set = []
	validation_set = []
	testing_set = []

	complete_training_set = create_complete_sets_help(training_set, train, input_folder)
	complete_validation_set = create_complete_sets_help(validation_set, validation, input_folder)
	complete_test_set = create_complete_sets_help(testing_set, test, input_folder)
	return complete_training_set, complete_validation_set, complete_test_set


def create_complete_sets_help(new_lst, old_lst, input_folder):
	for elem in old_lst :
		img_abs_path = os.path.join(input_folder, elem)
		xml_path = create_xml_file_name(img_abs_path)
		if os.path.isfile(img_abs_path) and os.path.isfile(xml_path):
			new_lst.extend([img_abs_path, xml_path])
		else:
			continue

	return new_lst

def create_xml_file_name(image_file_name):
	file_name, _ = os.path.splitext(image_file_name)
	return file_name + '.xml'

# the input to this functions is x numbers of lists
def divide_data_test_train_validation(*args):
	training_set = []
	validation_set = []
	testing_set = []

	for arg in args:
		random.shuffle(arg)
		tmp_len_lst = len(arg)
		training_set.extend(arg[:math.floor(tmp_len_lst/2)])
		validation_set.extend(arg[math.ceil(tmp_len_lst/2):math.floor(3*tmp_len_lst/4)])
		testing_set.extend(arg[math.ceil(3*tmp_len_lst/4):])

	return training_set, validation_set, testing_set

def num_of_files_to_change(lst):
	percentage = 0.3
	#divide by two since there are .xml files in the lst as well.
	return math.ceil(len(lst)/2*percentage)

def sort_list(lst,object_names):
	obj_dict = {}
	for name in object_names:
		tmp = []
		for file in lst:
			if name in file:
				tmp.append(file)
		obj_dict[name] = tmp
	return obj_dict

def change_images(list_of_images, input_folder):
	for img in list_of_images:
		img_path = input_folder + '/' + img
		img = cv2.imread(img_path)

		list_of_augmentation_function = [contrast_change, add_gaussian_noise]
		augmented_img = random.choice(list_of_augmentation_function)(img)

		cv2.imwrite(img_path, augmented_img)

def contrast_change(img):
	lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5,5))
	cl = clahe.apply(l)

	limg = cv2.merge((cl,a,b))

	final_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return final_image

def add_gaussian_noise(img):
    gaussian_noise_img = cv2.GaussianBlur(img,(7,7),0)

    return gaussian_noise_img

if __name__ == '__main__':
	main(sys)

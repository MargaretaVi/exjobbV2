import os, re
import pdb

GROUND_TRUTH_BOUNDING_BOX = '/home/xmreality/Documents/exjobb/Object_detection_rcnn_automatic_annotation_test/test_images/'
NETWORK_BOUNDING_BOX_DIR = '/home/xmreality/Documents/exjobb/Object_detection_rcnn_annotation_test/output/test_images/prediction'

lst_of_groundtruth_files = []
for file in os.listdir(GROUND_TRUTH_BOUNDING_BOX):
	if file.endswith('xml'):	
		lst_of_groundtruth_files.append(GROUND_TRUTH_BOUNDING_BOX + file)
	
# Calculates the Intersection over Union ratio. 
def bounding_box_intersection_over_union(boxA, boxB):
  # determine the (x, y)-coordinates of the intersection rectangle
  yA = max(boxA[0], boxB[0])
  xA = max(boxA[1], boxB[1])
  yB = min(boxA[2], boxB[2])
  xB = min(boxA[3], boxB[3])
 
  # compute the area of intersection rectangle, makes sure that if there is no intersection
  # answer is zero
  interArea = max(0,(xB - xA + 1)) * max(0,(yB - yA + 1))
 
  # compute the area of both the prediction and ground-truth
  # rectangles
  boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
  boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
  # compute the intersection over union by taking the intersection
  # area and dividing it by the sum of prediction + ground-truth
  # areas - the interesection area
  iou = interArea / float(boxAArea + boxBArea - interArea)
 
  # return the intersection over union value
  return iou

def compare_files(pred_file, GT_file):
	GT_dict = {}
	pred_dict = {}
	true_positive = 0
	true_negative = 0
	false_positive = 0 
	false_negative = 0
	convert_file_to_dict(pred_file, pred_dict)
	convert_file_to_dict(GT_file, GT_dict)
	
	for pred_object, pred_object_dict in pred_dict.items():
		pred_label = pred_object_dict['label']
		pred_box = create_list_of_values_for_bb(pred_object_dict)
		for GT_object, GT_object_dict in GT_dict.items():
			GT_box = create_list_of_values_for_bb(GT_object_dict)
			GT_label = GT_object_dict['label']
			iou = bounding_box_intersection_over_union(pred_box, GT_box)
			if iou >= 0.8:
				if pred_label == GT_label:
					true_positive += 1
				else:
					false_positive += 1
			else: # iou < 0.5
				if pred_label == GT_label:
					false_negative += 1
				else:
					true_negative += 1

	precision = true_positive / (true_positive + false_positive)

	recall = true_positive / (true_positive + false_negative)

def create_list_of_values_for_bb(dict):
	box = [dict['ymin'], dict['xmin'], dict['ymax'], dict['xmax']]
	return box

def convert_file_to_dict(file,dict):
	with open(file) as f:
		counter = 0
		for line in f:
			counter += 1
			(label, ymin, xmin, ymax, xmax) = convert_line_to_bb_and_label(line)
			dict_elem = {'label': label, 'ymin' : float(ymin), 'xmin' : float(xmin) ,'ymax': float(ymax), 'xmax' : float(xmax)}
			dict_key = 'object%d' % (counter)
			dict[dict_key] = dict_elem	

def convert_line_to_bb_and_label(line):
	label = get_label(line)
	ymin = get_ymin(line)
	ymax = get_ymax(line)
	xmin = get_xmin(line)
	xmax = get_xmax(line)

	return(label, ymin, xmin, ymax, xmax)

def get_label(line):
	find = re.compile('label:(?:)(.*)(?<=)ymin')
	label = re.search(find, line).group(1)
	return label[:-1]

def get_xmin(line):
	find = re.compile('xmin:(?:)(.*)(?<=)ymax')
	xmin = re.search(find, line).group(1)
	return xmin

def get_xmax(line):
	find = re.compile('xmax:(?:)(.*)')
	xmax = re.search(find, line).group(1)
	return xmax

def get_ymin(line):
	find = re.compile('ymin:(?:)(.*)(?<=)xmin')
	ymin = re.search(find, line).group(1)
	return ymin

def get_ymax(line):
	find = re.compile('ymax:(?:)(.*)(?<=)xmax')
	ymax = re.search(find, line).group(1)
	return ymax


def main():
	lst_of_groundtruth_files = os.listdir(GROUND_TRUTH_BOUNDING_BOX_DIR)
	for network_file in os.listdir(NETWORK_BOUNDING_BOX_DIR):
		if network_file in lst_of_groundtruth_files:
			network_file_path = os.path.join(NETWORK_BOUNDING_BOX_DIR, network_file)
			GT_file_path = os.path.join(GROUND_TRUTH_BOUNDING_BOX_DIR, network_file)
			compare_files(network_file_path, GT_file_path)
		else:
			print('Will not compute iou or precision/recall on file %s, no GT file exist' % (network_file))	

if __name__ == '__main__':
  	main()

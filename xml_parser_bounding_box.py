from lxml import etree
from lxml.etree import tostring
import os

GROUND_TRUTH_XML_FILE_DIR = '/home/xmreality/Documents/Object_detection_rcnn/test_images'

def xml_parser(xml_file,saving_file):
	tree = etree.parse(xml_file)
	root = tree.getroot()
	filename = os.path.splitext(os.path.basename(xml_file))[0]
	for child in root.iter():
		if child.tag.startswith('obj'):
			for grandchild in child:
				if grandchild.tag == 'name':
					label = grandchild.text
				if grandchild.tag == 'bndbox':
					for attrib in grandchild:
						if attrib.tag == 'xmin':
							xmin = attrib.text	

						if attrib.tag == 'ymin':
							ymin = attrib.text	
							
						if attrib.tag == 'xmax':
							xmax = attrib.text	
						
						if attrib.tag == 'ymax':
							ymax = attrib.text			
					string = "image_name:%s label:%s ymin:%s xmin:%s ymax:%s xmax:%s" % (filename, label, ymin, xmin, ymax, xmax)	
					saving_file.write(string)
					saving_file.write('\n')

"image_name:%s label:%s ymin:%s xmin:%s ymax:%s xmax:%s "

for file in os.listdir(GROUND_TRUTH_XML_FILE_DIR):
	if file.endswith('.xml'):
		GT_filename_path = GROUND_TRUTH_XML_FILE_DIR + '/groundtruth/' + os.path.splitext(os.path.basename(file))[0] + '.txt'
		writing_file = open(GT_filename_path,'w')
		file_full_path = os.path.join(GROUND_TRUTH_XML_FILE_DIR, file)
		xml_parser(os.path.abspath(file_full_path), writing_file)	

		writing_file.close()
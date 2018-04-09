import sys, os
from lxml import etree
def main(sys):
	input_folder = sys.argv[1]
	input_folder = os.path.abspath(input_folder)
	for filename in os.listdir(input_folder):
		filename_full = os.path.join(input_folder, filename)
		for obj in etree.parse(filename_full).getroot().findall('object'):
			if (obj.find('name').text != 'car') and (obj.find('name').text != 'handel') and \
				(obj.find('name').text != 'eStop') and (obj.find('name').text != 'cabel Protector') \
				 and (obj.find('name').text != 'turnKnob'):
				print(filename)

	print('looked through all files')			


if __name__ == '__main__':
	main(sys)
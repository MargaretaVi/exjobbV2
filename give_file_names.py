import os, sys, glob

def main(sys):
	input_folder = sys.argv[1]
	dst_name = sys.argv[2]

	all_images_in_dir = glob.glob(os.path.abspath(input_folder)  + '/*.jpeg')
	textfile = open(dst_name, "w+")
	for f in all_images_in_dir:
		textfile.write(os.path.splitext(os.path.basename(f))[0])
		textfile.write('\n')
	textfile.close()	

if __name__ == '__main__':
	main(sys)
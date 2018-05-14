import pandas as pd
import matplotlib.pyplot as plt
import os, sys, re ,pdb

def main(sys):	
	INPUT_FOLDER = os.path.abspath(sys.argv[1])
	OUTPUT_FOLDER = os.path.abspath(sys.argv[2])
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)
	lst_of_csv_files = os.listdir(INPUT_FOLDER)
	for file in lst_of_csv_files:
		if file.endswith('.csv'):
			filepath = INPUT_FOLDER + '/' + file
			(title, x_axis_label, y_axis_label, save_file_name,legend) = labeling_figure(filepath)

			headers = ['Wall time', 'Step', 'Value']
			df = pd.read_csv(filepath, skiprows=1,names=headers)
			x = df['Step']
			y = df['Value']

			fig = plt.figure()
			plt.plot(x,y,label=legend)
			plt.title(title)
			plt.xlabel(x_axis_label)
			plt.ylabel(y_axis_label)
			plt.legend()
			fig.savefig(OUTPUT_FOLDER + '/' + save_file_name, format='eps', dpi =1200)
			plt.close()

def parse_legend(filepath):
	if 'evaluation' in filepath:
		legend = 'Evaluation'
	elif 'training' in filepath:
		legend = "Training"
	elif 'testing' in filepath: 
		legend = "Testing"	
	return legend	

def labeling_figure(filepath):
	x_axis_label='Steps'
	legend = parse_legend(filepath)
	category = ""
	if 'loss' in filepath:
		y_axis_label = 'Loss'
		if "classification" in filepath:
			title = 'Classification loss'
			category = 'classification'
		elif "localization" in filepath:
			title = 'Localization loss'
			category = "localization"
		elif "regularization" in filepath:
			title = 'Regularization loss'
			category = 'regularization'
		elif "Total" in filepath:	
			title = 'Total loss'
			category = 'total'
		elif "clone" in filepath:
			title = 'Clone loss'
			category = 'clone'
		elif "objectness" in filepath:
			title = 'Objectness loss'
			category = 'objectness'		
	if "Category" in filepath:
		title = 'Intersection over union 0.5'
		y_axis_label = "Average Precision"	
		if "cabel" in filepath:
			title = title + ': Cabel protector'
			category = "IOU_Cabel_Protector"
		elif "car" in filepath:
			title = title + ': Car'
			category = "IOU_car"
		elif "eStop" in filepath:
			title = title + ': Button'
			category = "IOU_Button"
		elif "Handel" in filepath:
			title = title + ': Handel'
			category = "IOU_Handel.eps"
		elif "turn" in filepath:
			title = title + ': Turn knob'
			category = "IOU_turn_knob"
	if "Precision" in filepath:
		title = "Mean Average precision, 0.5 IOU"	
		y_axis_label = "mean average precision"
		category = "mean_average_precision"
	if category is "":
		pdb.set_trace()
	save_file_name = legend + '_' + category + '.eps'	
	return(title, x_axis_label, y_axis_label, save_file_name,legend)

def parsing_title(filepath):
	filename = os.path.basename(filepath)
	graph_title_regex = 'tag-(.*)\.csv'
	m = re.search(graph_title_regex, filename).group(1)
	return m


if __name__ == '__main__':
	main(sys)
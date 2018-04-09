import pandas as pd
import pdb
import matplotlib.pyplot as plt


#FILEPATH = '/home/xmreality/Downloads/run_train_.-tag-Loss_BoxClassifierLoss_mul_3_1.csv'
#FILEPATH = '/home/xmreality/Downloads/run_train_.-tag-Loss_RPNLoss_mul_3_1.csv'
FILEPATH = '/home/xmreality/Downloads/run_eval_.-tag-PerformanceByCategory_mAP@0.8IOU_Handel.csv'
FOLDER_PATH = '/home/xmreality/Documents/exjobb/Plots/ResNet/'
if "eval" in FILEPATH:
	title = 'Handel, 0.8IOU'
	x_axis_label='Steps'
	y_axis_label = 'mean Average Precision'
	save_file_name = title + '.png'
	headers = ['Wall time', 'Step', 'Value']



df = pd.read_csv(FILEPATH, skiprows=1,names=headers)
x = df['Step']
y = df['Value']

fig = plt.figure()
plt.plot(x,y)
plt.title(title)
plt.xlabel(x_axis_label)
plt.ylabel(y_axis_label)
plt.show()
fig.savefig(save_file_name)
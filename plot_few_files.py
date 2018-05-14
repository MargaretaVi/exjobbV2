import pandas as pd
import matplotlib.pyplot as plt
import os, sys, re , pdb


#Classification loss
file1 = '/home/xmreality/Desktop/Results_network/Faster_rcnn_inception_v2/batch_size_1/loss/csv/run_testing_.-tag-Losses_Loss_BoxClassifierLoss_classification_loss.csv'
file2 = '/home/xmreality/Desktop/Results_network/Faster_rcnn_inception_v2/batch_size_24/loss/csv/run_testing_.-tag-Losses_Loss_BoxClassifierLoss_classification_loss.csv'
#first run batch size 24
file3 = '/home/xmreality/Desktop/Results_network/SSD_inception/run1/loss/csv/run_testing_.-tag-Losses_Loss_classification_loss.csv'
file4 = '/home/xmreality/Desktop/Results_network/SSD_inception/batch_size_35/loss/csv/run_testing_.-tag-Losses_Loss_classification_loss.csv'
file5 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/run1/loss/csv/run_testing_.-tag-Losses_Loss_classification_loss.csv'
file6 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/24k_eval_on_same_batch/loss/csv/run_testing_.-tag-Losses_Loss_classification_loss.csv'
file7 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/24k-eval-on-old-batch/loss/csv/run_testing_.-tag-Losses_Loss_classification_loss.csv'
"""
#Localization loss
file1 = '/home/xmreality/Desktop/Results_network/Faster_rcnn_inception_v2/batch_size_1/loss/csv/run_testing_.-tag-Losses_Loss_BoxClassifierLoss_localization_loss.csv'
file2 = '/home/xmreality/Desktop/Results_network/Faster_rcnn_inception_v2/batch_size_24/loss/csv/run_testing_.-tag-Losses_Loss_BoxClassifierLoss_localization_loss.csv'
#first run batch size 24
file3 = '/home/xmreality/Desktop/Results_network/SSD_inception/run1/loss/csv/run_testing_.-tag-Losses_Loss_localization_loss.csv'
file4 = '/home/xmreality/Desktop/Results_network/SSD_inception/batch_size_35/loss/csv/run_testing_.-tag-Losses_Loss_localization_loss.csv'
file5 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/run1/loss/csv/run_testing_.-tag-Losses_Loss_localization_loss.csv'
file6 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/24k_eval_on_same_batch/loss/csv/run_testing_.-tag-Losses_Loss_localization_loss.csv'
file7 = '/home/xmreality/Desktop/Results_network/SSD_mobilenet/24k-eval-on-old-batch/loss/csv/run_testing_.-tag-Losses_Loss_localization_loss.csv'
"""
headers = ['Wall time', 'Step', 'Value']
df1 = pd.read_csv(file1, skiprows=1,names=headers)
x1 = df1['Step']
y1 = df1['Value']

df2 = pd.read_csv(file2, skiprows=1,names=headers)
x2 = df2['Step']
y2 = df2['Value']

df3 = pd.read_csv(file3, skiprows=1,names=headers)
x3 = df3['Step']
y3 = df3['Value']

df4 = pd.read_csv(file4, skiprows=1,names=headers)
x4 = df4['Step']
y4 = df4['Value']

df5 = pd.read_csv(file5, skiprows=1,names=headers)
x5 = df5['Step']
y5 = df5['Value']

df6 = pd.read_csv(file6, skiprows=1,names=headers)
x6 = df6['Step']
y6 = df6['Value']

df7 = pd.read_csv(file7, skiprows=1,names=headers)
x7 = df7['Step']
y7 = df7['Value']

fig = plt.figure()

plt.plot(x1,y1, 'b',label='Faster R-CNN + Inception, batch size 1')
plt.plot(x2,y2, 'r-',label='Faster R-CNN + Inception, batch size 24')
plt.plot(x3,y3, 'g',label='SSD + Inception, batch size 24')
plt.plot(x4,y4, 'y',label='SSD + Inception, batch size 35')
plt.plot(x5,y5, 'c-',label='SSD + MobileNet, batch size 24')
plt.plot(x6,y6, 'm',label='SSD + MobileNet, batch size 24, 24k training evaluation on dataset B')
plt.plot(x7,y7, 'k-',label='SSD + MobileNet, batch size 24, 24k training evaluation on dataset A')

#plt.title('Mean Average Precision')
#plt.title('Classification Loss')
plt.title('Localization Loss')

plt.xlabel('Step')

plt.ylabel('Loss')
#plt.ylabel('mAP')

plt.legend(prop={'size': 6})
plt.show()
save_file_name = '/home/xmreality/Desktop/Results_network/All/classification_loss.eps'

fig.savefig(save_file_name, format='eps', dpi=1200)
import tensorflow as tf

def create_graph(modelFullPath):
	with tf.gfile.FastGFile(modelFullPath,'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def, name='')

GRAPH_DIR = "/home/xmreality/Documents/exjobb/test/output_graph.pb"
create_graph(GRAPH_DIR)		

for op in tf.get_default_graph().get_operations():
	print(op.values, '\n')
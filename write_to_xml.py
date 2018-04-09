import xml.etree.cElementTree as ET

annotation = ET.Element("annontation")
ET.SubElement(annotation, "folder").text = "folder"
ET.SubElement(annotation, "filename").text = "fname"
ET.SubElement(annotation, "path").text = "saving_image_path"
source = ET.SubElement(annotation, "source")
ET.SubElement(source, "database").text = "Unknown"
size = ET.SubElement(annotation, "size")

ET.SubElement(annotation, "segmented").text = "0"
obj = ET.SubElement(annotation, "object")
ET.SubElement(obj, "xmin").text = "xmin"
ET.SubElement(obj, "ymin").text = "width"
ET.SubElement(obj, "width").text = "width"
ET.SubElement(obj, "height").text = "height"
obj = ET.SubElement(annotation, "object")
ET.SubElement(obj, "xmin").text = "xmin"
ET.SubElement(obj, "ymin").text = "width"
ET.SubElement(obj, "width").text = "width"
ET.SubElement(obj, "height").text = "height"
tree = ET.ElementTree(annotation)
tree.write('/home/xmreality/Desktop/xmlTest.xml')


def add_each_object_to_xml(root, obj):
	obj_node = ET.SubElement(root, "object")

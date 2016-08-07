import xml.etree.ElementTree as ET

def get_item_id(event_file_path):
    tree = ET.parse(event_file_path)
    root = tree.getroot()
    return root[0].attrib["id"]
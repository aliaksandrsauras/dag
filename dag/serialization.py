import xml.etree.ElementTree as ET


def deserialize(path):
    nodes = []
    edges = []

    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        if child.tag == "node":
            pair = (child.attrib["id"], child.attrib.get("operator"))
            nodes.append(pair)
        elif child.tag == "edge":
            pair = (child.attrib["source"], child.attrib["target"])
            edges.append(pair)

    return nodes, edges

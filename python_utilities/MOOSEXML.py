import xml.etree.ElementTree as ET

def readMOOSEXML(filename):
  tree = ET.parse(filename)
  root = tree.getroot()
  data = dict()
  for timestep_elem in root:
    for vector_elem in timestep_elem:
      vpp = vector_elem.attrib['object']
      vector_name = vector_elem.attrib['name']
      if vpp not in data:
        data[vpp] = dict()
      if vector_name not in data[vpp]:
        data[vpp][vector_name] = []
      data[vpp][vector_name].append([float(elem) for elem in vector_elem.text.split()])
  return data

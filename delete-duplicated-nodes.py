# author : eocampos
# license: GPL V2 or later.

from lxml import etree
from sys import argv, exit

if len(argv) != 2:
	print " Usage: " + argv[0] + " <osm file>\n Modified version will be sent to stdout."
	exit(1)

name = argv[1]
root = etree.parse(name)

nodes_by_coord = {}
nodes_by_id = {}
ways = []

for element in root.iter("node"):
	# Deletes duplicated nodes using a dictionary. 
        lat = element.attrib["lat"]
        lon = element.attrib["lon"]
        id  = element.attrib["id"]
	nodes_by_coord[lat+":"+lon] = element
	# Remember the original list for further use.
	nodes_by_id[id] = element

for element in root.iter("way"):
	for child in element.iter("nd"):
		id = child.attrib["ref"]
		lat = nodes_by_id[id].attrib["lat"]
		lon = nodes_by_id[id].attrib["lon"]
		# Get the unique reference to this coordinate and update it
		child.attrib["ref"] = nodes_by_coord[lat+":"+lon].attrib["id"]
	ways.append(element)

# Build .osm file
osm = etree.Element("osm", version="0.5")
osm.text = '\n  '
for element in nodes_by_coord.values():
	osm.append(element)

for element in ways:
	osm.append(element)

print(etree.tostring(osm, pretty_print=True))


import csv
import tempfile
from qgis.core import QgsVectorLayer, QgsProject, QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer, QgsSimpleMarkerSymbolLayerBase

import os

#current_directory = os.getcwd()
os.chdir('D:\\PROG\\gb-diploma-gis')
#print(current_directory)

# Get the temp directory
temp_dir = tempfile.gettempdir()

# Create a new vector layer
vl = QgsVectorLayer("Point?crs=epsg:4326", "markers", "memory")

# Get the data provider
pr = vl.dataProvider()

# Add fields
pr.addAttributes([QgsField("name", QVariant.String)])

# Update the layer's fields
vl.updateFields()

# Open the csv file
with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    # Iterate over the rows
    for row in reader:
        # Create a new feature
        feat = QgsFeature()
        # Set the geometry
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(row[5]), float(row[4]))))
        # Set the attributes
        feat.setAttributes([row[2]])
        # Add the feature to the layer
        pr.addFeatures([feat])

# Update the layer's extent when new features have been added
vl.updateExtents()

# Create a marker symbol
symbol = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': 'red', 'size': '4'})

# Apply the symbol to the layer
vl.renderer().setSymbol(symbol)

# Add the layer to the map
QgsProject.instance().addMapLayer(vl)

# Print the results
print('Markers added to the map')

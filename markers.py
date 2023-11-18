import csv
import tempfile
from qgis.core import QgsVectorLayer, QgsProject, QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsPointXY
from qgis.core import QgsVectorFileWriter
from qgis.utils import iface
import os

os.chdir('D:\\PROG\\gb-diploma-gis\\mosdata')
# Set the path where you want to save the shapefile
output_shapefile_path = 'D:\\PROG\\gb-diploma-gis\\mosdata\\markers.shp'

# Initialize a QGIS project
project = QgsProject.instance()
project.setTitle('Marker Layer Project')

# Create a new vector layer
vl = QgsVectorLayer("Point?crs=epsg:4326", "markers", "memory")

if not vl.isValid():
    print("Layer creation failed.")
else:
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
    project.addMapLayer(vl)

    # Save the vector layer to a shapefile
    #QgsVectorFileWriter.writeAsVectorFormat(vl, output_shapefile_path, "UTF-8", None, "ESRI Shapefile")
    # Save the vector layer to a shapefile
    QgsVectorFileWriter.writeAsVectorFormat(vl, output_shapefile_path, 'UTF-8', vl.crs(), 'ESRI Shapefile')


    # Set the project's CRS to match the layer's CRS
    project.setCrs(vl.crs())

    # Load the layer into the QGIS interface
    iface.addVectorLayer(output_shapefile_path, 'Markers', 'ogr')

    # Print the results
    print(f"Markers added to the map and saved to {output_shapefile_path}")

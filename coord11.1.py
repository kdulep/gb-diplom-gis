from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsVectorLayer, QgsPointXY, QgsSpatialIndex, QgsGeometry, QgsField, QgsMarkerSymbol, QgsRendererCategory
from qgis.core import QgsProject, QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer, QgsSimpleMarkerSymbolLayerBase
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtCore import Qt, QVariant
from qgis.utils import iface
import os

def myaddfeatures(mylayername, myfeats):
    # Create a new vector layer
    vl = QgsVectorLayer("Point?crs=epsg:4326", mylayername, "memory")

    # Get the data provider
    pr = vl.dataProvider()

    # Add attributes dynamically based on the first feature
    for field in myfeats[0].fields():
        pr.addAttributes([field])

    # Update the layer's fields
    vl.updateFields()

    pr.addFeatures(myfeats)
    vl.updateExtents()

    # Create a marker symbol
    symbol = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': 'red', 'size': '4'})

    # Apply the symbol to the layer
    vl.renderer().setSymbol(symbol)

    # Add the layer to the map
    QgsProject.instance().addMapLayer(vl)

    # Print the results
    print(f'Markers added to the map for layer: {mylayername}')

def print_attributes(target_x, target_y):
    os.chdir('D:\\PROG\\gb-diploma-gis\\mosdata')
    geojson_file_path = '710881420-obshchestvennoe.geojson'

    # Load the GeoJSON layer
    layer = QgsVectorLayer(geojson_file_path, 'my_geojson_layer', 'ogr')

    # Check if the layer is valid
    if not layer.isValid():
        print('Error: Unable to load GeoJSON layer')
        return

    # Define the target coordinate
    target_point = QgsPointXY(target_x, target_y)

    # Buffer distance to consider features as 'near' (in layer CRS units)
    buffer_distance = 0.005  # Adjust ...

    # Create a circular buffer around the target point
    buffer_geometry = QgsGeometry.fromPointXY(target_point).buffer(buffer_distance, 30)

    # Use spatial index to efficiently find features within the buffer
    index = QgsSpatialIndex()
    for feature in layer.getFeatures():
        index.insertFeature(feature)

    intersecting_ids = index.intersects(buffer_geometry.boundingBox())
    print(f"Number of points of interest: {len(intersecting_ids)}")

    # List to store features near the target point
    near_features = []

    # Iterate through the features in the layer
    for feature_id in intersecting_ids:
        near_features.append(layer.getFeature(feature_id))

    myaddfeatures("markers_sel", near_features)

    # Print information about near features
    print(f"Features near coordinate {target_point.x()}, {target_point.y()}:")
    for near_feature in near_features:
        #print(f"Feature ID: {near_feature.id()} - Geometry: {near_feature.geometry().asPoint()}")
        attributes = near_feature.attributes()[1]
        phone = attributes['PublicPhone'][0]['PublicPhone']
        textToCopy = f"{attributes['Address']}\t{attributes['Name']}\t{phone}\n"
        with open("clicklog.txt", "a") as myfile:
            myfile.write(textToCopy)

class CoordinateCaptureTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, callback_function):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.canvas = canvas
        self.callback_function = callback_function
        self.ctrl_pressed = False

    def canvasPressEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        self.callback_function(point)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            print("Break key pressed. Exiting.")
            self.deactivate()
            self.canvas.unsetMapTool(self)

def capture_coordinates(clicked_point):
    print(f"Clicked at: {clicked_point.x()}, {clicked_point.y()}")
    print_attributes(clicked_point.x(), clicked_point.y())

# Assuming 'iface' is the QGIS interface object
canvas = iface.mapCanvas()

# Set the map tool to the custom CoordinateCaptureTool
capture_tool = CoordinateCaptureTool(canvas, capture_coordinates)
canvas.setMapTool(capture_tool)

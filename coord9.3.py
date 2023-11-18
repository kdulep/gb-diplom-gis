from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsVectorLayer, QgsPointXY, QgsSpatialIndex, QgsGeometry
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtCore import Qt
from qgis.utils import iface
from PyQt5.QtGui import QClipboard
import os

textToCopy=""
with open("clicklog.txt","w") as myfile:
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
    print_attributes(clicked_point.x(),clicked_point.y())
    #target_x = clicked_point.x()
    #target_y = clicked_point.y()


# Assuming 'iface' is the QGIS interface object
canvas = iface.mapCanvas()

# Set the map tool to the custom CoordinateCaptureTool
capture_tool = CoordinateCaptureTool(canvas, capture_coordinates)
canvas.setMapTool(capture_tool)


def print_attributes(target_x, target_y):

    os.chdir('D:\\PROG\\gb-diploma-gis\\mosdata')
    geojson_file_path = '710881420-obshchestvennoe.geojson'

# Load the GeoJSON layer
    layer = QgsVectorLayer(geojson_file_path, 'my_geojson_layer', 'ogr')

# Check if the layer is valid
    if not layer.isValid():
        print('Error: Unable to load GeoJSON layer')
    else:
        # Define the target coordinate (replace with your actual coordinates)
        # target_y = 55.696427
        # target_x = 37.528471
        target_point = QgsPointXY(target_x, target_y)

    # Buffer distance to consider features as 'near' (in layer CRS units)
        buffer_distance = 0.005  # Adjust as needed

    # Create a circular buffer around the target point
    # The second argument (30) is the number of segments used to approximate the circle
    buffer_geometry = QgsGeometry.fromPointXY(
        target_point).buffer(buffer_distance, 30)

    # Print buffer information for debugging
    # print(f"Buffer Geometry: {buffer_geometry.asWkt()}")

    # Use spatial index to efficiently find features within the buffer
    index = QgsSpatialIndex()
    for feature in layer.getFeatures():
        index.insertFeature(feature)
#        attributes = feature.attributes()
        # Print the attributes (you can modify this part based on your needs)
#       print(f"Feature ID: {feature.id()} - Attributes: {attributes}")

#    print(len(index))
    intersecting_ids = index.intersects(buffer_geometry.boundingBox())
    print(f"Number of points of interest:{len(intersecting_ids)}")

    # List to store features near the target point
    near_features = []

    # Iterate through the features in the layer
    for feature_id in intersecting_ids:
        near_features.append(layer.getFeature(feature_id))

    # Print information about near features
    print(f"Features near coordinate {target_point.x()}, {target_point.y()}:")
    for near_feature in near_features:
        #print(f"Feature ID: {near_feature.id()} - Geometry: {near_feature.geometry().asPoint()}")
        attributes = near_feature.attributes()[1]
        phone=attributes['PublicPhone'][0]['PublicPhone']
        # Print the attributes (you can modify this part based on your needs)
        #print(f"Feature ID: {near_feature.id()} - Attributes: {attributes['Address']}\t{attributes['Name']}\t{phone}")
        #print(f"Feature ID: {near_feature.id()} - Attributes: {attributes}")
        textToCopy=attributes['Address'] +"\t"+ attributes['Name']+"\t"+phone+"\n"
        print(textToCopy)
        with open("clicklog.txt","a") as myfile:
            myfile.write(textToCopy)

# Don't forget to properly exit or remove the layer when done
# QgsApplication.exitQgis()

import urllib.request
import tempfile
from qgis.core import QgsVectorLayer
from qgis.gui import QgsMapCanvas
from qgis.utils import iface

# Download the data
url = 'https://download.bbbike.org/osm/bbbike/Moscow/Moscow.osm.pbf'
temp_dir = tempfile.gettempdir()
temp_file = temp_dir + '/Moscow.osm.pbf'

try:
    response = urllib.request.urlopen(url)
    with open(temp_file, 'wb') as f:
        f.write(response.read())

    # Load the data into QGIS
    layer = QgsVectorLayer(temp_file, 'Moscow Map', 'ogr')
    
    if not layer.isValid():
        print("Layer is not valid. Please check the file or layer settings.")
    else:
        QgsProject.instance().addMapLayer(layer)

        # Zoom to the layer
        canvas = iface.mapCanvas()
        canvas.setExtent(layer.extent())
        canvas.refresh()
except Exception as e:
    print(f"An error occurred: {e}")

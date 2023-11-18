
import urllib.request
import tempfile

# Download the World country polygon
url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)

# Save the file to temp directory
temp_dir = tempfile.gettempdir()
file_name = 'ne_10m_admin_0_countries.zip'
file_path = temp_dir + '/' + file_name
with open(file_path, 'wb') as f:
    f.write(response.read())

# Open the file
iface.addVectorLayer(file_path, 'World Country Polygon', 'ogr')

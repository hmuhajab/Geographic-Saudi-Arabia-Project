#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('brew install osmium-tool')


# In[8]:


#Convert the OSM PBF file to GeoJSON to easdily access and read the data 
get_ipython().system('osmium export gcc-states-latest.osm.pbf -o gcc_states_latest.geojson')

print("OSM data for GCC States has been converted to GeoJSON.")


# In[23]:


import json
from rdflib import Graph, Namespace

# Example Turtle data with prefixes
turtle_data = """
@prefix wkg: <http://example.org/wkg#> .
@prefix wkgs: <http://example.org/wkgs#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix osmn: <http://example.org/osmn#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix sf: <http://www.opengis.net/ont/sf#> .

wkg:10009114596 a wkgs:Clothes ;
    rdfs:label "Al- fooz sports" ;
    wkgs:clothes "sports" ;
    wkgs:nameAr "الفوز للرياضه" ;
    wkgs:osmLink osmn:10009114596 ;
    wkgs:spatialObject wkg:geo10009114596 .

wkg:geo10009114596 a sf:Point ;
    geo:asWKT "Point(57.6242478 23.7531119)"^^geo:wktLiteral .
"""

# Load the RDF graph
g = Graph()
g.parse(data=turtle_data, format="ttl")

# Define the namespaces
WKGS = Namespace("http://example.org/wkgs#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
SF = Namespace("http://www.opengis.net/ont/sf#")

# Prepare the JSON structure
json_data = []

# Example OSM ID to extract
example_osm_id = "10009114596"

# Search for the specific example in the graph
for s in g.subjects(RDFS.label, None):
    osm_id = str(s).split("#")[-1]
    if osm_id != example_osm_id:
        continue

    name = g.value(s, RDFS.label)
    name_ar = g.value(s, WKGS.nameAr)
    type_ = None
    for type_stmt in g.triples((s, None, None)):
        if str(type_stmt[1]) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            type_ = str(type_stmt[2]).split("#")[-1].split("/")[-1]
            break
    osm_link = g.value(s, WKGS.osmLink)
    spatial_object = g.value(s, WKGS.spatialObject)

    # Get the coordinates
    lat = None
    long = None
    if spatial_object:
        wkt = g.value(spatial_object, GEO.asWKT)
        if wkt:
            wkt = str(wkt)
            coordinates = wkt.split("(")[-1].strip(")").split()
            long = float(coordinates[0])  # Correcting the order to (long, lat)
            lat = float(coordinates[1])

    # Add the extracted data to the JSON structure
    json_data.append({
        "OSM_ID": osm_id,
        "name": str(name) if name else None,
        "nameAr": str(name_ar) if name_ar else None,
        "type": type_ if type_ else "None",
        "lat": lat,
        "long": long,
        "within": "",
        "neighbours": []
    })

# Print the JSON data
print(json.dumps(json_data, ensure_ascii=False, indent=4))


# In[25]:


import json
from rdflib import Graph, Namespace

# Load the RDF graph
g = Graph()
g.parse("gcc-states-latest.osm.ttl", format="ttl")

# Define the namespaces
WKGS = Namespace("http://example.org/wkgs#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
SF = Namespace("http://www.opengis.net/ont/sf#")

# Prepare the JSON structure
json_data = []

# Iterate over all subjects with an rdfs:label
for s in g.subjects(RDFS.label, None):
    osm_id = str(s).split("#")[-1]
    name = g.value(s, RDFS.label)

    # Extract the nameAr value
    name_ar = None
    spatial_object = None
    for p, o in g.predicate_objects(s):
        if str(p) == "http://www.worldkg.org/schema/nameAr":
            name_ar = o
        elif str(p) == "http://www.worldkg.org/schema/spatialObject":
            spatial_object = o

    type_ = None
    for type_stmt in g.triples((s, None, None)):
        if str(type_stmt[1]) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            type_ = str(type_stmt[2]).split("#")[-1].split("/")[-1]
            break
    osm_link = g.value(s, WKGS.osmLink)

    # Get the coordinates
    lat = None
    long = None
    if spatial_object:
        wkt = g.value(spatial_object, GEO.asWKT)
        if wkt:
            wkt = str(wkt)
            coordinates = wkt.split("(")[-1].strip(")").split()
            if len(coordinates) >= 2:
                long = float(coordinates[0])  # Correcting the order to (long, lat)
                lat = float(coordinates[1])

    # Add the extracted data to the JSON structure
    json_data.append(
        {
            "OSM_ID": osm_id,
            "name": str(name) if name else None,
            "nameAr": str(name_ar) if name_ar else None,
            "type": type_ if type_ else "None",
            "lat": lat,
            "long": long,
            "within": "",
            "neighbours": [],
        }
    )

# Write the JSON data to a file
with open("Output_SaudiArabia.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("Data has been extracted and written to output.json")


# In[26]:


# remove http://www.worldkg.org/resource/

import json

# Load the JSON data from the file
with open("Output_SaudiArabia.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define the prefix to be removed
prefix = "http://www.worldkg.org/resource/"

# Remove the prefix from the OSM_ID field in each entry
for entry in data:
    if entry["OSM_ID"].startswith(prefix):
        entry["OSM_ID"] = entry["OSM_ID"][len(prefix):]

# Save the modified data back to the JSON file
with open("Output_SaudiArabia_modified.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Prefix has been removed from all OSM_ID fields and the modified data has been saved.")


# In[28]:


# find the parent from GADM Data# (last level)
# Check if the coordinates of each place are within any of the polygons in the second file.
import json
from shapely.geometry import Point, Polygon, MultiPolygon

# Load the JSON files
with open("Output_SaudiArabia_modified.json", "r", encoding="utf-8") as f:
    places = json.load(f)

with open("gadm_2_updated_nearest.json", "r", encoding="utf-8") as f:
    gadm_data = json.load(f)

# Extract polygons from GADM data
gadm_polygons = []
for feature in gadm_data:
    gid = feature['GID']
    polygons = feature['geometry']['coordinates']
    multi_polygon = MultiPolygon([Polygon(polygon[0]) for polygon in polygons])
    gadm_polygons.append((gid, multi_polygon))

# Check each place to determine which polygon it falls within
for place in places:
    point = Point(place["long"], place["lat"])
    place["within"] = ""
    for gid, multi_polygon in gadm_polygons:
        if multi_polygon.contains(point):
            place["within"] = gid
            break

# Save the updated JSON data to a new file
with open("Output_SaudiArabia_within_updated.json", "w", encoding="utf-8") as f:
    json.dump(places, f, ensure_ascii=False, indent=4)

print("Places have been updated with GID values.")



# In[32]:


#plot on map to make sure about the non found parent if it is located in Saudi Arabia or not 
import folium

# Data for the location
location_data = {
    "OSM_ID": "9998216524",
    "name": "الهدهد للشاي",
    "nameAr": None,
    "type": "Cafe",
    "lat": 23.8082314,
    "long": 57.5539181,
    "within": "",
    "neighbours": []
}

# Extract latitude and longitude
latitude = location_data["lat"]
longitude = location_data["long"]
name = location_data["name"]

# Create a map centered around the location
m = folium.Map(location=[latitude, longitude], zoom_start=15)

# Add a marker for the location
folium.Marker([latitude, longitude], popup=name).add_to(m)

# Display the map
m



# In[35]:


#  separate the entries based on whether the "within" field is found or not
import json

# Load the JSON file
with open('Output_SaudiArabia_within_updated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lists to store entries
found_within = []
not_found_within = []

# Separate entries based on the "within" field
for entry in data:
    if entry["within"]:
        found_within.append(entry)
    else:
        not_found_within.append(entry)

# Save the entries to separate JSON files
with open('found_SaudiArabia_OSM.json', 'w', encoding='utf-8') as f:
    json.dump(found_within, f, ensure_ascii=False, indent=4)

with open('not_found_SA_OSM.json', 'w', encoding='utf-8') as f:
    json.dump(not_found_within, f, ensure_ascii=False, indent=4)

# Print the number of entities in each category
print(f"Number of entities with 'within' field: {len(found_within)}")
print(f"Number of entities without 'within' field: {len(not_found_within)}")


# In[37]:


# calculate the S2Grid

#The level parameter in the S2 hierarchy determines the resolution of the cells.
#Level 10: Each cell covers about 200 square kilometers.
#Level 13: Each cell covers about 25 square kilometers. <<Knowehere Gragh
# to capture significant features, such as different parts of a city or populated places 
#(as presented in KnowWhere Graph with points of interest)
#, without splitting the data into too many small.
#Higher Levels: Higher levels correspond to smaller cells, providing higher resolution
import json
from s2sphere import LatLng, CellId

def calculate_s2_cell_data(lat, lon, level=13):
    # Converts the latitude and longitude into the S2 cell hierarchy to represent a point on the Earth's surface.
    latlng = LatLng.from_degrees(lat, lon)
    # The level indicates the cell's resolution, with higher levels corresponding to smaller cells.
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    # Method converts the cell ID to a human-readable token, which is a unique identifier for the S2 cell.
    s2_token = cell_id.to_token()
    s2_cell_id = cell_id.id()  # Get the S2 Cell ID
    return s2_token, s2_cell_id

input_json_file_path = 'found_SaudiArabia_OSM.json'

with open(input_json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

updated_json_data = []

for item in json_data:
    try:
        lat = item["lat"]
        lon = item["long"]

        # Calculate S2 cell token and ID
        s2_cell_token, s2_cell_id = calculate_s2_cell_data(lat, lon)
        
        print(f"For lat: {lat}, lon: {lon}, S2 Cell Token: {s2_cell_token}, S2 Cell ID: {s2_cell_id}")

        # Add the S2 cell token and ID to the item dictionary
        item["s2_cell_token"] = s2_cell_token
        item["s2_cell_id"] = s2_cell_id

        updated_json_data.append(item)
    except Exception as e:
        print(f"Error processing entry with lat: {lat}, lon: {lon}. Error: {e}")
        continue

output_json_file_path = 'found_SaudiArabia_OSM_with_s2tokens.json'

with open(output_json_file_path, 'w', encoding='utf-8') as output_json_file:
    json.dump(updated_json_data, output_json_file, ensure_ascii=False, indent=4)

print("S2 cell tokens and IDs added and JSON data saved to:", output_json_file_path)


# In[38]:


# Calculate the nearest between the grid  
import json
import math

def get_atan2(y, x):
    return math.atan2(y, x)

def compute_bearing(endpoint, startpoint):
    x1 = endpoint['lat']
    y1 = endpoint['long']
    x2 = startpoint['lat']
    y2 = startpoint['long']

    radians = get_atan2((y1 - y2), (x1 - x2))

    compass_reading = radians * (180 / math.pi)

    if compass_reading < 0:
        compass_reading = compass_reading + 360

    coord_names = ["N", "E", "S", "W", "N"]
    coord_index = round(compass_reading / 90)

    return coord_names[coord_index]  # returns the coordinate value

def compute_distance(endpoint, startpoint):
    R = 6373.0
    x1 = math.radians(endpoint['lat'])
    y1 = math.radians(startpoint['lat'])
    x2 = math.radians(endpoint['long'])
    y2 = math.radians(startpoint['long'])

    dlon = y2 - x2
    dlat = y1 - x1
    a = (math.sin(dlat / 2)) ** 2 + math.cos(x1) * math.cos(y1) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest_neighbors(data):
    for region in data:
        lat = region.get('lat', None)
        lon = region.get('long', None)
        if lat is None or lon is None:
            continue
        startpoint = {'lat': float(lat), 'long': float(lon)}
        
        neighbors = {'N': None, 'E': None, 'S': None, 'W': None}
        
        for other_region in data:
            if other_region == region:
                continue
            other_lat = other_region.get('lat', None)
            other_lon = other_region.get('long', None)
            if other_lat is None or other_lon is None:
                continue
            endpoint = {'lat': float(other_lat), 'long': float(other_lon)}
            distance = compute_distance(endpoint, startpoint)
            direction = compute_bearing(endpoint, startpoint)
            
            if neighbors[direction] is None or distance < neighbors[direction]['distance']:
                neighbors[direction] = {'name': other_region['name'], 'distance': distance}
        
        region['neighbours'] = neighbors

# Load the JSON data
input_file = 'found_SaudiArabia_OSM_with_s2tokens.json'
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Find the nearest neighbors for each region
find_nearest_neighbors(data)

# Save the updated data to a new JSON file
output_file = 'found_SaudiArabia_OSM_with_neighbours.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated data with neighbors saved to '{output_file}'")


# In[9]:


#map_s2cell


import json
from s2sphere import LatLng, CellId, Cell
import folium
import webbrowser

def calculate_s2_cell_token(lat, lon, level=13):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    s2_token = cell_id.to_token()
    return s2_token

def calculate_s2_cell_vertices(lat, lon, level=13):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    cell = Cell(cell_id)
    vertices = []
    for i in range(4):
        vertex = LatLng.from_point(cell.get_vertex(i))
        vertices.append((vertex.lat().degrees, vertex.lng().degrees))
    return vertices

# Create a Folium map centered at the first location in the dataset
mymap = folium.Map(location=[23.0130723, 40.4095065], zoom_start=5)  # Adjust to your data's location

# Load your JSON data from the file
with open('found_SaudiArabia_OSM_with_neighbours.json', 'r') as json_file:
    json_data = json.load(json_file)

# Iterate over the JSON data to plot the S2 cells and markers on the map
for item in json_data[:20]:  # Limiting to the first 10 items for testing
    name = item["name"]
    lat = item["lat"]
    lon = item["long"]
    s2_cell_token = calculate_s2_cell_token(lat, lon, level=13)
    
    # Calculate S2 cell vertices and add to the map
    s2_cell_vertices = calculate_s2_cell_vertices(lat, lon, level=13)
    cell_color = 'blue' if item["type"] == "Hamlet" else 'red'
    folium.Polygon(locations=s2_cell_vertices, color=cell_color, fill=True, fill_color=cell_color).add_to(mymap)
    
    # Add a marker with a popup
    popup_text = f"Name: {name}<br>S2 Cell Token: {s2_cell_token}"
    folium.Marker(location=(lat, lon), popup=popup_text, icon=folium.Icon(color=cell_color)).add_to(mymap)

# Save the map to an HTML file
html_file_path = 'map_s2cell_saudi.html'
mymap.save(html_file_path)

# Open the HTML file in a web browser
webbrowser.open(html_file_path)


# In[11]:


#all the json data 

import json
from s2sphere import LatLng, CellId, Cell
import folium
import webbrowser

def calculate_s2_cell_token(lat, lon, level=10):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    s2_token = cell_id.to_token()
    return s2_token

def calculate_s2_cell_vertices(lat, lon, level=10):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    cell = Cell(cell_id)
    vertices = []
    for i in range(4):
        vertex = LatLng.from_point(cell.get_vertex(i))
        vertices.append((vertex.lat().degrees, vertex.lng().degrees))
    return vertices

# Create a Folium map centered at the first location in the dataset
mymap = folium.Map(location=[23.0130723, 40.4095065], zoom_start=5)  # Adjust to your data's location

# Load your JSON data from the file
with open('found_SaudiArabia_OSM_with_neighbours.json', 'r') as json_file:
    json_data = json.load(json_file)

# Iterate over the JSON data to plot the S2 cells and markers on the map
for item in json_data:  # Process all items in the JSON data
    name = item["name"]
    lat = item["lat"]
    lon = item["long"]
    s2_cell_token = calculate_s2_cell_token(lat, lon, level=10)
    
    # Calculate S2 cell vertices and add to the map
    s2_cell_vertices = calculate_s2_cell_vertices(lat, lon, level=10)
    cell_color = 'blue' if item["type"] == "Hamlet" else 'red'
    folium.Polygon(locations=s2_cell_vertices, color=cell_color, fill=True, fill_color=cell_color).add_to(mymap)
    
    # Add a marker with a popup
    popup_text = f"Name: {name}<br>S2 Cell Token: {s2_cell_token}"
    folium.Marker(location=(lat, lon), popup=popup_text, icon=folium.Icon(color=cell_color)).add_to(mymap)

# Save the map to an HTML file
html_file_path = 'map_s2cell_saudi_all.html'
mymap.save(html_file_path)

# Open the HTML file in a web browser
webbrowser.open(html_file_path)


# In[11]:


from rdflib import Graph, Namespace, Literal
from s2sphere import LatLng, CellId, Cell
import folium
import webbrowser

# Function to calculate S2 cell token
def calculate_s2_cell_token(lat, lon, level=13):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    s2_token = cell_id.to_token()
    return s2_token

# Function to calculate S2 cell vertices
def calculate_s2_cell_vertices(lat, lon, level=13):
    latlng = LatLng.from_degrees(lat, lon)
    cell_id = CellId.from_lat_lng(latlng).parent(level)
    cell = Cell(cell_id)
    vertices = []
    for i in range(4):
        vertex = LatLng.from_point(cell.get_vertex(i))
        vertices.append((vertex.lat().degrees, vertex.lng().degrees))
    return vertices

# Define the namespaces used in your ontology
EX = Namespace("http://www.semanticweb.org/hn/dligs#")

# Load the ontology into an RDFLib graph
g = Graph()
g.parse('SaudiDataModel_S2Grid_updated_Friday.rdf', format='xml')

# List of specific places to plot (as shown in the picture)
places_of_interest = [
    "mohammed_bin_suaad_5",
    "AL_nhadee_2",
    "Munch_Bakery____________118",
    "Applebee_s_4",
    "mohammed_bin_suaad",
    "Mohammadiyah_Village_3",
    "ghazie_alhesane_1",
    "alforn_3",
    "UK_Visa_Application_Center_1",
    "mohammed_bin_suaad_3",
    "Building_20_5",
    "Dunkin___Donuts_50"
]

# Query the ontology for the specific places of interest
query = f"""
PREFIX : <http://www.semanticweb.org/hn/dligs#>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
SELECT ?place ?lat ?long ?type ?s2cellid ?osm_id
WHERE {{
  ?place wgs84:lat ?lat ;
         wgs84:long ?long ;
         :has_Type ?type ;
         :has_S2CellID ?s2cellid ;
         :has_OSMID ?osm_id .
  FILTER ({' || '.join([f"strends(str(?place), '{name}')" for name in places_of_interest])})
}}
"""

results = g.query(query)

# Create a Folium map centered at a general location (adjust to your data's location)
mymap = folium.Map(location=[23.0130723, 40.4095065], zoom_start=5)

# Iterate over the RDF query results to plot the S2 cells and markers on the map
for row in results:
    place_uri = row['place'].toPython()
    name = place_uri.split("#")[-1]  # Extract the local part of the URI as the name
    lat = float(row['lat'])
    lon = float(row['long'])
    place_type = str(row['type'])
    s2cellid = str(row['s2cellid'])
    osm_id = str(row['osm_id'])

    s2_cell_token = calculate_s2_cell_token(lat, lon, level=13)
    
    # Calculate S2 cell vertices and add to the map
    s2_cell_vertices = calculate_s2_cell_vertices(lat, lon, level=13)
    cell_color = 'blue' if place_type == "Hamlet" else 'red'
    folium.Polygon(locations=s2_cell_vertices, color=cell_color, fill=True, fill_color=cell_color).add_to(mymap)
    
    # Add a marker with a popup
    popup_text = f"Name: {name}<br>Type: {place_type}<br>S2 Cell Token: {s2_cell_token}<br>OSM ID: {osm_id}"
    folium.Marker(location=(lat, lon), popup=popup_text, icon=folium.Icon(color=cell_color)).add_to(mymap)

# Save the map to an HTML file
html_file_path = 'map_s2cell_saudi_from_rdf_specific.html'
mymap.save(html_file_path)

# Open the HTML file in a web browser
webbrowser.open(html_file_path)








# Saudi Arabia Linked Data Project: Geographic Data Processing and S2Grid Utilization

## Overview

This project focuses on building comprehensive linked data for Saudi Arabia by integrating and structuring geographic data from multiple sources. The project leverages OpenStreetMap (OSM) data for populated places, utilizes the S2Grid system for efficient querying and spatial analysis, and incorporates the Global Administrative Areas (GADM) database to define the administrative hierarchy of the country. The S2Grid system also helps in observing and tracking changes over time within specific regions. The project is divided into two main parts:
- **Part A**: Integration of data from the Global Administrative Areas (GADM) database.
- **Part B**: Processing and refining OSM data for Saudi Arabia.

## Project Structure

### Part A: Integrating GADM Data

- **GADM Data**: GADM provides detailed boundaries of administrative areas globally. In this project, GADM data is used to establish a hierarchical structure of regions within Saudi Arabia, which serves as a foundational layer for the linked data model.
- **Parent Identification**: The GADM data is used to identify the last-level (most specific) parent region for each entry in the dataset, ensuring that each geographic feature is correctly situated within the Saudi Arabian administrative structure.

### Part B: Processing OSM Data for Saudi Arabia

1. **Downloading and Structuring OSM Data**:
   - **Source**: The OSM data for Saudi Arabia is sourced from **WorldKG**, where it is provided in a structured Turtle (TTL) format `gcc-states-latest.osm.ttl`.
   - **Data Extraction**: The TTL file is processed to extract the following relevant fields:
     - `"OSM_ID"`: Unique identifier for the OSM entity.
     - `"name"`: Name of the place or feature in English.
     - `"nameAr"`: Name of the place or feature in Arabic.
     - `"type"`: Type of the geographic feature (e.g., city, building, park).
     - `"lat"`: Latitude coordinate.
     - `"long"`: Longitude coordinate.
     - `"within"`: The parent geographic region (will be found based on GADM).
     - `"neighbours"`: List of neighboring features.
   - **Output File**: The extracted data is saved into a JSON file named `Output_SaudiArabia_modified.json`.
  
 2. **Identifying the Parent Region Using GADM Data**:
   - **Parent Region Identification**: The script checks if the coordinates of each place are within any of the polygons representing the last level of administrative boundaries in the GADM. This ensures that each place is correctly associated with its respective administrative region within Saudi Arabia.


3. **Filtering and Separating Saudi Arabia Data**:
   - **Separation Based on `within` Field**: Since the initial data includes entries from across the Gulf countries, the script separates entries specific to Saudi Arabia. This is done using GADM data to verify that the `"within"` field corresponds to a Saudi Arabian region.
   - **Statistics**:
     - Number of entities with a `"within"` field: **44,136**
     - Number of entities without a `"within"` field: **80,938**
3. **Calculating the S2Grid**:
   - **S2 Geometry System**: The S2 system converts latitude and longitude coordinates into a hierarchical grid of cells on the Earth's surface.
   - **Level 13 Resolution**:
     - **Level 10**: Cells cover about 200 square kilometers.
     - **Level 13**: Cells cover about 25 square kilometers, providing a fine-grained resolution ideal for capturing significant features within populated places in Saudi Arabia.
     - **Application**: The Level 13 resolution is chosen to fit the requirement of representing the populated place.
     - **Output File**: All the previously extracted attributes, along with the newly calculated s2_cell_id and s2_cell_token, are saved into `found_SaudiArabia_OSM_with_neighbours_updated.json`.



4. **Calculating Proximity and Visualizing Data**:
   - **Nearest Neighbor Calculation**: The script calculates the nearest neighbors within the S2Grid, which aids in understanding spatial relationships between features.
   - **Visualization**: The grid is plotted on a map to verify the spatial accuracy of the S2 cells, ensuring that the linked data correctly represents geographic features.

## How to Run the Script

### Prerequisites

- **Python 3.x**
- **s2sphere**: Install using `pip install s2sphere`.
- **Additional Libraries**: Install any other necessary libraries listed in `requirements.txt`.

### Steps to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hmuhajab/Saudi_Arabia_Linked_Data.git
   cd Saudi_Arabia_Linked_Data

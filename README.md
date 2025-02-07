# Geographic Saudi Arabia Project: GADM

## Overview

This project focuses on building comprehensive linked data for Saudi Arabia by integrating and structuring geographic data from multiple sources. The project leverages geo data for populated places, utilizes the Global Administrative Areas (GADM) database to define the administrative hierarchy of the country. . The project is divided into two main parts:
- **Part A**: Integration of data from the Global Administrative Areas (GADM) database.
- **Part B**: Processing and refining geo data for Saudi Arabia.

## Project Structure



### Part A: Integrating GADM Data

- **GADM Data**: GADM provides detailed boundaries of administrative areas globally. In this project, GADM data is used to define the hierarchical structure of regions within Saudi Arabia, serving as a foundational layer for the linked data model.

1.  **Processing the GADM Data**:
   - **Reading Attributes**: The GADM data is loaded and processed to read the relevant attributes, including the geographic boundaries (polygons) that define each administrative region within Saudi Arabia.
   - **Extracting Latitude and Longitude**: For each polygon representing a geographic region, the script calculates the centroid to determine the latitude and longitude. This centroid serves as a representative point for the entire polygon, simplifying spatial analysis.
   - **Data Extraction**: The script extracts the following key attributes from the GADM data:
     - `"GID"`: The unique identifier for the geographic entity, e.g., `"SAU"`.
     - `"name"`: The name of the region.
     - `"type"`: The type of the geographic entity (e.g., state, province, district).
     - `"lat"`: The latitude of the centroid of the polygon.
     - `"long"`: The longitude of the centroid of the polygon.
     - `"within"`: The identifier of the parent region within the hierarchical structure.
     - `"neighbours"`: A list of neighboring regions.
     - `"geometry"`: The geometry of the polygon, which is the actual boundary data.
   - **Output Structure**: This extracted and structured data is saved in a JSON format, facilitating further analysis and integration with the linked data model.

2. **Finding and Calculating the Nearest Neighbors**:
   For each geographic region, the script identifies the nearest neighboring regions based on spatial proximity. The JSON file is updated with the nearest neighbors for each region.


### Part B: Processing geo Data for Saudi Arabia

1. **Downloading and Structuring OSM Data**:
   - **Source**: The geo data for Saudi Arabia.
   - **Data Extraction**: The TTL file is processed to extract the following relevant fields:
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


4. **Calculating Proximity and Visualizing Data**:
   - **Nearest Neighbor Calculation**: The script calculates the nearest neighbors within the S2Grid, which aids in understanding spatial relationships between features.
   - **Visualization**: The grid is plotted on a map to verify the spatial accuracy of the S2 cells, ensuring that the linked data correctly represents geographic features.

## How to Run the Script

### Prerequisites

- **Python 3.x**
- **Additional Libraries**: Install any other necessary libraries listed in `requirements.txt`.

### Steps to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hmuhajab/Saudi_Arabia_Linked_Data.git
   cd Saudi_Arabia_Linked_Data

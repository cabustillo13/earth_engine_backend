from fastapi import FastAPI
from pydantic import BaseModel
import folium
from starlette.responses import FileResponse
import ee
from dotenv import load_dotenv
from typing import Optional
import os


# Load environment variables from the .env file
load_dotenv()

# Retrieve the Earth Engine project name from the environment variables
ee_project = os.getenv('EE_PROJECT')

# Initialize Earth Engine with the project name
ee.Initialize(project=ee_project)

# FastAPI app
app = FastAPI()

# Define a model for the area of interest and date range
class AoiRequest(BaseModel):
    lat: float
    lon: float
    start_date: Optional[str] = '2024-01-01'
    end_date: Optional[str] = '2025-12-30'


# Endpoint 0: Root
@app.get("/")
async def root():
    return {"message": "Welcome to LESSAT 2024!"}


# Endpoint 1: Generate scatter plot of Red vs NIR
@app.post("/generate-scatter-plot/")
async def generate_scatter_plot(request: AoiRequest):
    aoi = ee.Geometry.Point([request.lon, request.lat])

    # Fetch Landsat 8 TOA images and filter by date and region
    landsat_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
        .filterDate(request.start_date, request.end_date) \
        .filterBounds(aoi)

    # Define a function to sample Red and NIR bands from each image
    def sample_image(image):
        return image.select(['B4', 'B5']).sample(region=aoi, scale=30, numPixels=500)

    # Map the sampling function over the collection
    sampled_images = landsat_collection.map(sample_image)

    # Flatten the sampled points into a single FeatureCollection
    all_samples = sampled_images.flatten()

    # Arrange the samples as a list of lists
    samp_dict = all_samples.reduceColumns(ee.Reducer.toList().repeat(2), ['B4', 'B5'])
    samp_list = ee.List(samp_dict.get('list'))

    # Save server-side ee.List as a client-side Python list
    samp_data = samp_list.getInfo()

    # Generate the scatter plot using matplotlib
    plt.scatter(samp_data[0], samp_data[1], alpha=0.2)
    plt.xlabel('Red (B4)', fontsize=12)
    plt.ylabel('NIR (B5)', fontsize=12)
    plt.title('Red vs. NIR Scatter Plot for Landsat Images')

    # Save the plot
    plot_filename = 'scatter_plot.png'
    plt.savefig(plot_filename)

    # Return the image as a response
    return FileResponse(plot_filename, media_type='image/png')

@app.post("/generate-map/")
async def generate_map(request: AoiRequest):
    aoi = ee.Geometry.Point([request.lon, request.lat])

    # Fetch Landsat 8 TOA images and filter by date and region
    landsat_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
        .filterDate(request.start_date, request.end_date) \
        .filterBounds(aoi)

    # Get the first image in the collection for visualization
    img = landsat_collection.first()

    # Get metadata from the first image
    img_info = img.getInfo()
    properties = img_info.get('properties', {})

    # Extract 5 key metadata items relevant to scientific analysis
    relevant_metadata = {
        'CLOUD_COVER': properties.get('CLOUD_COVER', 'N/A'),
        'SUN_AZIMUTH': properties.get('SUN_AZIMUTH', 'N/A'),
        'SUN_ELEVATION': properties.get('SUN_ELEVATION', 'N/A'),
        'EARTH_SUN_DISTANCE': properties.get('EARTH_SUN_DISTANCE', 'N/A'),
        'SENSOR_ANGLE': properties.get('SENSOR_AZIMUTH', 'N/A')
    }

    # Create a Folium map centered on the AOI
    map_center = [request.lat, request.lon]
    m = folium.Map(location=map_center, zoom_start=10)

    # Function to add Earth Engine image to folium map
    def add_ee_layer(image, vis_params, name):
        map_id_dict = ee.Image(image).getMapId(vis_params)
        folium.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name=name,
            overlay=True,
            control=True
        ).add_to(m)

    # Experimenting with auto-scaling or setting reasonable min/max values
    vis_params = {
        'bands': ['B4', 'B3', 'B2'],  # RGB bands
        'min': 0,  # Adjusted to minimum reflectance values
        'max': 0.3,  # Adjusted for TOA reflectance images
        'gamma': 1.4
    }

    # Add the Landsat image layer to the Folium map
    add_ee_layer(img, vis_params, 'Landsat 8 RGB')

    # Add the AOI to the map
    folium.Marker(location=[request.lat, request.lon], popup='AOI', icon=folium.Icon(color='red')).add_to(m)

    # Add relevant metadata as a popup on the map
    metadata_html = "<b>Landsat 8 Metadata (Scientific Analysis):</b><br>"
    for key, value in relevant_metadata.items():
        metadata_html += f"{key}: {value}<br>"

    metadata_popup = folium.Popup(html=metadata_html, max_width=300)
    folium.Marker(location=map_center, popup=metadata_popup).add_to(m)

    # Add base layers for context with attribution
    folium.TileLayer(
        tiles='Stamen Terrain',
        attr='Map data © OpenStreetMap contributors, CC-BY-SA, Stamen Design',
        name='Stamen Terrain',
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='Stamen Toner',
        attr='Map data © OpenStreetMap contributors, CC-BY-SA, Stamen Design',
        name='Stamen Toner',
        overlay=False,
        control=True
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save the map as an HTML file
    map_filename = "map_with_metadata.html"
    m.save(map_filename)

    # Return the HTML file
    return FileResponse(map_filename, media_type='text/html')


# Run the FastAPI app (use uvicorn in terminal to run the server)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# 🌍 Landsat Data API with FastAPI 🚀

This FastAPI application lets you interact with Google Earth Engine's Landsat data and provides endpoints for visualizing **scatter plots** and generating **maps** for a given area of interest (Mendoza, Argentina by default).

## 🌟 Features

- **Scatter Plot of Red vs. NIR bands** 📊
- **Map Visualization of Landsat Images** 🗺️

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+ 🐍
- Google Earth Engine account 🌐 (and credentials setup)

### 1. Clone the Repository

```bash
git clone https://github.com/cabustillo13/earth_engine_backend.git
cd earth_engine_backend
```

### 2. Install Dependencies

Create a virtual environment and install the required dependencies from `requirements.txt`:

```bash
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
pip install -r requirements.txt
```

### 3. Authenticate with Google Earth Engine 🌐

Before you can use the API, you need to authenticate your Google Earth Engine account.

Run the following command to authenticate:

```bash
earthengine authenticate
```

Alternatively, you can authenticate in Python:

```python
import ee
ee.Authenticate()
```

### 4. Run the FastAPI Application 🚀

Start the FastAPI server using `uvicorn`:

```bash
uvicorn main:app --reload
```

This will start the application at `http://127.0.0.1:8000`.

---

## 🔥 Endpoints

### 1. **Scatter Plot** 📊

Generates a scatter plot for Red vs. NIR bands from Landsat 8 data within the specified date range.

- **URL**: `POST /generate-scatter-plot/`
- **Response**: Number of images in the collection and a generated scatter plot.
- It returns a `media_type='image/png'`

### 2. **Map Visualization** 🗺️

Generates an interactive map of Landsat 8 images for the given Area of Interest (Tokyo by default).

- **URL**: `POST /generate-map/`
- **Response**: Number of images in the collection and a generated map saved as `map.html`.
- It returns a `media_type='text/html'`

---

## 🧪 Testing the API

1. Ensure that the FastAPI server is running:
   ```bash
   uvicorn main:app --reload
   ```

   or

  ```python
   python main.py
   ```

3. Run the client script to make requests to the two endpoints:
   ```bash
   python test.py
   ```

---

## 📂 Project Structure

```bash
├── main.py             # FastAPI application
├── test.py             # Client script to test API
├── requirements.txt    # Required dependencies
└── README.md           # This file! 📄
```

---

## 💡 Troubleshooting

- If you get the error `Please authorize access to your Earth Engine account`, make sure you’ve authenticated your Earth Engine account.
- Ensure that you’ve installed all the necessary libraries from `requirements.txt`.

---

## 🎉 Conclusion

This API makes it easy to access and visualize Landsat data for remote sensing and analysis. With just a couple of endpoints, you can fetch powerful satellite imagery data and visualize it easily!

Feel free to contribute to the project or expand its functionality! Happy coding! 🚀

---

## 📞 Contact

If you have any issues, feel free to reach out via a GitHub issue or send me a message.

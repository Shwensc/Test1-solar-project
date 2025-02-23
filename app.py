from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import os
import io

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# ✅ Set Gemini API Key
API_KEY = "AIzaSyCry2cPNZe-kbVqPLuBsmGEhv-T0V8OWbM"  # Replace with your actual API Key
genai.configure(api_key=API_KEY)

# ✅ Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ Home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ✅ Handle image uploads and make predictions
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded!")

    file = request.files["file"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # ✅ Open image and convert it to Gemini-compatible format
    img = Image.open(filepath)

    # ✅ Convert image to binary data
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG")  # Ensure image is in JPEG format
    img_bytes = img_buffer.getvalue()

    # ✅ Use the correct model: "gemini-1.5-flash"
    model = genai.GenerativeModel("gemini-1.5-flash")

    # ✅ Send **image with a text prompt** to Gemini API
    response = model.generate_content(
        [
            "Analyze this image and identify any faults in the solar panel.",
            {"mime_type": "image/jpeg", "data": img_bytes},  # Correctly formatted image data
        ]
    )

    # ✅ Extract prediction result
    predicted_class = response.text.strip()

    return render_template("result.html", filename=file.filename, prediction=predicted_class)

if __name__ == "__main__":
    app.run(debug=True)

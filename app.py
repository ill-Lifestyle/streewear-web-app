
from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
OUTPUT_FOLDER = "./outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/isolate", methods=["POST"])
def isolate():
    try:
        file = request.files.get("image")
        image_path = None
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

        if image_path and os.path.exists(image_path):
            image = Image.open(image_path).convert("RGBA")
            bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
            diff = ImageChops.difference(image, bg)
            diff = ImageChops.add(diff, diff, 2.0, -100)
            mask = diff.convert("L").point(lambda p: p > 128 and 255)
            isolated_image = Image.composite(image, bg, mask)
            isolated_image = isolated_image.filter(ImageFilter.SMOOTH)

            output_path = os.path.join(OUTPUT_FOLDER, "isolated_design.png")
            isolated_image.save(output_path, "PNG")

            img_io = BytesIO()
            isolated_image.save(img_io, "PNG")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/png")
        else:
            return jsonify({"error": "No valid image uploaded for isolation."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/download_isolated", methods=["GET"])
def download_isolated():
    try:
        output_path = os.path.join(OUTPUT_FOLDER, "isolated_design.png")
        if os.path.exists(output_path):
            return send_file(output_path, mimetype="image/png", as_attachment=True, download_name="isolated_design.png")
        else:
            return jsonify({"error": "No isolated design available for download."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

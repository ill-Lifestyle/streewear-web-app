
from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
FONTS_FOLDER = "./fonts"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", fonts=os.listdir(FONTS_FOLDER))

@app.route("/preview", methods=["POST"])
def preview():
    try:
        # Get form data
        text = request.form.get("text", "Your Text Here")
        text_color = request.form.get("color", "black")
        font_choice = request.form.get("font", "Poppins-Regular.ttf")
        file = request.files.get("image")
        image_path = None
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

        # Debugging log
        print(f"Image uploaded to: {image_path}")

        # Create canvas
        canvas_width, canvas_height = 1000, 1200
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(canvas)

        # Add image if uploaded
        if image_path and os.path.exists(image_path):
            uploaded_image = Image.open(image_path).convert("RGBA")
            uploaded_image.thumbnail((800, 600))
            img_x = (canvas_width - uploaded_image.width) // 2
            img_y = 200
            canvas.paste(uploaded_image, (img_x, img_y), uploaded_image)
        else:
            print("No valid image found.")

        # Add text
        font_path = os.path.join(FONTS_FOLDER, font_choice)
        try:
            font = ImageFont.truetype(font_path, 50)
        except:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (canvas_width - text_width) // 2
        text_y = 850
        draw.text((text_x, text_y), text, fill=text_color, font=font)

        # Convert to bytes
        img_io = BytesIO()
        canvas.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

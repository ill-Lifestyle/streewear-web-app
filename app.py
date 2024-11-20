
from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
OUTPUT_FOLDER = "./outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the quote from the form
        quote = request.form.get("quote", "Your Text Here")

        # Handle file upload
        file = request.files.get("image")
        image_path = None
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

        # Create the streetwear design
        output_path = os.path.join(OUTPUT_FOLDER, "streetwear_mockup.jpg")
        create_streetwear_design(image_path, quote, output_path)

        return send_file(output_path, mimetype="image/jpeg", as_attachment=True)

    return render_template("index.html")

def create_streetwear_design(image_path=None, quote="Your Text Here", output_name="streetwear_mockup.jpg"):
    canvas_width, canvas_height = 1000, 1200
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    if image_path and os.path.exists(image_path):
        input_image = Image.open(image_path)
        input_image.thumbnail((800, 600))
        img_x = (canvas_width - input_image.width) // 2
        img_y = 200
        canvas.paste(input_image, (img_x, img_y))

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        font = ImageFont.truetype(font_path, 40)
    except:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), quote, font=font)
    quote_width = text_bbox[2] - text_bbox[0]
    quote_height = text_bbox[3] - text_bbox[1]
    quote_x = (canvas_width - quote_width) // 2
    quote_y = 850 if image_path else (canvas_height - quote_height) // 2
    draw.text((quote_x, quote_y), quote, fill="black", font=font)

    canvas.save(output_name)


if __name__ == "__main__":
    app.run(debug=True)

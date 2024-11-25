
from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
OUTPUT_FOLDER = "./outputs"
FONTS_FOLDER = "./fonts"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle upload and design refinement
        quote = request.form.get("quote", "Your Text Here")
        text_color = request.form.get("color", "black")
        font_choice = request.form.get("font", "Poppins-Regular.ttf")
        file = request.files.get("image")
        image_path = None
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

        # Output path for design
        output_path = os.path.join(OUTPUT_FOLDER, "refined_design.png")
        create_refined_design(image_path, quote, output_path, text_color, font_choice)
        return send_file(output_path, mimetype="image/png", as_attachment=True)

    return render_template("index.html", fonts=os.listdir(FONTS_FOLDER))

def create_refined_design(image_path, quote, output_name, text_color, font_choice):
    canvas_width, canvas_height = 1000, 1200
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(canvas)

    # Load image if uploaded
    if image_path and os.path.exists(image_path):
        input_image = Image.open(image_path).convert("RGBA")
        input_image.thumbnail((800, 600))
        img_x = (canvas_width - input_image.width) // 2
        img_y = 200
        canvas.paste(input_image, (img_x, img_y), input_image)

    # Add text
    font_path = os.path.join(FONTS_FOLDER, font_choice)
    try:
        font = ImageFont.truetype(font_path, 50)
    except Exception as e:
        print(f"Error loading font: {e}")
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), quote, font=font)
    quote_width = text_bbox[2] - text_bbox[0]
    quote_x = (canvas_width - quote_width) // 2
    quote_y = 850
    draw.text((quote_x, quote_y), quote, fill=text_color, font=font)

    canvas.save(output_name, "PNG")

if __name__ == "__main__":
    app.run(debug=True)

from io import BytesIO
from PIL import Image
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/upscale_image", methods=["POST"])
def upscale_image():
    scale = int(request.args.get("scale", 2))
    image_file = request.files["image"]
    image_binary = BytesIO(image_file.read())
    image = Image.open(image_binary)
    image_format = image.format
    if image_format not in ["JPEG", "PNG"]:
        return "Unsupported image format", 400
    image = image.resize((image.width * scale, image.height * scale), Image.LANCZOS)
    result = BytesIO()
    image.save(result, image_format, quality=95)
    result.seek(0)
    response = make_response(result.read())
    response.headers["Content-Type"] = f"image/{image_format.lower()}"
    response.headers["Content-Disposition"] = f"attachment; filename=output.{image_format.lower()}"
    return response

if __name__ == "__main__":
    app.run()

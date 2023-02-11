from io import BytesIO
from PIL import Image
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/upscale_image", methods=["POST"])
def upscale_image():
    scale = int(request.args.get("scale", 2))
    image_binary = BytesIO(request.files["image"].read())
    image = Image.open(image_binary)
    image = image.resize((image.width * scale, image.height * scale), Image.LANCZOS)
    result = BytesIO()
    image.save(result, "JPEG", quality=95)
    result.seek(0)
    response = make_response(result.read())
    response.headers["Content-Type"] = "image/jpeg"
    response.headers["Content-Disposition"] = "attachment; filename=output.jpeg"
    return response

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, jsonify
import qrcode
import os

app = Flask(__name__)

# Folder to store generated QR codes
QR_FOLDER = "static/qrcodes"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"success": False, "error": "Invalid URL"}), 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(QR_FOLDER, "qrcode.png")
    qr_img.save(qr_path)

    return jsonify({"success": True, "qr_code": "/" + qr_path})

if __name__ == "__main__":
    app.run(debug=True)

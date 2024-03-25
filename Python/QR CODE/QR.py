import qrcode

# Text or data to encode into the QR code
data = "https://github.com/itxxBilal"

# Create a QR code instance
qr = qrcode.QRCode(version=1, box_size=10, border=4)

# Add data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
qr_image.save("qr_code.png")

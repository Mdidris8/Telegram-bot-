import base64

qr_base64 = """iVBORw0KGgoAAAANSUhEUgAAAZoAAAGaAQAAAAAefbjOAAAC+ElEQVR4nO2cTW6jQBBG3zdYyrK5QY5C32COFOVIcwM4ig8QCZaRsGoW/QP2bCaKBjxQvbBowZMLuVRV/XW1ZXx5DD++zoBDDjnkkEMOOXRMSHlcUJwkRW6SWpDam2AqD8RdzHNoe6gzM7MR7P3VDGjM..."""  # (maine shorten kiya hai)

# File banake save karo
with open("qr.png", "wb") as f:
    f.write(base64.b64decode(qr_base64))

print("✅ QR code saved as qr.png")
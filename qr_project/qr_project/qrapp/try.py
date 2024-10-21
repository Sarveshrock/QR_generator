import qrcode
from PIL import Image

# Function to create a QR code with an image embedded
# Function to create a QR code with an image embedded
def create_qr_with_image(data, image_path, output_path, qr_size=(400, 400), logo_size=(100, 100)):
    # Step 1: Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction to allow for an image in the middle
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Step 2: Create the QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize(qr_size, Image.Resampling.LANCZOS)  # Resize the QR code
    
    # Step 3: Open the image you want to embed and ensure it has an alpha channel
    logo = Image.open(image_path)
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')  # Ensure the logo has an alpha (transparency) channel
    
    logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

    # Step 4: Calculate positioning for the logo (centered)
    pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
    
    # Step 5: Paste the logo onto the QR code, handling transparency
    qr_img.paste(logo, pos, mask=logo)  # Use logo as its own mask for transparency
    
    # Step 6: Save the final QR code
    qr_img.save(output_path)
    print(f"QR code saved to {output_path}")

# Usage
data = "https://example.com"  # Data you want the QR code to encode
image_path = "C:/Users/ADMIN/Desktop/Cansprite/Qr generator/Hyundai-Creta-180120241405.jpg"  # Path to your image file
output_path = "artistic_qr_code.png"  # Where to save the final QR code

# Generate the QR code with the embedded image
create_qr_with_image(data, image_path, output_path)

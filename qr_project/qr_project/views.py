from django.shortcuts import render
import os
from django.conf import settings
from .qrapp.amazingqr.amzqr import run  # Adjust the import path
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'home.html')

def generate_qr(request):
    if request.method == "POST":
        # Get the URL/text provided by the user
        words = request.POST.get('words')

        if not words:
            return render(request, 'generate_qr.html', {'error': 'Please provide text or a URL for the QR code.'})

        # Get additional parameters
        contrast = float(request.POST.get('contrast', 1.5))
        brightness = float(request.POST.get('brightness', 1.6))
        colorized = 'colorized' in request.POST

        # Handle the uploaded image
        picture_path = None  # Default to None in case no image is uploaded
        output_extension = 'png'  # Default output format

        if 'picture' in request.FILES:
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            picture_name = fs.save(picture.name, picture)
            picture_path = fs.path(picture_name)

            # Check if the uploaded image is a .gif and adjust output accordingly
            if picture_name.lower().endswith('.gif'):
                output_extension = 'gif'
        
        # Set up the output directory and filename
        output_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Output file path
        output_name = f'artistic_qr.{output_extension}'  # Use the filename directly without the subdirectory
        output_path = os.path.join(output_directory, output_name)  # Save path within the qr_codes directory

        try:
            # Generate the artistic QR code using the amzqr library
            ver, ecl, qr_name = run(
                words=words,                # The user-provided URL or text
                version=5,                  # QR version
                level='H',                  # Error correction level
                picture=picture_path,        # Path to the uploaded image
                colorized=colorized,         # Whether to colorize the QR code
                contrast=contrast,           # Contrast for blending
                brightness=brightness,       # Brightness for blending
                save_name=output_path        # Where to save the QR code
            )

            # Check if the output file was successfully created
            if os.path.exists(output_path):
                return render(request, 'result.html', {'qr_code': f'{settings.MEDIA_URL}qr_codes/{output_name}'})
            else:
                return render(request, 'generate_qr.html', {'error': 'QR Code generation failed.'})
        except Exception as e:
            print(f"Error: {str(e)}")
            return render(request, 'generate_qr.html', {'error': str(e)})

    return render(request, 'generate_qr.html')

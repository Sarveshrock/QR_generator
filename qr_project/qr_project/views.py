from django.shortcuts import render
import os
from django.conf import settings
from .qrapp.amazingqr.amzqr import run  # Adjust the import path
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from qr_project.forms import SignUpForm, LoginForm
from .models import QRCode

# Existing home and generate_qr views...

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use your custom SignUpForm
        if form.is_valid():  # Check if the form is valid
            form.save()  # This should save the user to the database
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Authenticate the user after sign-up
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home page after successful signup
        else:
            print(form.errors)  # Print form errors if form validation fails (for debugging)
    else:
        form = SignUpForm()  # Render an empty form for GET request

    return render(request, 'signup.html', {'form': form})  # Render the signup template


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or any other page after signin
            else:
                return render(request, 'signin.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})



def home(request):
    return render(request, 'home.html')

'''def generate_qr(request):
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

    return render(request, 'generate_qr.html')'''

'''@login_required
def generate_qr(request):
    if request.method == "POST":
        words = request.POST.get('words')

        if not words:
            return render(request, 'generate_qr.html', {'error': 'Please provide text or a URL for the QR code.'})

        contrast = float(request.POST.get('contrast', 1.5))
        brightness = float(request.POST.get('brightness', 1.6))
        colorized = 'colorized' in request.POST

        picture_path = None
        output_extension = 'png'

        if 'picture' in request.FILES:
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            picture_name = fs.save(picture.name, picture)
            picture_path = fs.path(picture_name)

            if picture_name.lower().endswith('.gif'):
                output_extension = 'gif'

        # Ensure the output directory exists
        output_directory = os.path.join(settings.MEDIA_ROOT, 'Qr_Project')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Generate the QR code
        output_name = f'artistic_qr.{output_extension}'
        output_path = os.path.join(output_directory, output_name)

        try:
            ver, ecl, qr_name = run(
                words=words,
                version=5,
                level='H',
                picture=picture_path,
                colorized=colorized,
                contrast=contrast,
                brightness=brightness,
                save_name=output_path
            )

            if os.path.exists(output_path):
                # Save the QR code details in the database
                qr_instance = QRCode(
                    user=request.user,  # Associate the QR code with the logged-in user
                    words=words,
                    qr_code_image=f'Qr codes/{output_name}'  # Relative path to the saved image
                )
                qr_instance.save()

                # Pass the generated QR code image to the result template
                return render(request, 'result.html', {'qr_code': f'{settings.MEDIA_URL}Qr codes/{output_name}'})
            else:
                return render(request, 'generate_qr.html', {'error': 'QR Code generation failed.'})
        except Exception as e:
            print(f"Error: {str(e)}")
            return render(request, 'generate_qr.html', {'error': str(e)})

    return render(request, 'generate_qr.html')


@login_required
def qr_list(request):
    qrcodes = QRCode.objects.filter(user=request.user)  # Only fetch QR codes generated by the logged-in user
    return render(request, 'qr_list.html', {'Qr codes': qrcodes})'''

def generate_qr(request):
    if request.method == "POST":
        # Get the URL/text provided by the user
        words = request.POST.get('words')

        if not words:
            return render(request, 'generate_qr.html', {'error': 'Please provide text or a URL for the QR code.'})

        # Get additional parameters with validation
        try:
            contrast = float(request.POST.get('contrast', 1.5))
        except ValueError:
            contrast = 1.5

        try:
            brightness = float(request.POST.get('brightness', 1.6))
        except ValueError:
            brightness = 1.6

        colorized = 'colorized' in request.POST

        # Handle the uploaded image
        picture_path = None  # Default to None in case no image is uploaded
        output_extension = 'png'  # Default output format

        if 'picture' in request.FILES:
            picture = request.FILES['picture']
            allowed_extensions = {'.jpg', '.png', '.bmp', '.gif'}

            # Validate the uploaded image format
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in allowed_extensions:
                return render(request, 'generate_qr.html', {'error': f'Invalid image format! Please upload one of {allowed_extensions}.'})

            # Save the image
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
        output_name = f'artistic_qr.{output_extension}'
        output_path = os.path.join(output_directory, output_name)

        try:
            # Generate the artistic QR code using the amzqr library
            ver, ecl, qr_name = run(
                words=words,                # The user-provided URL or text
                version=5,                  # QR version
                level='H',                  # Error correction level
                picture=picture_path,        # Path to the uploaded image (can be None)
                colorized=colorized,         # Whether to colorize the QR code
                contrast=contrast,           # Contrast for blending
                brightness=brightness,       # Brightness for blending
                save_name=output_path        # Where to save the QR code
            )

            # Check if the output file was successfully created
            if os.path.exists(output_path):
                # Save the QR code details to the database
                qr_instance = QRCode(words=words)
                with open(output_path, 'rb') as f:
                    qr_instance.qr_code_image.save(output_name, File(f), save=True)

                # Send the QR code image URL to the template
                qr_code_url = fs.url(f'qr_codes/{output_name}')
                return render(request, 'generate_qr.html', {'qr_code_url': qr_code_url})

            # If something went wrong with QR code generation, show an error message
            return render(request, 'generate_qr.html', {'error': 'QR Code generation failed.'})

        except Exception as e:
            print(f"Error: {str(e)}")
            return render(request, 'generate_qr.html', {'error': f'Error generating QR code: {str(e)}'})

    # Render the page for GET requests
    return render(request, 'generate_qr.html')

def customize_qr_template(request):
    return render(request, 'Customize.html')
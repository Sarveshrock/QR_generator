from django.shortcuts import render
import os
import qrcode
from django.conf import settings
from .qrapp.amazingqr.amzqr import run  # Adjust the import path
from django.core.files.storage import FileSystemStorage
from django.core.files import File
#from segno import SvgSquareDrawer, SvgCircleDrawer, SvgPathSquareDrawer, SvgPathCircleDrawer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from qr_project.forms import SignUpForm, LoginForm
from .models import QRCode

# Existing home and generate_qr views...

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates the User instance

            # The UserProfile will automatically be created via the post_save signal.
            # You can access and update it like this:
            user_profile = user.userprofile
            user_profile.organization_name = form.cleaned_data.get('organization_name')
            user_profile.employee_id = form.cleaned_data.get('employee_id')
            user_profile.save()

            # Authenticate and log the user in
            login(request, user)
            return redirect('home')  # Redirect to the home page
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

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



def dashboard(request):
    if request.user.is_authenticated:
        # Fetch QR codes generated by the logged-in user
        qr_codes = QRCode.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'qr_codes': qr_codes})
    else:
        return redirect('signin')  # Redirect to signin page if the user is not authenticated

def home(request):
    return render(request, 'home.html')


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

def get_float_from_request(request, field_name, default=1.0):
    try:
        return float(request.POST.get(field_name, default))
    except ValueError:
        return default


# Handle image uploads and validation
def handle_image_upload(request, allowed_extensions):
    picture_path = None
    output_extension = 'png'

    if 'picture' in request.FILES:
        picture = request.FILES['picture']
        ext = os.path.splitext(picture.name)[1].lower()

        if ext in allowed_extensions:
            fs = FileSystemStorage()
            picture_name = fs.save(picture.name, picture)
            picture_path = fs.path(picture_name)

            # Adjust output extension if .gif is uploaded
            if picture_name.lower().endswith('.gif'):
                output_extension = 'gif'
        else:
            raise ValueError(f'Invalid image format! Allowed formats are: {allowed_extensions}.')

    return picture_path, output_extension


# View to handle QR code customization
def customize_qr(request):
    if request.method == 'POST':
        # Retrieve user inputs
        data = request.POST.get('data', 'Default data')
        foreground_color = request.POST.get('foreground_color', '#000000')
        background_color = request.POST.get('background_color', '#FFFFFF')

        # Generate colored QR code
        qr_code_img = generate_colored_qr_code(data, foreground_color, background_color)

        # Save the image to a temporary location to render in the template
        fs = FileSystemStorage()
        img_path = os.path.join(fs.location, 'colored_qr_code.png')
        qr_code_img.save(img_path)

        return render(request, 'Customize.html', {
            'qr_code_url': fs.url('colored_qr_code.png'),
        })

    return render(request, 'Customize.html', {'qr_code_url': None})


# Helper function to generate a colored QR code
def generate_colored_qr_code(data, foreground_color, background_color):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=foreground_color, back_color=background_color).convert("RGB")
    return img


# View to generate QR with advanced customization options
def generate_qr_custom(request):
    if request.method == "POST":
        words = request.POST.get('words')
        style = request.POST.get('style')
        embedded_image = request.FILES.get('embedded_image')

        if not words:
            return render(request, 'generate_qr.html', {'error': 'Please provide text or a URL for the QR code.'})

        # Create the QR code with style if selected
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(words)

        img = None  # Initialize QR code image variable
        if style == "rounded":
            img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
        elif style == "gradient":
            img = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
        elif style == "embedded" and embedded_image:
            fs = FileSystemStorage()
            temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', embedded_image.name)
            fs.save(temp_image_path, embedded_image)
            img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=temp_image_path)
            os.remove(temp_image_path)  # Clean up temporary image

        # Fallback to default style if none is selected
        if img is None:
            img = qr.make_image()

        # Save the QR code image
        qr_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_path, exist_ok=True)
        qr_filename = f"{request.user.username}_qr.png"
        qr_file_path = os.path.join(qr_path, qr_filename)
        img.save(qr_file_path)

        # Save the QR code to the database
        qr_instance = QRCode(user=request.user, words=words)
        with open(qr_file_path, "rb") as f:
            qr_instance.qr_code_image.save(qr_filename, File(f), save=True)

        qr_code_url = FileSystemStorage().url(f'qr_codes/{qr_filename}')
        return render(request, 'Customize.html', {'qr_code_url': qr_code_url})

    return render(request, 'Customize.html')
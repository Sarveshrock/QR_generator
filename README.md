# Amazing-QR

## Overview

**Python QR Code Generator**

Generate *common qr-code*,  *artistic qr-code (black & white or colorized)*,  *animated qr-code (black & white or colorized)*.



## Examples

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs0.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs1.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/qrs2.jpg)

![](https://github.com/x-hw/amazing-qr/blob/master/example/c_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode.gif)

![](https://github.com/x-hw/amazing-qr/blob/master/example/zootopia_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode0.gif)

## Install

```python
# via pip
pip install amzqr
```

## Usage

### Terminal Way  

*(**TIPS**: If you haven't install [**amzqr**](https://pypi.python.org/pypi/amzqr), you should  `python(3) amzqr.py` instead of `amzqr` blow.)*

```sh
# summary
amzqr Words
      [-v {1,2,3,...,40}]
      [-l {L,M,Q,H}]
      [-n output-filename]
      [-d output-directory]
      [-p picture_file]
      [-c]
      [-con contrast]
      [-bri brightness]
```

- see [Common QR-Code](#common-qr-code) for `Words`, `-v`, `-l`, `-n`, `-d`
- see [Artistic QR-Code](#artistic-qr-code) for `-p`, `-c`, `-con`, `-bri`
- see [Animated GIF QR-Code](#animated-gif-qr-code) about GIF

#### Common QR-Code

![](https://github.com/x-hw/amazing-qr/blob/master/example/0.png)

```markdown
#1 Words
amzqr https://github.com
```

* Just input a URL or a sentence, then get your QR-Code named 'qrcode.png' in the current directory.


```markdown
#2 -v, -l
amzqr https://github.com -v 10 -l Q
```

* The **default** size of QR-Code depends both on the numbers of words you input and the level, while the **default** level (Error Correction Level) is **H** (the highest).

* **Customize**: If you want to control the size and the error-correction-level, use the `-v` and `-l` arguments. 

   `-v`  representing the length is from a minimum of **1** to a maximum of **40**. 

   `-l` representing the error correction level is one of **L, M, Q and H**, where L is the lowest level and H is the highest.




```markdown
#3 -n, -d
amzqr https://github.com   -n github_qr.jpg   -d .../paths/
```

* The **default** output-filename is 'qrcode.png', while the **default** output-directory is current directory.

* **Customize**: You can name the output-file and decide the output-directory. **Notice** that if the name is as same as a existing file, the old one will be deleted.

  `-n` representing the output-filename could be in the format one of `.jpg`， `.png` ，`.bmp` ，`.gif` .

  `-d` means directory.


#### Artistic QR-Code

![](https://github.com/x-hw/amazing-qr/blob/master/example/1.png)![](https://github.com/x-hw/amazing-qr/blob/master/example/2.png)


```markdown
#1 -p
amzqr https://github.com -p github.jpg
```

* The `-p` is to combine the QR-Code with the following picture which is in the same directory as the program. The resulting picture is **black and white** by default.


```markdown
#2 -c
amzqr https://github.com -p github.jpg -c
```

* The `-c` is to make the resulting picture **colorized**.



```markdown
#3 -con, -bri
amzqr https://github.com -p github.jpg [-c] -con 1.5 -bri 1.6
```

* The `-con` flag changes the **contrast** of the picture - a low number corresponds to low contrast and a high number to high contrast. **Default: 1.0**.

* The `-bri` flag changes the **brightness** and the parameter values work the same as those for `-con`. **Default: 1.0**.





#### Animated GIF QR-Code

![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode.gif)![](https://github.com/x-hw/amazing-qr/blob/master/example/daftpunktocat-guy_qrcode0.gif)

The only difference from Artistic QR-Code mentioned above is that you should input an image file in the `.gif` format. The you can get your black-and-white or colorful qr-code. Remember that when you use `-n` to customize the output-filename, then the output-filename must end by `.gif`.

### Import Way

```python
from amzqr import amzqr

version, level, qr_name = amzqr.run(
    words,
    version=1,
    level='H',
    picture=None,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name=None,
    save_dir=os.getcwd()
)
```

*details about each parameter are as mentioned [above](#terminal-way)*

```python
# help(amzqr)
Positional parameter
   words: str

Optional parameters
   version: int, from 1 to 40
   level: str, just one of ('L','M','Q','H')
   picutre: str, a filename of a image
   colorized: bool
   constrast: float
   brightness: float
   save_name: str, the output filename like 'example.png'
   save_dir: str, the output directory
```

## Tips

* Use a nearly **square** picture instead of a rectangle one.

* If the size of the picture is large, you should also choose a **rightly** large `-v` instead of using the default one.

* If part of the picture is transparent, the qr code will look like: ![](https://github.com/x-hw/amazing-qr/blob/master/example/aa.png)

  You can change the transparent layer to white, and then it will look like: ![](https://github.com/x-hw/amazing-qr/blob/master/example/a0.png)

## Supported Characters

* Numbers:  `0~9`

* Letters:  `a~z, A~Z`

* Common punctuations:

  ```console
  · , . : ; + - * / \ ~ ! @ # $ % ^ & ` ' = < > [ ] ( ) ? _ { } | and  (space)
  ```

## Environment

- Python 3

# Artistic QR Code Generator

This Django application allows users to generate artistic QR codes. Users can input text or URLs, customize the QR code's appearance, and download the generated codes in various formats.

## Features

- Generate artistic QR codes from user-defined text or URLs.
- Upload images to blend with the QR code.
- Adjust contrast and brightness settings for enhanced visual appeal.
- Download generated QR codes in PNG and GIF formats.
- User-friendly web interface for easy interaction.

## Technologies Used

- Python
- Django
- HTML/CSS
- JavaScript
- Git
- [amazing-qr](https://github.com/x-hw/amazing-qr) (for artistic QR code generation)

## Requirements

- Python 3.6 or higher
- Django 5.x or higher
- Git
- Additional libraries (see `requirements.txt`)

## Installation

### Clone the repository
## Set up a virtual environment

It's recommended to create a virtual environment to manage dependencies.

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## Install dependencies
```bash
pip install -r requirements.txt
```
## Configure the project
## Database Configuration
Set up your database in settings.py according to your preference (SQLite is the default for Django).

## Static and Media Files
Ensure that you have proper configurations for static and media files in settings.py.

```bash
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
## Run Migrations
Apply database migrations to set up the required tables.
```bash
python manage.py migrate
  ```
## Running the Application
To start the Django development server, run:

```bash
python manage.py runserver
```
Access the application in your web browser at http://127.0.0.1:8000/.

## Usage
1. Navigate to the home page.
2. Enter the text or URL you want to convert into a QR code.
3. Optionally, upload an image to blend with the QR code.
4. Adjust the contrast and brightness settings as desired.
5. Click the "Generate QR" button to create the QR code.
6. Download the generated QR code from the results page.





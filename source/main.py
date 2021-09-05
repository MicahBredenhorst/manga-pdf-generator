"""
This is a test application made by Micah Bredenhorst.
This application converts a folder of images into one single pdf.
The general thought behind this application is to have a folder of manga images and convert
them to one pdf for export to the ereader

Because images have rather a large size and ereaders have small memory capacity, there is a downscale option.
In my testing was a downscale factor of 0.6 still quite readable, that is why that is the default.

If you want to have a cover image make sure that this image has a name that is alphabetically the lowest image. 
Covers that are rotated (Width > Height), these will be rotated 90 gedrees. 
If it is just a normal page this will be ignored because it does not fit the criteria.

Example:
    Input directory: ../input/
    Output directory: ../output/
    Output filename: test
    Downscaling 20 images with a factor of 0.6
    Done

Requirements:
    - Pillow (pip)
"""
import os 
import re
from PIL import Image
from math import floor

class ITP:
    images = []
    converted_images = []
    file_directory = os.path.dirname(__file__)
    input_directory = os.path.join(file_directory, "../input/")        
    output_directory = os.path.join(file_directory, "../output/")
    output_filename = "temp.pdf"
    downscale_factor = 1
    hascover = True

    def __init__(self, downscale_factor = 0.6):
        self.input_directory = os.path.join(self.file_directory, input("Input directory: "))
        self.output_directory = os.path.join(self.file_directory, input("Output directory: "))
        self.output_filename = input("Output filename: ") + ".pdf"
        self.downscale_factor = downscale_factor

    def list_directory_content(self):
        self.images = [f for f in os.listdir(self.input_directory)]

    def downscale(self):
        print("Downscaling %d images with a factor of %.2f" % (len(self.converted_images), self.downscale_factor))
        for index, image in enumerate(self.converted_images):
            new_width = floor(image.size[0] * self.downscale_factor)
            new_heigth = floor(image.size[1] * self.downscale_factor)
            self.converted_images[index] = image.resize((new_width, new_heigth))

    def print_sizes(self):
        for image in self.converted_images:
            print("image size: %d %d" %  image.size)

    def load_images(self):
        self.list_directory_content()
        self.images.sort()
        for relative_path in self.images:
            absolute_path = os.path.join(self.input_directory, relative_path)
            image = Image.open(absolute_path)
            conv_img = image.convert('RGB')
            self.converted_images.append(conv_img)

    def rotate_cover(self):
        cover = self.converted_images[0]
        if cover.size[0] > cover.size[1]:
            print("Rotating cover")
            self.converted_images[0] = self.converted_images[0].rotate(-90, expand=1)


    def convert_images_to_pdf(self):
        self.load_images()
        self.downscale()
        if self.hascover:
            self.rotate_cover()    
        self.converted_images[0].save(
            self.output_directory + self.output_filename,
            save_all=True,
            append_images=self.converted_images[1:]
        )
        print("Done")


itp = ITP()
itp.convert_images_to_pdf()

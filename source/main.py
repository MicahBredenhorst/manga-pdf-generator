"""
This is a test application made by Micah Bredenhorst.
This application converts a directory contains directories which contain chapter images into a volume.
This means if you want to create a volume, just create multiple folders which contain all the images for a chapter,
then the output of the program is an pdf volume with those images.

The general thought behind this application is to prepare the pdf for use on an e-reader.

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
    Author: Micah Bredenhorst
    Title: Manga PDF Generator
    Done

Requirements:
    - Pillow (pip)
    - PyPDF2

"""
import os 
from PIL import Image
from math import floor
from PyPDF2 import PdfFileWriter, PdfFileReader

class ITP:
    images = []
    converted_images = []
    file_directory = os.path.dirname(__file__)
    base_input_directory = os.path.join(file_directory, "../input/")        
    output_directory = os.path.join(file_directory, "../output/")
    output_filename = "temp.pdf"
    downscale_factor = 0.6
    current_input_directory = ""
    hascover = True

    author = "Unknown Author"
    title = output_filename


    def __init__(self, downscale_factor = 0.6):
        self.downscale_factor = downscale_factor
        
        # File information input
        self.base_input_directory = os.path.join(self.file_directory, input("Input directory: "))
        self.output_directory = os.path.join(self.file_directory, input("Output directory: "))
        self.output_filename = input("Output filename: ") + ".pdf"
        self.author = input("Author: ")
        self.title = input("Title: ")

        self.load_all_iamges_of_all_chapters()
        self.downscale()
        self.convert_images_to_pdf()
        self.set_author()

    def load_all_iamges_of_all_chapters(self):
        for chapter in self.list_sorted_directories():
            self.current_input_directory = chapter
            imagesPaths = self.list_directory_content()
            self.load_images(imagesPaths)

    def set_author(self):
        path = os.path.join(self.output_directory, self.output_filename)
        with open(path, 'rb') as pdf:
            reader = PdfFileReader(pdf)
            writer = PdfFileWriter()

            # Read metadata
            writer.appendPagesFromReader(reader)
            metadata = reader.getDocumentInfo()
            writer.addMetadata(metadata)

            # Set Author and Title
            writer.addMetadata({
                '/Author': self.author,
                '/Title': self.title
            })

            with open(path, 'ab') as pdf_out:
                writer.write(pdf_out)


    def list_directory_content(self):
        return [f for f in os.listdir(self.current_input_directory)]

    def list_sorted_directories(self):
        unsorted_directories = [ f.path for f in os.scandir(self.base_input_directory) if f.is_dir() ]
        unsorted_directories.sort()
        return unsorted_directories

    def downscale(self):
        print("Downscaling %d images with a factor of %.2f" % (len(self.converted_images), self.downscale_factor))
        for index, image in enumerate(self.converted_images):
            new_width = floor(image.size[0] * self.downscale_factor)
            new_heigth = floor(image.size[1] * self.downscale_factor)
            self.converted_images[index] = image.resize((new_width, new_heigth))

    def print_sizes(self):
        for image in self.converted_images:
            print("image size: %d %d" %  image.size)

    def load_images(self, imagePaths):
        imagePaths.sort()
        for relative_path in imagePaths:
            absolute_path = os.path.join(self.current_input_directory, relative_path)
            image = Image.open(absolute_path)
            conv_img = image.convert('RGB')
            self.converted_images.append(conv_img)

    def rotate_cover(self):
        cover = self.converted_images[0]
        if cover.size[0] > cover.size[1]:
            print("Rotating cover")
            self.converted_images[0] = self.converted_images[0].rotate(-90, expand=1)

    def convert_images_to_pdf(self):
        if self.hascover:
            self.rotate_cover()    
        self.converted_images[0].save(
            self.output_directory + self.output_filename,
            save_all=True,
            append_images=self.converted_images[1:]
        )
        print("Done")


itp = ITP()

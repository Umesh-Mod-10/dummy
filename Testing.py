## Extracting each page individually:
# import os
# from pdf2image import convert_from_path
# from PIL import Image

# def convert_pdf_to_images(pdf_path, output_dir):
#     """
#     Converts a PDF into images, saving each page as a separate image file.

#     Args:
#         pdf_path (str): Path to the input PDF file.
#         output_dir (str): Directory to save the output images.

#     Returns:
#         List[str]: Paths to the saved image files.
#     """
#     # Ensure the output directory exists
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     try:
#         # Convert PDF pages to images
#         pages = convert_from_path(pdf_path, dpi=300)
#     except Exception as e:
#         raise RuntimeError(f"Error converting PDF to images: {e}")

#     image_paths = []
#     for i, page in enumerate(pages):
#         # Save each page as a JPEG image
#         output_path = os.path.join(output_dir, f"page_{i+1}.jpg")
#         page.save(output_path, "JPEG")
#         image_paths.append(output_path)
#         print(f"Saved: {output_path}")

#     return image_paths

# # Example usage
# if __name__ == "__main__":
#     pdf_path = input("Please provide the path for the document: ").strip().strip('"').strip("'")  # Replace with your PDF file path
#     output_dir = r"C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Extracted"  # Replace with your desired output directory
#     try:
#         saved_images = convert_pdf_to_images(pdf_path, output_dir)
#         print(f"Successfully saved {len(saved_images)} images.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

## Can extract images from only one page:
# import os
# from PyPDF2 import PdfReader
# import fitz  # PyMuPDF
# from PIL import Image
# import io

# # Function to convert PDF page to images using PyMuPDF
# def pdf_page_to_images(pdf_path, page_num):
#     doc = fitz.open(pdf_path)
#     page = doc[page_num]
#     images = []
#     for img_index in range(len(page.get_images(full=True))):
#         xref = page.get_images(full=True)[img_index][0]
#         img = doc.extract_image(xref)
#         img_bytes = img["image"]
#         images.append(Image.open(io.BytesIO(img_bytes)))
#     return images

# # Function to crop image to its best shape
# def crop_best_shape(image):
#     # Find the non-transparent bounding box
#     bbox = image.getbbox()
#     if bbox:
#         return image.crop(bbox)
#     return image

# # Main process
# pdf_path = input("Please provide the path for the document: ").strip().strip('"').strip("'")
# output_dir = "C:\\Users\\umesh\\OneDrive\\Desktop\\DigitalT3\\Project - MultiModel Knowlege Retrival\\Extracted"

# # Get images from the PDF
# image_page = pdf_page_to_images(pdf_path, 0)  # First page

# # Check for multiple images on the page
# if len(image_page) > 1:
#     # Save each image separately
#     for idx, img in enumerate(image_page):
#         img_path = os.path.join(output_dir, f'extracted_image_{idx}.png')
#         img.save(img_path)
#         print(f"Saved: {img_path}")
# else:
#     # Crop the image to its best shape
#     best_cropped_image = crop_best_shape(image_page[0])
#     img_path = os.path.join(output_dir, 'best_cropped_image.png')
#     best_cropped_image.save(img_path)
#     print(f"Saved: {img_path}")

## Can extract all the images from all pages:
# import os
# from PyPDF2 import PdfReader
# import fitz  # PyMuPDF
# from PIL import Image
# import io

# # Function to convert PDF page to images using PyMuPDF
# def pdf_page_to_images(pdf_path, page_num):
#     doc = fitz.open(pdf_path)
#     page = doc[page_num]
#     images = []
#     for img_index in range(len(page.get_images(full=True))):
#         xref = page.get_images(full=True)[img_index][0]
#         img = doc.extract_image(xref)
#         img_bytes = img["image"]
#         images.append(Image.open(io.BytesIO(img_bytes)))
#     return images

# # Function to crop image to its best shape
# def crop_best_shape(image):
#     # Find the non-transparent bounding box
#     bbox = image.getbbox()
#     if bbox:
#         return image.crop(bbox)
#     return image

# # Main process
# pdf_path = input("Please provide the path for the document: ").strip().strip('"').strip("'")
# output_dir = "C:\\Users\\umesh\\OneDrive\\Desktop\\DigitalT3\\Project - MultiModel Knowlege Retrival\\Extracted"

# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Open the PDF and get the total number of pages
# doc = fitz.open(pdf_path)
# total_pages = len(doc)

# # Process all pages
# for page_num in range(total_pages):
#     images = pdf_page_to_images(pdf_path, page_num)  # Extract images from the current page
    
#     if images:
#         for idx, img in enumerate(images):
#             # Crop each image to its best shape
#             cropped_image = crop_best_shape(img)
#             img_path = os.path.join(output_dir, f'page_{page_num+1}_image_{idx+1}.png')
#             cropped_image.save(img_path)
#             print(f"Saved: {img_path}")
#     else:
#         print(f"No images found on page {page_num+1}")

# print("Image extraction complete.")

## Can render the entire PDF page as an image:
# import os
# import fitz  # PyMuPDF

# # Function to render the entire PDF page as an image
# def render_pdf_pages(pdf_path, output_dir):
#     # Open the PDF document
#     doc = fitz.open(pdf_path)
#     total_pages = len(doc)

#     # Ensure the output directory exists
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Iterate through each page and render it as an image
#     for page_num in range(total_pages):
#         try:
#             page = doc[page_num]
#             pix = page.get_pixmap()  # Render the page
#             img_path = os.path.join(output_dir, f'page_{page_num+1}.png')
#             pix.save(img_path)  # Save the image
#             print(f"Saved rendered page as image: {img_path}")
#         except Exception as e:
#             print(f"Error rendering page {page_num+1}: {e}")

#     print("Page rendering complete.")

# # Main process
# pdf_path = input("Please provide the path for the PDF: ").strip().strip('"').strip("'")
# output_dir = "C:\\Users\\umesh\\OneDrive\\Desktop\\DigitalT3\\Project - MultiModel Knowlege Retrival\\Rendered"

# # Call the function
# render_pdf_pages(pdf_path, output_dir)


import os
import fitz  # PyMuPDF
from PIL import Image
import io

# Function to render and save PDF pages as images
def render_and_save_pdf_pages(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(total_pages):
        try:
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase DPI for better quality
            # Convert Pixmap to RGB to ensure compatibility
            img_data = io.BytesIO()
            pix.pil_save(img_data, format="PNG")
            img_data.seek(0)
            image = Image.open(img_data).convert("RGB")

            img_path = os.path.join(output_dir, f'page_{page_num+1}.png')
            image.save(img_path)  # Save as image
            print(f"Saved rendered page as image: {img_path}")
        except Exception as e:
            print(f"Error rendering page {page_num+1}: {e}")

    print("Page rendering complete.")

# Function to convert JPEG2000 images to JPEG
def convert_jpeg2000_to_jpeg(jpeg2000_image_path, output_path):
    try:
        # Open the JPEG2000 image
        image = Image.open(jpeg2000_image_path)
        # Convert and save as JPEG
        image.convert('RGB').save(output_path, 'JPEG')
        print(f"Image converted and saved as {output_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

# Function to extract images embedded in the PDF
def extract_and_crop_images_from_pdf(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(total_pages):
        page = doc[page_num]
        images = page.get_images(full=True)

        if not images:
            print(f"No images found on page {page_num+1}")
            continue

        for idx, img in enumerate(images):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                pil_image = Image.open(io.BytesIO(img_bytes))

                # Check if image is valid
                if pil_image.format not in ['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF']:
                    print(f"Image from page {page_num+1}, image {idx+1} is not in a valid format: {pil_image.format}")
                    continue

                # Crop to the best shape
                bbox = pil_image.getbbox()
                cropped_image = pil_image.crop(bbox) if bbox else pil_image

                img_path = os.path.join(output_dir, f'page_{page_num+1}_image_{idx+1}.png')
                cropped_image.save(img_path)
                print(f"Saved cropped image: {img_path}")

                # Convert to JPEG2000 and then to JPEG
                jpeg2000_img_path = img_path.replace('.png', '.jpeg2000')
                cropped_image.save(jpeg2000_img_path, 'JPEG2000')

                # Convert JPEG2000 to JPEG
                jpeg_img_path = img_path.replace('.png', '.jpeg')
                convert_jpeg2000_to_jpeg(jpeg2000_img_path, jpeg_img_path)

            except Exception as e:
                print(f"Error saving image from page {page_num+1}, image {idx+1}: {e}")

    print("Image extraction and cropping complete.")

# Main process
pdf_path = input("Please provide the path for the PDF: ").strip().strip('"').strip("'")
rendered_output_dir = "C:\\Users\\umesh\\OneDrive\\Desktop\\DigitalT3\\Project - MultiModel Knowlege Retrival\\Rendered"
extracted_output_dir = "C:\\Users\\umesh\\OneDrive\\Desktop\\DigitalT3\\Project - MultiModel Knowlege Retrival\\Extracted"

# Render pages and extract images
render_and_save_pdf_pages(pdf_path, rendered_output_dir)
extract_and_crop_images_from_pdf(pdf_path, extracted_output_dir)



# # Necessary Libraries for the implementation of the code:
# from PIL import Image
# import os
# import json
# import yaml
# from fpdf import FPDF
# from groq import Groq
# import base64
# import sys
# import logging
# import re
# import unicodedata
# import fitz

# # Configure logging
# logging.basicConfig(
#     format='[%(levelname)s] %(asctime)s - %(message)s',
#     level=logging.INFO,
#     handlers=[logging.StreamHandler()]
# )

# # Load configuration from config.yml:
# def load_config():
#     """
#     Loads and validates the configuration file.
#     """
#     logging.info("Loading the config file...")

#     config_path = "config.yml"
#     try:
#         # Check if the file exists
#         if not os.path.exists(config_path):
#             raise FileNotFoundError(f"The configuration file '{config_path}' does not exist.")
        
#         # Open and load the configuration file
#         with open(config_path, 'r') as file:
#             try:
#                 config = yaml.safe_load(file)
                
#                 # Ensure the configuration is not empty
#                 if config is None:
#                     raise ValueError("The configuration file is empty.")
            
#             except yaml.YAMLError as e:
#                 raise ValueError(f"Error parsing the configuration file: {e}")
            
#         # Perform additional validation if necessary
#         if not isinstance(config, dict):
#             raise ValueError("The configuration file does not contain valid key-value pairs.")

#         # Log the successful loading
#         logging.info("Configuration loaded successfully.")

#         return config

#     except Exception as e:
#         # Handle any other unexpected exceptions
#         logging.error(f"[ERROR] An unexpected error occurred: {e}")
#         sys.exit(1)

# # Initialize the Groq client and Paths for output:
# def setup_llava(config):
#     # API key setup:
#     client = Groq(
#         api_key=config['llama_vision']['login'],
#     )
#     # Paths for output:
#     output_dir = r'C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Digital Catalog\Python BE Model\Catalog_Backend\Outputs'

#     # Define file paths using os.path.join for cross-platform compatibility
#     output_pdf_path = os.path.join(output_dir, "result.pdf")
#     output_json_path = os.path.join(output_dir, "result.json")

#     return client, output_json_path, output_pdf_path

# # Convert images to base64 url to fit into the model
# def image_to_base64_url(image_path):
#     logging.info("Converting image to base64 URL...")
#     try:
#         with open(image_path, "rb") as image_file:
#             encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#         return f"data:image/jpeg;base64,{encoded_string}"
#     except Exception as e:
#         print(f"Error converting image to base64 URL: {e}")
#         return None

# # Cleaning the text:
# def clean_text(text):
#     """
#     Normalize text and replace unsupported characters with ASCII equivalents or spaces.
#     """
#     # Normalize the text to remove special characters
#     text = unicodedata.normalize("NFKD", text)
#     # Replace non-ASCII characters with a space
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     return text

# # Convert images into png format:
# def convert_to_png(image_path):
#     """
#     Ensure the image is in PNG format and save it.
    
#     Args:
#         image_path (str): The path to the input image file.
    
#     Returns:
#         str: The path to the converted PNG image.
#     """
#     try:
#         logging.info("Converting image to PNG format...")

#         # Check if the file exists
#         if not os.path.isfile(image_path):
#             raise FileNotFoundError(f"File not found: {image_path}")

#         # Open and convert the image
#         img = Image.open(image_path)
        
#         # Replace the file extension with '.png', regardless of original extension
#         png_image_path = os.path.splitext(image_path)[0] + "_converted.png"

#         # Save the image in PNG format
#         img.convert("RGBA").save(png_image_path, "PNG")
#         logging.info(f"Image converted to PNG format and saved...")
#         return png_image_path
    
#     except Exception as e:
#         print(f"[ERROR] An unexpected error occurred: {e}")

# #Extracts images from PDF pages using PyMuPDF and saves them to an output directory
# # def extract_images_from_pdf(file_path):
# #     logging.info("Extracting images from PDF...")
# #     # Verify file existence
# #     if not os.path.exists(file_path):
# #         raise FileNotFoundError(f"File not found at path: {file_path}")

# #     # Verify file type
# #     if not file_path.lower().endswith(".pdf"):
# #         raise ValueError("Provided file is not a PDF.")

# #     # Attempt to open the PDF
# #     try:
# #         doc = fitz.open(file_path)
# #     except RuntimeError as e:
# #         raise RuntimeError(f"Failed to open PDF file: {e}")

# #     image_paths = []
# #     output_path = os.path.splitext(file_path)[0]

# #     os.makedirs(output_path, exist_ok=True)

# #     for page_num in range(doc.page_count):
# #         page = doc.load_page(page_num)
# #         images = page.get_images(full=True)

# #         if not images:
# #             print(f"No images found on page {page_num + 1}.")
# #             continue

# #         for img_index, img in enumerate(images):
# #             xref = img[0]
# #             base_image = doc.extract_image(xref)
# #             img_name = f"image_{page_num+1}_{img_index+1}.png"
# #             img_path = os.path.join(output_path, img_name)
# #             image_paths.append(img_path)

# #             with open(img_path, "wb") as img_file:
# #                 img_file.write(base_image["image"])

# #     if not image_paths:
# #         raise ValueError("No images found in the provided PDF.")

# #     return image_paths

# def extract_images_from_pdf(pdf_path):
#     """
#     Converts a PDF into images, saving each page as a separate image file.

#     Args:
#         pdf_path (str): Path to the input PDF file.
#         output_dir (str): Directory to save the output images.

#     Returns:
#         List[str]: Paths to the saved image files.
#     """
#     output_dir = r"C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Extracted"
#     # Ensure the output directory exists
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     try:
#         # Convert PDF pages to images
#         pages = convert_from_path(pdf_path, dpi=300)
#     except Exception as e:
#         raise RuntimeError(f"Error converting PDF to images: {e}")

#     image_paths = []
#     for i, page in enumerate(pages):
#         # Save each page as a JPEG image
#         output_path = os.path.join(output_dir, f"page_{i+1}.jpg")
#         page.save(output_path, "JPEG")
#         image_paths.append(output_path)
#         print(f"Saved: {output_path}")

#     return image_paths

# # Create a PDF Catalog template
# class CatalogPDF(FPDF):
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

#     def add_catalog_entry(self, image_path, title, description):
#         self.add_page()

#         # Further decrease font size for the title
#         self.set_font('Arial', 'B', 10)
#         self.cell(0, 6, title, 0, 1, 'C')  # Reduced height for the title cell
#         self.ln(2)  # Reduced spacing after the title

#         # Convert image and resize for PDF
#         image_path = convert_to_png(image_path)
#         img = Image.open(image_path)
#         img_width, img_height = img.size
#         pdf_width = 100  # Further reduce width to make the image smaller
#         aspect_ratio = img_height / img_width
#         pdf_height = pdf_width * aspect_ratio
#         left_margin = 10
#         pdf_page_width = self.w - left_margin * 2

#         if pdf_width > pdf_page_width:
#             pdf_width = pdf_page_width
#             pdf_height = pdf_width * aspect_ratio

#         self.image(image_path, x=5, y=self.get_y(), w=pdf_width, h=pdf_height)
#         self.ln(pdf_height + 3)  # Reduced spacing after the image

#         # Further decrease font size and line spacing for description
#         self.cell(0, 6, "Description", 0, 1, 'C')  # Reduced height for description title
#         self.set_font('Arial', '', 8)
#         self.multi_cell(0, 5, description)  # Reduced line spacing to 5
#         self.ln(2)  # Reduced spacing at the end

# # Handle image input:
# def load_prompt():
#     logging.info("Loading prompt...")
#     return """
#     Analyze the image and create a professional catalog entry:
#     Title: Identify the object in the image and provide an appropriate title for the catalog.
#     Content:
#     Mention the important specific features and not generic details in a paragraph of 4-5 sentences and then the rest as bulletin points.
#     List technical features of the identified object in short points. No Dimensions necessary.
#     Include software features in concise bullet points, if applicable.
#     Use online sources to research and enhance the details, ensuring accuracy and relevance.
#     Avoid mentioning any specific details about the image itself or its background and phrases of 'note' and paragraph descriptions, etc.    """

# # Implementing the whole image description process:
# def main():

#     logging.info("Starting the program...")
#     # Get input type from the user:
#     input_type = input("Enter 'i' for image input or 'd' for document input or 'b' for both").strip().lower()

#     # Validate input type:
#     if input_type not in ['i', 'd', 'b']:
#         print("Invalid input type. Please enter 'i' for image input or 'd' for document input.")
#         sys.exit()

#     # Get input path from the user:
#     if input_type == 'b':
#         input_path_i = input("Please provide the path for the image: ").strip().strip('"').strip("'")
#         input_path_d = input("Please provide the path for the document: ").strip().strip('"').strip("'")

#     elif input_type == 'i':
#         input_path_i = input("Please provide the path for the image: ").strip().strip('"').strip("'")

#     elif input_type == 'd':
#         input_path_d = input("Please provide the path for the document: ").strip().strip('"').strip("'")

#     if (input_type == 'i' and input_path_i == "") or (input_type == 'd' and input_path_d == "") or (input_type == 'b' and (input_path_i == "" or input_path_d == "")):
#         print("No input path provided. Please provide a valid path.")
#         sys.exit()
    
#     # Getting the basic working functionality:
#     logging.info("Input type: %s", input_type)
#     config = load_config()
#     client, output_json_path, output_pdf_path = setup_llava(config)
#     prompt = load_prompt()
    
#     # Initialize catalog data and PDF
#     logging.info("Loading of dependencies completed...")
#     catalog_data = []
#     pdf_catalog = CatalogPDF()
#     pdf_catalog.set_auto_page_break(auto=True, margin=15)

#     catalog_content = []

#     # Process images
#     logging.info("Processing inputs...")
#     if input_type == 'i' or input_type == 'b':
#         image_base64 = image_to_base64_url(input_path_i)
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}
#             ],
#             model=config['llama_vision']['type'],
#             temperature=config['llama_vision']['temperature'],
#             max_tokens=config['llama_vision']['max_tokens_to_generate'],
#             top_p=config['llama_vision']['top_p'],
#             frequency_penalty=config['llama_vision']['frequency_penalty'],
#             presence_penalty=config['llama_vision']['presence_penalty']
#         )

#         description = chat_completion.choices[0].message.content
#         description = clean_text(description)
#         catalog_content.append(description)
#         title = os.path.basename(input_path_i)
#         pdf_catalog.add_catalog_entry(input_path_i, title, description)
#         catalog_data.append({"image_path": input_path_i, "title": title, "description": description})

#     # Handle document input:
#     if input_type == 'd' or input_type == 'b':
#         image_paths = extract_images_from_pdf(input_path_d)

#         for img_path in image_paths:
#             image_base64 = image_to_base64_url(img_path)

#             chat_completion = client.chat.completions.create(
#                 messages=[
#                     {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}
#                 ],
#                 model=config['llama_vision']['type'],
#                 temperature=config['llama_vision']['temperature'],
#                 max_tokens=config['llama_vision']['max_tokens_to_generate'],
#                 top_p=config['llama_vision']['top_p'],
#                 frequency_penalty=config['llama_vision']['frequency_penalty'],
#                 presence_penalty=config['llama_vision']['presence_penalty']
#             )

#             description = chat_completion.choices[0].message.content
#             description = clean_text(description)
#             catalog_content.append(description)
#             title = os.path.basename(img_path)
#             pdf_catalog.add_catalog_entry(img_path, title, description)
#             catalog_data.append({"image_path": img_path, "title": title, "description": description})

#     # Save outputs
#     logging.info("Saving outputs...")
#     pdf_catalog.output(output_pdf_path)
#     with open(output_json_path, "w") as json_file:
#         json.dump(catalog_data, json_file, indent=4)
    
#     logging.info("Saved outputs as pdf and json files.")
#     return catalog_content

# if __name__ == "__main__":
#     main()

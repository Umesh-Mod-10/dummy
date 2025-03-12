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
# from pdf2image import convert_from_path
# import cv2
# import pytesseract
# import openai
# import time

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
# def setup_llava(config, catalog_name):
#     #API key setup:
#     client = Groq(
#         api_key=config['llama_vision']['login'],
#     )
#     # client = openai.OpenAI(
#     #     api_key=config['llama_vision']['login'],
#     #     base_url="https://api.sambanova.ai/v1",
#     # )
#     # Paths for output:
#     output_dir = r'C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Digital Catalog\Python BE Model\Catalog_Backend\Outputs'

#     # Define file paths using os.path.join for cross-platform compatibility
#     output_pdf_path = os.path.join(output_dir, f"{catalog_name}.pdf")
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

# # Preprocess the image:
# def preprocess_image(image_path):
#     try:
#         # Load image using OpenCV
#         img = cv2.imread(image_path)
#         if img is None:
#             raise ValueError("Image not found or cannot be read.")
        
#         # Convert image to grayscale
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Apply adaptive thresholding to clean up noise and improve contrast
#         processed_img = cv2.adaptiveThreshold(
#             gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
#         )
        
#         # Additional filtering (optional, can remove noise)
#         processed_img = cv2.medianBlur(processed_img, 3)
        
#         return processed_img

#     except Exception as e:
#         print(f"Error during image preprocessing: {e}")
#         return None

# # Extract text from image using Tesseract OCR
# def extract_text_from_image(image_path):
#     try:
#         # Preprocess the image
#         processed_img = preprocess_image(image_path)
#         if processed_img is None:
#             return ""  # Exit if image preprocessing failed

#         # Perform OCR with Tesseract
#         custom_config = r'--oem 3 --psm 6'  # Use Tesseract OCR Engine Mode 3 and Page Segmentation Mode 6
#         extracted_text = pytesseract.image_to_string(processed_img, config=custom_config).strip()

#         # Check if any text was extracted
#         if extracted_text:
#             return extracted_text.replace('\n', ' ')  # Format as paragraph
#         else:
#             print("No text was extracted from the image.")
#             return ""

#     except Exception as e:
#         print(f"Error during OCR processing: {e}")
#         return ""

# # #Extracts images from PDF pages using PyMuPDF and saves them to an output directory
# def extract_images_from_pdf(file_path):

#     logging.info(" Extracting images from PDF...")
#     output_dir = r"C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Extracted"
#     # Ensure the output directory exists
#     image_paths = []
#     os.makedirs(output_dir, exist_ok=True)
#     # Convert PDF pages to images
#     for i in file_path:
#         pages = convert_from_path(i, dpi=300)
#         for i, page in enumerate(pages):
#             # Save each page as a JPEG image
#             output_path = os.path.join(output_dir, f"page_{i+1}.jpg")
#             page.save(output_path, "JPEG")
#             image_paths.append(output_path)
#             logging.info(f"Saved: {output_path}")
#     return image_paths

# # Creating Catalog 
# class CatalogPDF(FPDF):
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 5)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

#     def add_catalog_entry(self, image_path, title, description):
#         self.add_page()

#         # Title
#         self.set_font('Arial', 'B', 5)

#         # Convert image and resize for PDF
#         image_path = convert_to_png(image_path)  # Assuming this function converts and returns path
#         img = Image.open(image_path)
#         img_width, img_height = img.size
#         pdf_image_width = 70  # Width of the image in the PDF
#         aspect_ratio = img_height / img_width
#         pdf_image_height = pdf_image_width * aspect_ratio

#         # Set starting position for both image and description
#         image_x = 10  # X position for image
#         description_x = image_x + pdf_image_width + 5  # X position for description
#         description_y = self.get_y()  # Y position for the description

#         # Image Section
#         self.set_xy(image_x, self.get_y())  # Set starting position for image
#         self.image(image_path, w=pdf_image_width, h=pdf_image_height)  # Insert image

#         # Description Section (Starts at the same X position as the image)
#         self.set_font('Arial', '', 8)  # Reduce font size for description
#         self.set_xy(description_x, image_x)  # Set starting position for description
#         self.multi_cell(0, 3, description)  # Reduced line height to 4 for closer spacing
#         self.ln(pdf_image_height + 2)  # Adjust spacing after image and description
        
# # Load the prompt
# def load_prompt(text):
#     logging.info("Loading prompt...")
#     return f"""
#     Analyze the image and create a professional catalog entry:
#     Title: Identify the object in the image and provide an appropriate title for the catalog.
#     Content:
#     If there is only, extract all the text possible and implement the searches.
#     If any text content present, use OCR and find from the text content and conclude the main object in a more accurate manner.
#     Mention the important specific features and not generic details in a paragraph of 4-5 sentences and then the rest as bulletin points.
#     List technical features of the identified object in short points. No Dimensions necessary.
#     Include software features in concise bullet points, if any.
#     Use online sources to research and enhance the details, ensuring accuracy and relevance.
#     Avoid mentioning any specific details about the image itself or its background and phrases of 'note' and paragraph descriptions, etc. 
#     No need to mention research sources.
# """

# # Implementing the whole image description process:
# def main(catalog_name=None, catalog_topic=None, image_paths=None, pdf_paths=None, include_images_in_catalog=None):

#     logging.info("Starting the program...")

#     # Validate input type:
#     if image_paths != [] and pdf_paths != []:
#         logging.error("Fill the required fields.")
#         return

#     # Get input path from the user:
#     if image_paths != [] and pdf_paths != []:
#         input_path_i = image_paths
#         input_path_d = pdf_paths

#     elif image_paths != []:
#         input_path_i = image_paths
#         input_path_d = []

#     elif pdf_paths != []:
#         input_path_d = pdf_paths
#         input_path_i = []

#     logging.info("Processed the data")
#     config = load_config()
#     client, output_json_path, output_pdf_path = setup_llava(config, catalog_name)
    
#     # Initialize catalog data and PDF
#     logging.info("Loading of dependencies completed...")
#     catalog_data = []
#     pdf_catalog = CatalogPDF()
#     pdf_catalog.set_auto_page_break(auto=True, margin=15)

#     catalog_content = []

#     # Process images
#     logging.info("Processing inputs...")
#     if input_path_i != []:
#         for i in input_path_i:
#             texts = extract_text_from_image(i)
#             image_base64 = image_to_base64_url(i)
#             prompt = load_prompt(texts)
#             logging.info("Implementing the LLM...")
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
#             logging.info("LLM completed...")
#             description = chat_completion.choices[0].message.content
#             description = clean_text(description)
#             catalog_content.append(description)
#             title = os.path.basename(i)
#             pdf_catalog.add_catalog_entry(i, title, description)
#             catalog_data.append({"image_path": i, "title": title, "description": description})
        
#     # Handle document input
#     if input_path_d != []:
#         try:
#             image_paths = extract_images_from_pdf(input_path_d)

#         except RuntimeError as e:
#             logging.error(f"PDF processing failed completely: {e}")
#             print("Unable to process the document. Exiting.")
#             sys.exit()

#         for img_path in image_paths:
#                 texts = extract_text_from_image(img_path)
#                 image_base64 = image_to_base64_url(img_path)
#                 prompt = load_prompt(texts)
#                 chat_completion = client.chat.completions.create(
#                     messages=[
#                         {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}
#                     ],
#                     model=config['llama_vision']['type'],
#                     temperature=config['llama_vision']['temperature'],
#                     max_tokens=config['llama_vision']['max_tokens_to_generate'],
#                     top_p=config['llama_vision']['top_p'],
#                     frequency_penalty=config['llama_vision']['frequency_penalty'],
#                     presence_penalty=config['llama_vision']['presence_penalty']
#                 )

#                 description = chat_completion.choices[0].message.content
#                 description = clean_text(description)
#                 catalog_content.append(description)
#                 title = os.path.basename(img_path)
#                 pdf_catalog.add_catalog_entry(img_path, title, description)
#                 catalog_data.append({"image_path": img_path, "title": title, "description": description})
    
#     # Save outputs
#     logging.info("Saving outputs...")
#     pdf_catalog.output(output_pdf_path)
#     with open(output_json_path, "w") as json_file:
#         json.dump(catalog_data, json_file, indent=4)

#     logging.info("Catalog generation completed.")
#     path = catalog_name
    
#     logging.info("Saved outputs as pdf and json files.")
#     return catalog_content, output_pdf_path, output_json_path, path


# Necessary Libraries for the implementation of the code:
from PIL import Image
import os
import json
import yaml
from fpdf import FPDF
from groq import Groq
import base64
import sys
import logging
import re
import unicodedata
import fitz
from pdf2image import convert_from_path
import cv2
import pytesseract
import openai
import time

# Configure logging
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# Load configuration from config.yml:
def load_config():
    logging.info("Loading the config file...")
    config_path = "config.yml"
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file '{config_path}' does not exist.")
        
        with open(config_path, 'r') as file:
            try:
                config = yaml.safe_load(file)
                if config is None:
                    raise ValueError("The configuration file is empty.")
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing the configuration file: {e}")
            
        if not isinstance(config, dict):
            raise ValueError("The configuration file does not contain valid key-value pairs.")

        logging.info("Configuration loaded successfully.")
        return config

    except Exception as e:
        logging.error(f"[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)

# Initialize the Groq client and Paths for output:
def setup_llava(config, catalog_name):
    client = Groq(
        api_key=config['llama_vision']['login'],
    )
    output_dir = r'C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Digital Catalog\Python BE Model\Catalog_Backend\Outputs'
    output_pdf_path = os.path.join(output_dir, f"{catalog_name}.pdf")
    output_json_path = os.path.join(output_dir, "result.json")
    return client, output_json_path, output_pdf_path

# Convert images to base64 url
def image_to_base64_url(image_path):
    logging.info("Converting image to base64 URL...")
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error converting image to base64 URL: {e}")
        return None

# Clean text
def clean_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text

# Convert to PNG
def convert_to_png(image_path):
    try:
        logging.info("Converting image to PNG format...")
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
        img = Image.open(image_path)
        png_image_path = os.path.splitext(image_path)[0] + "_converted.png"
        img.convert("RGBA").save(png_image_path, "PNG")
        logging.info(f"Image converted to PNG format and saved...")
        return png_image_path
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

# Preprocess image
def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found or cannot be read.")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_img = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        processed_img = cv2.medianBlur(processed_img, 3)
        return processed_img
    except Exception as e:
        print(f"Error during image preprocessing: {e}")
        return None

# # Extract text from image
# def extract_text_from_image(image_path):
#     try:
#         processed_img = preprocess_image(image_path)
#         if processed_img is None:
#             return ""
#         custom_config = r'--oem 3 --psm 6'
#         extracted_text = pytesseract.image_to_string(processed_img, config=custom_config).strip()
#         if extracted_text:
#             return extracted_text.replace('\n', ' ')
#         else:
#             print("No text was extracted from the image.")
#             return ""
#     except Exception as e:
#         print(f"Error during OCR processing: {e}")
#         return ""

# Extract images from PDF
def extract_images_from_pdf(file_path):
    logging.info(" Extracting images from PDF...")
    output_dir = r"C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Extracted"
    image_paths = []
    os.makedirs(output_dir, exist_ok=True)
    for i in file_path:
        pages = convert_from_path(i, dpi=300)
        for i, page in enumerate(pages):
            output_path = os.path.join(output_dir, f"page_{i+1}.jpg")
            page.save(output_path, "JPEG")
            image_paths.append(output_path)
            logging.info(f"Saved: {output_path}")
    return image_paths

# Catalog PDF Class
class CatalogPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 5)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Add catalog entry function
def add_catalog_entry(pdf, image_path, description, includes_image):
    try:
        description = description.replace("**", "")
        image_path = convert_to_png(image_path)
        img = Image.open(image_path)
        img_width, img_height = img.size
        pdf_image_width = 70
        aspect_ratio = img_height / img_width
        pdf_image_height = pdf_image_width * aspect_ratio

        # Get current Y position
        current_y = pdf.get_y()
        
        # Add new page if content won't fit
        if current_y + pdf_image_height > pdf.h - 20:
            pdf.add_page()
            current_y = pdf.get_y()  # Get fresh Y position after new page
            
        if includes_image == 'option1':
            image_x = 10
            description_x = image_x + pdf_image_width + 5
            
            # Place image
            pdf.set_xy(image_x, current_y)
            pdf.image(image_path, w=pdf_image_width, h=pdf_image_height)
            
            # Place description next to image
            pdf.set_font('Arial', '', 8)
            pdf.set_xy(description_x, current_y)
            pdf.multi_cell(0, 3, description)
            
            # Set Y position to bottom of content
            new_y = max(pdf.get_y(), current_y + pdf_image_height + 25)
            new_y += 20

            # Add dividing line
            pdf.line(10, new_y - 10, pdf.w - 10, new_y - 10)

        else:
            # Text-only entry
            pdf.set_font('Arial', '', 8)
            pdf.set_xy(10, current_y)
            pdf.multi_cell(0, 3, description)
            new_y = pdf.get_y() + 5
            
            # Set Y position to bottom of content
            new_y = max(pdf.get_y(), current_y + pdf_image_height + 25)
            new_y += 20

            # Add dividing line
            pdf.line(10, new_y - 10, pdf.w - 10, new_y - 10)

        # Update cursor position for next entry
        pdf.set_y(new_y)

    except Exception as e:
        logging.error(f"Error adding catalog entry: {e}")

# Load prompt
def load_prompt():
    logging.info("Loading prompt...")
    return f"""
    Analyze the image and create a professional catalog entry:
    Title: Identify the object in the image and provide an appropriate title for the catalog.
    Content:
    If there is only, extract all the text possible and implement the searches.
    If any text content present, use OCR and find from the text content and conclude the main object in a more accurate manner.
    Mention the important specific features and not generic details in a paragraph of 4-5 sentences and then the rest as bulletin points.
    List technical features of the identified object in short points. No Dimensions necessary.
    Include software features in concise bullet points, if any.
    Use online sources to research and enhance the details, ensuring accuracy and relevance.
    Avoid mentioning any specific details about the image itself or its background and phrases of 'note' and paragraph descriptions, etc.
    No need to mention research sources.
"""

# Main function
def main(catalog_name=None, catalog_topic=None, image_paths=None, pdf_paths=None, include_images_in_catalog=None):
    logging.info("Starting the program...")
    
    if image_paths != [] and pdf_paths != []:
        logging.error("Fill the required fields.")
        return
    
    if image_paths != [] and pdf_paths != []:
        input_path_i = image_paths
        input_path_d = pdf_paths
    elif image_paths != []:
        input_path_i = image_paths
        input_path_d = []
    elif pdf_paths != []:
        input_path_d = pdf_paths
        input_path_i = []
    
    logging.info("Processed the data")
    config = load_config()
    client, output_json_path, output_pdf_path = setup_llava(config, catalog_name)
    
    logging.info("Loading of dependencies completed...")
    catalog_data = []
    pdf_catalog = CatalogPDF()
    pdf_catalog.add_page()
    pdf_catalog.set_auto_page_break(auto=True, margin=15)
    
    catalog_content = []
    
    logging.info("Processing inputs...")
    if input_path_i != []:
        for i in input_path_i:
            # texts = extract_text_from_image(i)
            image_base64 = image_to_base64_url(i)
            prompt = load_prompt()
            logging.info("Implementing the LLM...")
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}
                ],
                model=config['llama_vision']['type'],
                temperature=config['llama_vision']['temperature'],
                max_tokens=config['llama_vision']['max_tokens_to_generate'],
                top_p=config['llama_vision']['top_p'],
                frequency_penalty=config['llama_vision']['frequency_penalty'],
                presence_penalty=config['llama_vision']['presence_penalty']
            )
            logging.info("LLM completed...")
            description = chat_completion.choices[0].message.content
            description = clean_text(description)
            catalog_content.append(description)
            title = os.path.basename(i)
            add_catalog_entry(pdf_catalog, i, description, include_images_in_catalog)
            catalog_data.append({"image_path": i, "title": title, "description": description})
    
    if input_path_d != []:
        try:
            image_paths = extract_images_from_pdf(input_path_d)
        except RuntimeError as e:
            logging.error(f"PDF processing failed completely: {e}")
            print("Unable to process the document. Exiting.")
            sys.exit()
        
        for img_path in image_paths:
            # texts = extract_text_from_image(img_path)
            image_base64 = image_to_base64_url(img_path)
            prompt = load_prompt()
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}
                ],
                model=config['llama_vision']['type'],
                temperature=config['llama_vision']['temperature'],
                max_tokens=config['llama_vision']['max_tokens_to_generate'],
                top_p=config['llama_vision']['top_p'],
                frequency_penalty=config['llama_vision']['frequency_penalty'],
                presence_penalty=config['llama_vision']['presence_penalty']
            )
            
            description = chat_completion.choices[0].message.content
            description = clean_text(description)
            catalog_content.append(description)
            title = os.path.basename(img_path)
            add_catalog_entry(pdf_catalog, img_path, title, description)
            catalog_data.append({"image_path": img_path, "title": title, "description": description})
    
    logging.info("Saving outputs...")
    pdf_catalog.output(output_pdf_path)
    with open(output_json_path, "w") as json_file:
        json.dump(catalog_data, json_file, indent=4)
    
    logging.info("Catalog generation completed.")
    path = catalog_name
    
    logging.info("Saved outputs as pdf and json files.")
    return catalog_content, output_pdf_path, output_json_path, path, description

import sys
import os
import logging
import re
import yaml
import json
import unicodedata
import Image_Descriptions as img
import Text_Descriptions as txt
from fpdf import FPDF
from datetime import datetime
import openai

# Generate the PDF catalog:
class CatalogPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_catalog_entry(self, description):
        self.add_page()
        self.set_font('Arial', '', 12)
        description = clean_text(description)
        self.multi_cell(0, 10, description)
        self.ln(10)

# Function to load the prompt:
def prompt_load(image=None, text=None, topic=None):
    logging.info("Loading prompt for the combined catalog...")
    if image and text:
        prompt = f"""
# Comprehensive Catalog Template
#### Title Page
# **Separate Page**:
#   - **Catalog Title**: {topic}
#   - **Date**: {datetime.now()}
#   - Design: Full page, large font size, professional layout.
#### Table of Contents
# **Separate Page**:
#   - **List each section title** using a tabular structure, occupy the entire page.
### 3. Introduction
# **Separate Page**:
#   - **Purpose**: Clearly articulate the catalog's intent using insights from {image} and {text}.
#   - **Background**: Tailored context relevant to the topic, no generic information.
### 4. Main Points (Descriptions)
# **Separate Page**:
#   - **Combine {image} and {text} insights** for detailed discussion:
#     - **Overview**: Summary of the section's focus.
#     - **Detailed Descriptions**: Include technical specifics, examples, or data.
#     - **Key Highlights**: Derived from both text and image analysis.
#   - **Images and Captions**: Relevant visuals with meaningful captions.
#   - **Minimum Content**: 5000 words.
### 5. Key Points
# **Separate Page**:
#   - **Extract insights from {image} and {text}** in bullet points:
#     - **Minimum of 10 points** for each topic.
#     - Each point derived from both text and image analysis.
#   - **Minimum Content**: 5000 words.
### 6. Conclusions
# **Separate Page**:
#   - **Recap**: Combined insights and relevance to catalog purpose.
#   - **Call-to-Action**: Clear direction for readers.
### 7. End Page
# **Separate Page**:
#   - **Closing Remarks**: Professional tone.
#   - **Optional**: Disclaimers or legal notes if necessary.
### Notes:
# **Integration of {image} and {text}**: Combine insights from both sources for detailed output.
# **Professional Tone**: Avoid casual or generic wording.
# **Topic Relevance**: All data must be according to the {topic}.
"""
    return prompt.strip()

# Load configuration from config.yml
def load_config():
    """Load the configuration from the YAML file."""
    logging.info("Loading the configuration file...")
    config_path = "config.yml"
    
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file '{config_path}' does not exist.")
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            if not config:
                raise ValueError("The configuration file is empty or invalid.")
        
        logging.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logging.error(f"Error loading the configuration file: {e}")
        sys.exit(1)

# Initialize OpenAI client
def setup():
    logging.info("Setting up the model...")
    try:
        client = openai.OpenAI(
        api_key="649c8e1d-21e0-42e3-8c7f-47536acbe3e7",
        base_url="https://api.sambanova.ai/v1",
    )
        logging.info("Model initialized successfully.")
        return client
    except Exception as e:
        logging.error(f"Error initializing OpenAI client: {e}")
        sys.exit(1)

# Cleaning the text:
def clean_text(text):
    """
    Normalize text and replace unsupported characters with ASCII equivalents or spaces.
    """
    # Normalize the text to remove special characters
    text = unicodedata.normalize("NFKD", text)
    # Replace non-ASCII characters with a space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text

def main(catalog_data):
    # Obtaining the data for the catalog building:
    logging.info("Starting the catalog building process...")

    catalog_name = catalog_data[0]
    catalog_topic = catalog_data[1]
    image_paths = catalog_data[2]
    pdf_paths = catalog_data[3]
    include_images_in_catalog = catalog_data[4]

    # if description != "" and image_paths == [] and pdf_paths == []:
    #     text,  output_pdf_path, output_json_path, file_name  = txt.main(catalog_name, description)
    #     logging.info("Text generated successfully. And Passed to the backend with pdf.")
    #     result = {}
    #     result['text'] = (text)
    #     result['output_pdf_path'] = (output_pdf_path)
    #     result['output_json_path'] = (output_json_path)
    #     result['file_name'] = (file_name)
    #     return result['output_pdf_path'], result['file_name']
    
    if image_paths != [] or pdf_paths != []:
        logging.info("Passing the deatils for catalog...")
        image, output_pdf_path, output_json_path, file_name, description = img.main(catalog_name, catalog_topic, image_paths, pdf_paths, include_images_in_catalog)
        logging.info("Images catalog generated successfully. And Passed to the backend with pdf.")
        result = {}
        result['image'] = (image)
        result['output_pdf_path'] = (output_pdf_path)
        result['output_json_path'] = (output_json_path)
        result['file_name'] = (file_name)
        result['description'] = (description)
        return result['output_pdf_path'], result['file_name'], result['description']

    # Setting up the necessary components:
    logging.info("Setting up the necessary components...")

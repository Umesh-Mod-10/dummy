import os
import openai
from fpdf import FPDF
import yaml
import sys
import logging
import json
import re
import unicodedata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

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

# Loading the prompt:
def load_prompt(content_source, topic):

    logging.info("Loading the prompt...")
    prompt = f"""
    Title: Identify the object described in the {content_source} and work for appropriate title of {topic} for the catalog entry.
Content:
List the technical features of the identified object in concise bullet points.
Include both physical and software features, if applicable, ensuring clarity and brevity.
Use reliable online sources to research and enhance the details, ensuring the information is accurate and relevant.
Note: Do not provide general paragraph answers with content or descriptions—focus strictly on the requested structured format and concise details and phrases of "note:".
    """

    return prompt

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

# Generate the PDF catalog:
class CatalogPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_catalog_entry(self, title, description):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        description = clean_text(description)
        self.multi_cell(0, 10, description)
        self.ln(10)

# Loading the main application:
def main(catalog_file_name, catalog_topic, catalog_name, description):

    logging.info("Starting the application...")
    # Setting up the support files:
    config = load_config()
    client = setup()
    pdf_catalog = CatalogPDF()
    pdf_catalog.set_auto_page_break(auto=True, margin=15)
    catalog_content = []

    content_source_t = description

    if description == "":
        logging.info("No description provided. Using the topic as the description.")
        return
    
    logging.info("Input type processing...")
    prompt = load_prompt(content_source_t, catalog_topic)

    # Generate response using model and parameters:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=config['llm']['select_expert'],
        temperature=config['llm']['temperature'],
        max_tokens=config['llm']['max_tokens_to_generate'],
        top_p=config['llm']['top_p'],
        frequency_penalty=config['llm']['frequency_penalty'],
        presence_penalty=config['llm']['presence_penalty']
    )
    
    # Extract the content from the response:
    content = response.choices[0].message.content
    content = clean_text(response.choices[0].message.content.strip())
    catalog_content.append(content.strip())
    pdf_catalog.add_catalog_entry(catalog_name, content)

    # Set the output file path:
    logging.info("Setting up the output file path...")
    # Paths for output:
    output_dir = r'C:\Users\umesh\OneDrive\Desktop\DigitalT3\Project - MultiModel Knowlege Retrival\Digital Catalog\Python BE Model\Catalog_Backend\Outputs'

    # Define file paths using os.path.join for cross-platform compatibility
    output_pdf_path = os.path.join(output_dir, 'result.pdf')
    output_json_path = os.path.join(output_dir, 'result.json')
    file_name = 'result.pdf'
    logging.info("Output file paths set successfully and ready to saved.")
    # Output the catalog to a PDF file:
    pdf_catalog.output(output_pdf_path)
    # Save the catalog content to a JSON file:
    with open(output_json_path, 'w') as json_file:
        json.dump(catalog_content, json_file, indent=4)

    logging.info("Catalog saved as pdf file and json file.")
    return catalog_content, output_pdf_path, output_json_path, file_name
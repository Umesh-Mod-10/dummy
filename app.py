from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import main
from database.models import (
    create_entry_mongo,
    update_catalog_files_mongo,
    get_latest_catalog_entry_mongo,
    update_catalog_description_mongo,
    update_catalog_details_mongo,
    get_all_buttons_mongo,
    get_button_with_catalog_mongo,
    update_button_catalog_status_mongo
)
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/catalog-button', methods=['POST'])
def catalog_button():
    data = request.get_json()
    try:
        entry_data = {
            'catalogName': '',
            'catalogTopic': '',
            'description': '',
            'image_paths': [],
            'pdf_paths': [],
            'include_images': None,
            'buttonName': data['buttonName'],
            'buttonDesc': data['buttonDesc'],
            'buttonId': data['buttonId'],
            'is_catalog': data.get('isCatalogCreated', False),
            'created_at': datetime.now()
        }
        mongo_id = create_entry_mongo(entry_data)
        return jsonify({
            'status': 'success',
            'message': 'Button data stored successfully',
            'catalog_id': str(mongo_id)
        })
    except Exception as e:
        print(f"Error storing button data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/catalog-details', methods=['POST'])
def catalog_details():
    data = request.get_json()
    try:
        existing_entry = get_latest_catalog_entry_mongo()
        updated_data = {
            'catalogName': data['catalogName'],
            'catalogTopic': data['catalogTopic'],
            'updated_at': datetime.now()
        }
        mongo_id = update_catalog_details_mongo(existing_entry['_id'], updated_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Data updated successfully',
            'catalog_id': str(mongo_id)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/catalog-project', methods=['POST'])
def catalog_form():
    try:
        catalog_entry = get_latest_catalog_entry_mongo()
        
        image_files = []
        pdf_files = []
        index = 0
        
        while f'imageFiles[{index}]' in request.files:
            file = request.files[f'imageFiles[{index}]']
            image_files.append(file)
            index += 1
        
        index = 0
        while f'pdfFiles[{index}]' in request.files:
            file = request.files[f'pdfFiles[{index}]']
            pdf_files.append(file)
            index += 1

        include_images_in_catalog = request.form.get('includeImagesInCatalog')
        image_paths = []
        pdf_paths = []

        for image in image_files:
            if image.filename:
                image.save(os.path.join('uploads/images', image.filename))
                image_paths.append(os.path.join('uploads/images', image.filename))

        for pdf in pdf_files:
            if pdf.filename:
                pdf_path = os.path.join('uploads/pdfs', pdf.filename)
                pdf.save(pdf_path)
                pdf_paths.append(pdf_path)

        update_catalog_files_mongo(
            catalog_entry['_id'],
            image_paths,
            pdf_paths,
            include_images_in_catalog
        )


        catalog_data = [
            catalog_entry['catalog_name'],
            catalog_entry['catalog_topic'],
            image_paths,
            pdf_paths,
            include_images_in_catalog,
        ]

        if image_paths or pdf_paths:
            link, file_name, description = main.main(catalog_data)
            update_catalog_description_mongo(catalog_entry['_id'], description)
            
            return jsonify({
                'status': 'success',
                'message': 'Files uploaded and processed successfully',
                'link': link,
                'file_name': file_name,
                'description': description
            })

        return jsonify({
            'status': 'success',
            'message': 'Data processed successfully'
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/buttons', methods=['GET'])
def get_all_buttons():
    try:
        buttons = get_all_buttons_mongo()
        response_data = []
        
        for button in buttons:
            # Check if description exists and is non-empty
            description = button.get('description', '').strip()
            has_catalog = bool(description)
            
            button_data = {
                'buttonName': button['buttonName'],
                'buttonDesc': button['buttonDesc'],
                'buttonId': button['buttonId'],
                'isCatalogCreated': has_catalog,
                'catalogDetails': {
                    'catalogName': button.get('catalog_name', ''),
                    'catalogTopic': button.get('catalog_topic', ''),
                    'description': description,
                    'imagePaths': button.get('image_paths', []),
                    'pdfPaths': button.get('pdf_paths', [])
                } if has_catalog else None,
                'created_at': button['created_at'].isoformat() if button.get('created_at') else None
            }
            response_data.append(button_data)
            
        print(f"Sending buttons data: {response_data}")  # Debug log
        return jsonify(response_data)
    except Exception as e:
        print(f"Error getting buttons: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/buttons/<button_id>', methods=['GET'])
def get_button_details(button_id):
    try:
        button = get_button_with_catalog_mongo(button_id)
        if not button:
            return jsonify({'status': 'error', 'message': 'Button not found'}), 404
            
        return jsonify({
            'buttonName': button['buttonName'],
            'buttonDesc': button['buttonDesc'],
            'buttonId': button['buttonId'],
            'isCatalogCreated': button['has_catalog'],
            'catalogDetails': {
                'catalogName': button.get('catalog_name', ''),
                'catalogTopic': button.get('catalog_topic', ''),
                'description': button.get('description', ''),
                'imagePaths': button.get('image_paths', []),
                'pdfPaths': button.get('pdf_paths', [])
            } if button['has_catalog'] else None,
            'created_at': button['created_at'].isoformat() if button.get('created_at') else None
        })
    except Exception as e:
        print(f"Error getting button details: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/catalogs/by-button/<button_id>', methods=['GET'])
def get_catalog_by_button(button_id):
    try:
        button = get_button_with_catalog_mongo(button_id)
        if not button or not button.get('is_catalog'):
            return jsonify({'status': 'error', 'message': 'Catalog not found'}), 404
            
        return jsonify({
            'catalogName': button.get('catalog_name', ''),
            'catalogTopic': button.get('catalog_topic', ''),
            'description': button.get('description', ''),
            'imagePaths': button.get('image_paths', []),
            'pdfPaths': button.get('pdf_paths', [])
        })
    except Exception as e:
        print(f"Error getting catalog: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/send-pdf', methods=['GET'])
def get_data():
    catalog_entry = get_latest_catalog_entry_mongo()
    data = {
        'name': catalog_entry['catalog_name'],  # Changed from catalogName to catalog_name
        'pdf_path': f'./Outputs/{catalog_entry["catalog_name"]}.pdf'  # Changed here as well
    }
    
    if os.path.exists(data['pdf_path']):
        return send_file(data['pdf_path'], as_attachment=True)
    return jsonify({'error': 'PDF file not found'}), 404

@app.route('/api/send-pdf-name', methods=['GET'])
def get_name():
    catalog_entry = get_latest_catalog_entry_mongo()
    if not catalog_entry:
        return jsonify({'error': 'No catalog entry found'}), 404
    return jsonify({'filename': f'{catalog_entry["catalog_name"]}.pdf'})

if __name__ == '__main__':
    app.run()

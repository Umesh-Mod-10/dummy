from .mongodb_config import get_mongodb_client
from datetime import datetime
from bson import ObjectId

def create_entry_mongo(data):
    client = get_mongodb_client()
    db = client.digital_catalog
    entry = {
        'catalog_name': data.get('catalogName', ''),
        'catalog_topic': data.get('catalogTopic', ''),
        'description': data.get('description', ''),
        'image_paths': data.get('image_paths', []),
        'pdf_paths': data.get('pdf_paths', []),
        'include_images': data.get('include_images', None),
        'buttonName': data.get('buttonName', ''),
        'buttonDesc': data.get('buttonDesc', ''),
        'buttonId': data.get('buttonId', ''),
        'is_catalog': data.get('is_catalog', False),
        'created_at': datetime.now()
    }
    result = db.catalog_entries.insert_one(entry)
    return result.inserted_id

def update_catalog_files_mongo(entry_id, image_paths, pdf_paths, include_images, description=None, button_data=None):
    client = get_mongodb_client()
    db = client.digital_catalog
    update_data = {
        'image_paths': image_paths,
        'pdf_paths': pdf_paths,
        'include_images': include_images,
        'updated_at': datetime.now()
    }
    
    if description:
        update_data['description'] = description
    
    if button_data:
        update_data.update({
            'buttonName': button_data.get('buttonName', ''),
            'buttonDesc': button_data.get('buttonDesc', ''),
            'buttonId': button_data.get('buttonId', ''),
            'is_catalog': button_data.get('is_catalog', False)
        })
    
    db.catalog_entries.update_one(
        {'_id': ObjectId(entry_id)},
        {'$set': update_data}
    )

def update_catalog_description_mongo(entry_id, description):
    client = get_mongodb_client()
    db = client.digital_catalog
    db.catalog_entries.update_one(
        {'_id': ObjectId(entry_id)},
        {'$set': {
            'description': description,
            'updated_at': datetime.now()
        }}
    )

def update_catalog_details_mongo(entry_id, data):
    client = get_mongodb_client()
    db = client.digital_catalog
    update_data = {
        'catalog_name': data.get('catalogName', ''),
        'catalog_topic': data.get('catalogTopic', ''),
        'updated_at': datetime.now()
    }
    result = db.catalog_entries.update_one(
        {'_id': ObjectId(entry_id)},
        {'$set': update_data}
    )
    return entry_id

def get_latest_catalog_entry_mongo():
    client = get_mongodb_client()
    db = client.digital_catalog
    return db.catalog_entries.find_one(
        sort=[('created_at', -1)]
    )

def get_catalog_by_id_mongo(entry_id):
    client = get_mongodb_client()
    db = client.digital_catalog
    return db.catalog_entries.find_one(
        {'_id': ObjectId(entry_id)}
    )

def get_all_buttons_mongo():
    """Retrieve all buttons with their catalog status based on description"""
    client = get_mongodb_client()
    db = client.digital_catalog
    buttons = list(db.catalog_entries.find(
        {},
        {
            'buttonName': 1,
            'buttonDesc': 1,
            'buttonId': 1,
            'description': 1,
            'catalog_name': 1,
            'catalog_topic': 1,
            'image_paths': 1,
            'pdf_paths': 1,
            'created_at': 1
        }
    ))
    
    # Transform the data to include has_catalog flag based on description
    for button in buttons:
        button['has_catalog'] = bool(button.get('description', '').strip())
    
    return buttons

def get_button_with_catalog_mongo(button_id):
    """Get detailed button info including its catalog if exists"""
    client = get_mongodb_client()
    db = client.digital_catalog
    button = db.catalog_entries.find_one(
        {'buttonId': button_id},
        {
            'buttonName': 1,
            'buttonDesc': 1,
            'buttonId': 1,
            'description': 1,
            'catalog_name': 1,
            'catalog_topic': 1,
            'image_paths': 1,
            'pdf_paths': 1,
            'created_at': 1
        }
    )
    
    if button:
        button['has_catalog'] = bool(button.get('description', '').strip())
    
    return button

def update_button_catalog_status_mongo(button_id, is_catalog=True):
    """Update isCatalogCreated flag when catalog is created"""
    client = get_mongodb_client()
    db = client.digital_catalog
    result = db.catalog_entries.update_one(
        {'buttonId': button_id},
        {'$set': {
            'is_catalog': is_catalog,
            'updated_at': datetime.now()
        }}
    )
    return result.modified_count > 0

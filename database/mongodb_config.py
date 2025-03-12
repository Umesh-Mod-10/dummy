from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging
import certifi
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'digital_catalog')

def get_mongodb_client():
    try:
        # Configure client with longer timeouts and retryable writes
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            ssl=True,
            tlsCAFile=certifi.where()
        )
        # Test the connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        logger.error(f"MongoDB URI being used: {MONGODB_URI}")
        return None

def get_database():
    if not MONGODB_URI:
        raise Exception("MONGODB_URI environment variable is not set")
        
    client = get_mongodb_client()
    if client is None:
        raise Exception("Failed to connect to MongoDB. Please check your MONGODB_URI in .env file")
    
    try:
        db = client[DB_NAME]
        # Ensure we can actually access the database
        collections = db.list_collection_names()
        logger.info(f"Successfully accessed database. Available collections: {collections}")
        return db
    except Exception as e:
        logger.error(f"Error accessing database {DB_NAME}: {str(e)}")
        raise Exception(f"Failed to access database {DB_NAME}. Error: {str(e)}")

def store_image_metadata(image_data: dict):
    """Store image metadata in MongoDB"""
    try:
        db = get_database()
        collection = db['image_metadata']
        
        metadata = {
            'image_id': image_data.get('id', str(datetime.utcnow())),
            'file_name': image_data.get('file_name'),
            'file_path': image_data.get('file_path'),
            'created_at': datetime.utcnow(),
            'description': image_data.get('description'),
            'tags': image_data.get('tags', []),
            'size': image_data.get('size'),
            'mime_type': image_data.get('mime_type')
        }
        
        result = collection.insert_one(metadata)
        logger.info(f"Stored image metadata with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error storing image metadata: {str(e)}")
        raise

def get_image_metadata(image_id: str):
    """Get metadata for a specific image"""
    try:
        db = get_database()
        collection = db['image_metadata']
        return collection.find_one({'image_id': image_id})
    except Exception as e:
        logger.error(f"Error retrieving image metadata: {str(e)}")
        raise

def get_all_images():
    """Get all images metadata"""
    try:
        db = get_database()
        collection = db['image_metadata']
        return list(collection.find().sort('created_at', -1))
    except Exception as e:
        logger.error(f"Error retrieving all images: {str(e)}")
        raise

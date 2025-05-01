import boto3
import numpy as np
import cv2
import tempfile
import os
from deepface import DeepFace

def download_image(bucket, key):
    """
    Downloads an image file from S3 and saves it temporarily.
    Returns the local path of the downloaded image.
    """
    s3 = boto3.client("s3")

    # Create a temporary file to hold the image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        s3.download_fileobj(bucket, key, temp_file)
        return temp_file.name


def load_image(path):
    """
    Loads an image using OpenCV.
    """
    image = cv2.imread(path)
    return image


def find_face(image):
    """
    Detects the first face in the image using Haar Cascade.
    Returns the face region cropped from the image.
    """
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        raise ValueError("No face found in the image.")

    # Take the first face found
    x, y, w, h = faces[0]
    face_image = image[y:y+h, x:x+w]
    return face_image


def lambda_handler(event, context):
    """
    Main function for AWS Lambda.
    Reads one image from S3, processes it, and returns a face vector.
    """
    try:
        # Get S3 info from the event
        bucket_name = event.get("bucket")
        image_key = event.get("key")

        if not bucket_name or not image_key:
            return {
                "statusCode": 400,
                "body": "Error: Missing bucket name or image key."
            }
         
        image_path = download_image(bucket_name, image_key)
        image = load_image(image_path)

        if image is None:
            return {
                "statusCode": 400,
                "body": "Error: Unable to load image."
            }
        
        face = find_face(image)

        if face is None:
            return {
                "statusCode": 400,
                "body": "Error: No face found in the image."
            }
        # DeepFace will automatically use the FaceNet model if you don't specify another model
        face_vector = DeepFace.represent(face, model_name="Facenet", enforce_detection=False)
        if not face_vector:
            return {
                "statusCode": 400,
                "body": "Error: Unable to extract face vector."
            }
        # Extract the first face vector
        # Note: DeepFace returns a list of dictionaries, each containing an embedding
        vector = face_vector[0]["embedding"]

        # Convert the vector to a numpy array
        vector = np.array(vector)
        
        # Delete the temp image file
        os.remove(image_path)

        # Return vector as a list
        return {
            "statusCode": 200,
            "body": {
                "vector": vector.tolist()
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

# Facial Recognition Image Encoder – AWS Lambda

This project is a Python-based AWS Lambda function designed to process one image at a time from an S3 bucket and convert the face in the image into a fixed-length vector (embedding). The vector represents key facial features and is used as input for machine learning models.

## What This Lambda Does

- Receives an image reference from AWS S3
- Loads the image and detects a face
- Encodes the face into a 128-dimensional vector
- Returns the vector as a list of floating-point values

This process is called **facial encoding** — turning facial features into numbers that can be used for facial recognition and identity verification.

## Why This Matters

Facial encodings make it possible to compare faces using mathematics rather than pixels. High-quality encodings improve the accuracy of facial recognition systems and are essential for training machine learning models.

## Key Concepts Covered

- Reading image files from AWS S3 using `boto3`
- Using the `face_recognition` library to detect and encode faces
- Ensuring consistent vector output (same length every time)
- Structuring Python code for AWS Lambda deployment
- Writing clean, well-commented, review-ready code

## Outcome

Once deployed, this Lambda will enable a system where facial images can be transformed into consistent, descriptive vectors. These vectors can then be stored, compared, or used in downstream ML workflows for tasks like authentication, clustering, or face matching.

---

**Developed by:** Mpho Mofokeng  
**Purpose:** Task 2 - Facial Recognition Authentication System  
**Stack:** Python, AWS Lambda, S3, face_recognition, boto3  

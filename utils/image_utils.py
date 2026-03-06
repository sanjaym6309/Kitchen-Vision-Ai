import cv2
import numpy as np

def preprocess_image(image_bytes):
    """
    Preprocess the uploaded pantry image:
    1. Decode from bytes
    2. Resize if too large
    3. Adjust brightness and contrast
    4. Encode back to jpg format
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image provided")

    # Resize (limit max dimension to 1024 to save API processing time / tokens)
    max_dim = 1024
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Adjust brightness and contrast
    # alpha = contrast control (1.0-3.0), beta = brightness control (0-100)
    alpha = 1.2
    beta = 10
    enhanced_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    # Optional: Enhance clarity (slight sharpening)
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened_img = cv2.filter2D(enhanced_img, -1, kernel)

    # Encode back to JPEG for API upload
    _, buffer = cv2.imencode('.jpg', sharpened_img)
    return buffer.tobytes()

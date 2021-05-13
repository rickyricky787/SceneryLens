import numpy as np
import tensorflow as tf
from PIL import Image

def predictImage(img):
    # Load model
    model_json = None

    with open('model/xception_model.json', 'r') as f:
        model_json = f.read()

    model = tf.keras.models.model_from_json(model_json)

    # Add weights
    model.load_weights('model/xception_weights.h5')

    # Array of labels
    labels = [
        "alley", "bridge", "canyon", "desert", "downtown", 
        "forest", "grotto", "iceberg", "lake", "mountain", 
        "ocean", "park", "rock_arch", "ruin", "sky", 
        "skyscraper", "snowfield", "street", "village", "waterfall"
    ]
    
    # Resize image
    size = (128, 128)
    new_img = img.resize(size)

    # Process the image
    input_arr = tf.keras.preprocessing.image.img_to_array(new_img)
    img_batch = np.expand_dims(input_arr, axis=0)
    
    image_preprocessed = tf.keras.applications.resnet_v2.preprocess_input(img_batch)

    # Predict image
    y_preds = model.predict(image_preprocessed)

    # Get top three predictions
    pred_label_list = []
    pred_score_list = []

    for i in range(3):
        pred_pos = np.argmax(y_preds)
        pred_label = labels[pred_pos]
        pred_score = np.amax(y_preds)
        
        pred_label_list.append(pred_label)
        pred_score_list.append(pred_score)

        y_preds = np.delete(y_preds, pred_pos)
        labels.pop(pred_pos)

    return pred_label_list, pred_score_list



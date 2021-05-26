import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.xception import preprocess_input
from PIL import Image

def predictImage(img):
    # Load model
    with open('model/xception_model.json', 'r') as f:
        model_json = f.read()

    model = model_from_json(model_json)

    # Add weights
    model.load_weights('model/xception_weights.h5')

    # Array of labels
    labels = [
        "Alley", "Bridge", "Canyon", "Desert", "Downtown", 
        "Forest", "Grotto", "Iceberg", "Lake", "Mountain", 
        "Ocean", "Park", "Rock Arch", "Ruin", "Sky", 
        "Snowfield", "Street", "Tower", "Village", "Waterfall"
    ]
    
    # Resize image
    size = (256, 256)
    new_img = img.resize(size)

    # Process the image
    input_arr = img_to_array(new_img)
    img_batch = np.expand_dims(input_arr, axis=0)
    
    image_preprocessed = preprocess_input(img_batch)

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



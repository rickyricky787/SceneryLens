import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" 

import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.xception import preprocess_input
from PIL import Image

def predictImage(model, labels, img):
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



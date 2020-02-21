import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from django.conf import settings
from os import path

def predict(value): 
    absoluteAddr = path.join(settings.BASE_DIR)                            #function for prediction
    absoluteAddr = path.join(absoluteAddr, "CropPred")
    absoluteAddr = path.join(absoluteAddr, "crop_pred")
    pkl_filename='crop_prediction.pkl'
    pkl_filename = path.join(absoluteAddr,pkl_filename)
    """[
        [
            ph_val, -> Float32
            temp_val, -> Float32
            humidity_val, ->Float32
            rainfall_val, -> Float32
            moisture_val - > Float32
        ]
    ]"""
    with open(pkl_filename,'rb') as file:
        
        model=pickle.load(file)
        pred=model.predict(value)
        pred = list(pred).pop()
        pred = int(pred)
        if pred is 1:
            pred = "paddy"
        elif pred is 2:
            pred = "corn"
        elif pred is 3:
            pred = "potato"
        elif pred is 4:
            pred = "tomato"
    return pred

if __name__ == "__main__":
    l = predict([[20.20,32,10,140,80]])

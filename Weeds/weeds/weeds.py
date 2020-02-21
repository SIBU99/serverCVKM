from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
from skimage import transform
import os
def predict(filename):
    def load(filename):
        np_image = Image.open(filename) #Open the image
        np_image = np.array(np_image).astype('float32')/255 #Creates a numpy array as float and divides by 255.
        np_image = transform.resize(np_image, (150, 150, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "weed.h5")
    model=load_model(path)
    image_to_predict = load(filename)
    result = model.predict(image_to_predict)
    result= np.around(result,decimals=3)
    result=result*100
    result = list(map(float,result[0]))
    dataset = {
        'broadleaf': result[0],
        'grass': result[1],
        'soil': result[2],
        'soybean': result[3],
        }
    return dataset

if __name__=="__main__":
    print(predict("D:\\machine_learning_and _iot\\dataSet\\dataset\\test\\grass\\1.tif"))




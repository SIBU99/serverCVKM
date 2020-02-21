from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
from skimage import transform
import os


   #picture1 prediction
def predict(filename):
    def load(filename):
        np_image = Image.open(filename) #Open the image
        np_image = np.array(np_image).astype('float32')/255 #Creates a numpy array as float and divides by 255.
        np_image = transform.resize(np_image, (150, 150, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    path = os.apth.dirname(os.path.abspath(__file__))
    path = os.apth.join(path, "seedling.h5")
    model=load_model(path)
    image_to_predict = load(filename)
    result = model.predict(image_to_predict)
    result= np.around(result,decimals=3)
    result=result*100
    result = list(map(float, result[0]))
    dataset = {
        'Black-grass': result[0],
        'Charlock': result[1],
        'Cleavers': result[2],
        'Common Chickweed': result[3],
        'Common wheat': result[4],
        'Fat Hen': result[5],
        'Loose Silky-bent': result[6],
        'Maize': result[7],
        'Scentless Mayweed': result[8],
        'ShepherdGÇÖs Purse': result[9],
        'Small-flowered Cranesbill': result[10],
        'Sugar beet': result[11],
        }
    
    return dataset
if __name__=="__main__":
        print(predict("D:\\machine_learning_and _iot\\seedling\\training\\Black-grass\\1.png"))





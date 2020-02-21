from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
 #use it
from PIL import Image
import numpy as np
from skimage import transform

def predict(imagename):
    "this will predict nutrient deficient"
    def load(filename):
        np_image = Image.open(filename) #Open the image
        np_image = np.array(np_image).astype('float32')/255 #Creates a numpy array as float and divides by 255.
        np_image = transform.resize(np_image, (150, 150, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image
    
    model=load_model('nutrient.h5')
    image_to_predict = load(imagename)
    result = model.predict(image_to_predict)
    result= np.around(result,decimals=3)
    result=result*100
    result = list(map(int, result[0]))

    dataset = {
        'Healthy Leaves':result[0],
        'Iron Deficient': result[1],
        'Magnisium_deficient': result[2],
        'Sulphur_deficient': result[3],
        'nitrogen_deficient': result[4]
    }
    return dataset


if __name__=="__main__":
        print(predict("D:\\machine_learning_and _iot\\nutrients\\train\\Healthy Leaves\\1.jpg"))


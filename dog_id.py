import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from PIL import Image
from keras.applications.densenet import preprocess_input

model = tf.keras.models.load_model('static/model/dog_id_model2(1).h5')

breed_list = os.listdir("static/model/images/Images/")

label_maps = {}
label_maps_rev = {}
for i, v in enumerate(breed_list):
    label_maps.update({v: i})
    label_maps_rev.update({i : v})

def download_and_predict(url, filename):
    # download and save
    os.system("curl -s {} -o {}".format(url, filename))
    img = Image.open(filename)
    img = img.convert('RGB')
    img = img.resize((224, 224))
    img.save(filename)
    # show image
    plt.figure(figsize=(4, 4))
    plt.imshow(img)
    plt.axis('off')
    # predict
    img = imread(filename)
    img = preprocess_input(img)
    probs = model.predict(np.expand_dims(img, axis=0))
    for idx in probs.argsort()[0][::-1][:5]:
        print("{:.2f}%".format(probs[0][idx]*100), "\t", label_maps_rev[idx].split("-")[-1])

download_and_predict("https://images-na.ssl-images-amazon.com/images/I/41l5feWxmcL.jpg", "test_1.jpg")
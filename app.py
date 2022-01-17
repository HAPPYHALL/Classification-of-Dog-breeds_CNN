import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from pymongo import MongoClient
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.io import imread
from PIL import Image
from keras.applications.densenet import preprocess_input


client = MongoClient('localhost', 27017)
db = client.db_ai_dog_breeds


# 머신러닝
model = tf.keras.models.load_model('static/model/dog_id_model2.h5')

breed_list = os.listdir("static/model/images/Images/")




# 웹 서버
app = Flask(__name__)
# print(tf.__version__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def main():

    a,b= download_and_predict("1.jpg","1.jpg")
    img = '../1.jpg'
    return render_template("main.html", a= a, b=b,c=a[0],d=b[0], zip=zip,int=int , img = img)

@app.route('/upload')
def uplode():
    return render_template("upload.html")

# 파일 업로드

@app.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    # today = datetime.now()
    # mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = 1
    # 파일 저장 경로 설정 (파일은 서버 컴퓨터 자체에 저장됨)
    save_to = f'./{filename}.{extension}'
    save_to = f'./static/sajin/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)

    return jsonify({'result':'success'})

label_maps = {}
label_maps_rev = {}
for i, v in enumerate(breed_list):
    label_maps.update({v: i})
    label_maps_rev.update({i : v})



def download_and_predict(url, filename):
    # download and save
    os.system("curl -s {} -o {}".format(url,filename))
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


    var_list_1, var_list_2 = [], []

    for idx in probs.argsort()[0][::-1][:3]:
        print("{:.2f}%".format(probs[0][idx]*100), "\t", label_maps_rev[idx].split("-")[-1])

        # probs[0][idx] 변수를 생성
        var_1 = probs[0][idx]
        # 두 번째 매개변수도 변수화
        var_2 = label_maps_rev[idx].split("-")[-1]
        # append()함수로 하나씩 할당
        var_list_1.append(int(var_1*100))
        var_list_2.append(var_2)

        # print(var_list_1, var_list_2)
    return [var_list_1, var_list_2]


# print(download_and_predict)



if __name__ == '__main__':
    app.run()



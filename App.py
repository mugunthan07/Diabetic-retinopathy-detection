from flask import Flask, render_template, flash, request, session

import cv2

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Prediction")
def Prediction():
    return render_template('Prediction.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        pname = request.form['pname']
        mobile = request.form['mobile']

        file = request.files['file']
        file.save('static/Out/Test.jpg')

        import_file_path = 'static/Out/Test.jpg'
        img1 = cv2.imread(import_file_path)

        img1S = cv2.resize(img1, (400, 400))

        cv2.imshow('Original image', img1S)

        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        dst = cv2.resize(dst, (400, 400))
        cv2.imshow("Noise Removal", dst)

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('diabetic.h5')

        import numpy as np
        from keras.preprocessing import image
        test_image = image.load_img('./static/Out/Test.jpg', target_size=(200, 200))
        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        print(result)

        out = ''
        if result[0][0] == 1:
            print("DR1")
            out = "DR1"
            re = 'Short-acting (regular) insulin'


        elif result[0][1] == 1:
            print("DR2")
            out = "DR2"
            re = 'Possibly, diabetes medication or insulin therapy'

        elif result[0][2] == 1:
            print("Normal")
            out = "Normal"
            re = 'nil'

        sendmsg(mobile,"Prediction Result: "+str(out))

        return render_template('Result.html', pre=out, result=re)



@app.route("/res", methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        return render_template('Prediction.html')
def sendmsg(targetno,message):
    import requests
    requests.post("http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

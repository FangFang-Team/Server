import base64
from flask import Flask
from flask import request
from predictor import predict

app = Flask(__name__)


@app.route('/classification', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    data = request.form
    image = data['image']
    # print(image)
    image = base64.b64decode(image)
    file = open('image.jpg', 'wb')
    file.write(image)
    file.close()
    res = predict("./image.jpg")
    # print(res)
    return res


if __name__ == '__main__':
    app.run()

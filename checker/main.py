import os
from flask import Flask, request, redirect, url_for, render_template
from PIL import Image
from tensorflow import keras
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def model():
	model=keras.models.load_model("model_2.h5")
	return model

def image_conditioning(filename):
	path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
	image=Image.open(path)
	imsize=(224,224)
	image=image.resize(imsize)
	image=keras.preprocessing.image.img_to_array(image)
	image=np.expand_dims(image,axis=0)
	return image
	
@app.route('/')
def index():
	message='Select an image to upload and display'
	return render_template('upload.html', intro=message)

@app.route('/upload', methods=['POST'])
def upload_image():
	file = request.files['file']
	message=None
	if file and allowed_file(file.filename):
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		message='Image successfully uploaded and displayed'
		intro='prediction'
		return render_template('upload.html', filename=filename, message=message, intro=intro)
	else:
		message='Allowed image types are -> png, jpg, jpeg, gif'
		return render_template('upload.html', message=message)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='images/' + filename), code=301)

@app.route('/predict/<filename>')
def predict(filename):
	
	model=keras.models.load_model("model_2.h5")
	image=image_conditioning(filename)
	results=model.predict_classes(image)
	message=results[0]
	return render_template('upload.html', message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

import os
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
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
	message='kfljakljfpredict'
	return render_template('upload.html', message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

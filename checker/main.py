import os
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('Image successfully uploaded and displayed')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='images/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

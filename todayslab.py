from flask import Flask, render_template, request, redirect, url_for, abort
import os

app = Flask(__name__)

# Route 1: Display a welcome message on the home page.
@app.route('/')
def index():
    return render_template('homepage.html')

# Route 2: Display information about yourself on a separate page.
@app.route('/about')
def about():
    return render_template('about.html')

# Route 3: Create a custom 404 error page.
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, this page does not exist.", 404

# Form Handling: Create a form with Flask that takes user input and displays it on a new page after submission.
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('form_result.html', name=name, email=email)
    return render_template('form.html')

# File Upload: Create a Flask route that allows users to upload files.
# Save the uploaded files on the server and display a list of uploaded files on another page.
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Get current working directory and join with 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the 'uploads' folder exists, if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to display file upload form
@app.route('/upload')
def upload_form():
    return render_template('upload_form.html')

# Route to handle file upload and save files on the server
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_files'))

# Route to display list of uploaded files
@app.route('/uploaded_files')
def uploaded_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('uploaded_files.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)

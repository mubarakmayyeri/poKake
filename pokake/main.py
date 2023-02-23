from flask import (Blueprint, flash, redirect, url_for, render_template, request, send_file, send_from_directory)
import subprocess
import sys
import os


bp = Blueprint('/', __name__)

container = '.\\uploads'

# Upload Streamlit and model pickle files
@bp.route('/', methods=['GET', 'POST'])
def upload():
    file = None
    for file in os.listdir(container):
        try:
            file = os.path.join(container, file)
            break
        except Exception as e:
            file = None
    if request.method == 'POST':
        streamlit = request.files['streamlit']
        model = request.files['model']
        
        error = None

        if not streamlit:
            error = 'Streamlit file is required!!!'
        elif not model:
            error = 'Model file is required!!!'
        
        if error is None:
            streamlit.save(os.path.join(container, streamlit.filename))
            model.save(os.path.join(container, model.filename))
            flash('Files uploaded successfully...')
            file = streamlit.filename
    
        flash(error)
        
        
    return render_template('/home.html', file=file)

# Compile and run the Streamlit app
@bp.route('/compile/<file>', methods=['GET'])
def compile(file):
    path = os.path.join(container, file)

    try:
        subprocess.run(f"streamlit run {path}", shell=True, check=True)
        subprocess.Popen(f"streamlit run {file}", shell=True)
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    
    
    
    
    return render_template('/compile.html', file=file)

# Remove files from container
@bp.route('/delete')
def delete():
    for file in os.listdir(container):
        try:
            path = os.path.join(container, file)
            os.remove(path)
        except:
            flash('Error occurred')
    flash('Files deleted successfully...')
    
    
    return redirect(url_for('.upload'))
from flask import (Blueprint, flash, redirect, render_template, request, send_file, send_from_directory)
import subprocess
import os


bp = Blueprint('/', __name__)

@bp.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        streamlit = request.files['streamlit']
        model = request.files['model']
        
        error = None

        if not streamlit:
            error = 'Streamlit file is required!!!'
        elif not model:
            error = 'Model file is required!!!'
        
        if error is None:
            streamlit.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), streamlit.filename))
            model.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), model.filename))
            flash('Files uploaded successfully...')
    
        flash(error)
        
        
    return render_template('/home.html')
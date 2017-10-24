#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo

import logging
from logging import Formatter, FileHandler
import os
import csv
import json

"""----------------------------------------------------------------------------"""
#App Config.
""""----------------------------------------------------------------------------"""

app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
       
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    
        if file and allowed_file(file.filename):
            app.logger.info('File Saved')
           
            filename = secure_filename(file.filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(savepath)
            file.save(savepath)
            
            #Saving File Contents in DB
            #save_in_db(savepath)

            return redirect(url_for('upload', filename=filename))
    return render_template('pages/placeholder.upload.html')
	
filename1= "C:\survey-viz\data\sample1.csv"


"""def save_in_db(savepath):
    # This function stores the csv contents into MongoDB
    app.logger.info(savepath)

    csv_rows = []

    with open(savepath) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])			
  
    #result = mongo.db.data.insert_many(csv_rows)
    
    #print(result.inserted_ids)"""

@app.route('/update', methods=['POST'])
def update():
    print(request)
    filepath = request.form['filename']
    title=[]
    print(filepath)
    with open(filepath,'r') as csvfile:

        reader = csv.DictReader(csvfile)
        title=reader.fieldnames
        print(title)
        numofField = len(title)
        return render_template('pages/placeholder.selector1.html',
                               title=title, numofField = numofField, filename=filepath)


@app.route('/updateFile',methods=['POST'])
def updateFile():
    print(request.form["numofField"])
    print(request.form["filename"])
    numofField= int(request.form["numofField"])
    newtitles = []
    filepath=request.form["filename"]
    print(filepath)
    for index in range(1, numofField+1):  # begin at 1 and leave filename out
        newtitles.append(request.form['field-' + str(index)])
    rows=[newtitles]
    print(newtitles)
    with open(filepath, 'r') as csv_in :
        reader = csv.reader(csv_in)
        next(reader, None) # ignores the original header
        for row in reader:
            rows.append(row) # stores all rows
    print(rows)
    filepath=filepath[:-4]+"new.csv"
    with open(filepath, 'w') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(rows) # writes all rows, including new header

    return """<html><div>New titles updated: {} to the file{} {}</div></html>""".format(newtitles, filepath, request)

@app.route('/selector')
def selector():
    return render_template('pages/placeholder.selector.html',filename=filename1)

filename2= "C:\survey-viz\data\sample1new.csv"


@app.route("/config", methods=['POST'])
def config():
    choices = {}
	filepath = request.form['filename']
    with open(filepath, 'r') as csvfile :
        reader = csv.reader(csvfile)
        titles = next(reader)
        for index, title in enumerate(titles,1):
            choice = 'choice-' + str(index)
            choices[title] = request.form.get(choice)
	return render_template('pages/placeholder.configure1.html',
                               title=title, filename=filepath)



@app.route('/configure')
def configure():
    return render_template('pages/placeholder.configure.html', filename=filename2)


@app.route('/dashboard')
def dashboard():
    return render_template('pages/placeholder.dashboard.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    """db_session.rollback()"""
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

"""----------------------------------------------------------------------------"""
# Launch.
"""----------------------------------------------------------------------------"""

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

#!/usr/bin/python
# file: flask_server.py
# Eilidh Southren - 1513195

#------------------------------------------
#
#   This script creates a flask server 
#   that allows the user to view the pictures
#   taken by the security system online. 
#


from flask import Flask, render_template
app = Flask(__name__)
import os
import time 

@app.route('/')
def index():

    # return array of files in static folder
    fileList = os.listdir("static")
   
    todayDate = time.strftime("%d_%m_%Y")
    newDate = '00_00_00'

    myData = {
        'list' : fileList,
        'date' : todayDate,
        'newDate' : newDate
        }
    
    return render_template('index.html', **myData)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        pass
print('Shutting down web app:', __name__)

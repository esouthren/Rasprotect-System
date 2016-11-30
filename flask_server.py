#!/usr/bin/python
# file: /home/pi/cm2540/labs/lab13/lab13_examples/lab13_example2/flask_server.py
from flask import Flask, render_template
app = Flask(__name__)
import os
import time 

@app.route('/')
def index():

    # return array of files in static folder
    fileList = os.listdir("/home/pi/Desktop/Coursework/static")
   
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

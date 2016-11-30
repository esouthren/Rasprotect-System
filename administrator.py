#!/usr/bin/python3
# file: lab10_example3/lab10_example3.py

from tkinter import *
from FSM import *
from sense_hat import SenseHat
import subprocess
import time
import datetime
import os


class GUI(Tk):


    # check SenseHat pins authorisation
    try:
        import RPi.GPIO as GPIO
    except RuntimeError:
        print('Error importing RPi.GPIO!\n',
              'This is probably because you need superuser privileges.\n',
              'You can achieve this by using "sudo" to run your script')
   
    # Set up Sensehat pins for IR Sensor
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.IN)


#
#    --->>  To DO List <<---
#
#    

# 
# 
# - when alarm is activated, send tweet and email (include date/time)
# 

#
#   Bonus Round:
#       - Add Countdown to activation
#       - Animated Intro
  
    # Take a picture and assign today's date as filename
    def takePic(self):
        date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        camera.capture("static/" + date + ".jpg")
        

    # Reverting back to initial state after alarm triggered        
    def _activate(self):
        self.fsm.state='initial'
        self.fsm.activeCheck = True
        hat.set_pixels(green)
        self.label2.config(text='Alarm Active', background='green')

    # When Infrared Sensor is triggered
    def IRevent(self,number):

        # if the alarm is 'active', trigger alarm
        if self.fsm.activeCheck == True:
            hat.set_pixels(blue)
            self.label2.config(text='ALARM', background='blue')
          # self.sendTweet()
            # Call Picture Taking Method
            self.after(10, self.takePic)
            # after 4 seconds, call activate method to revert to active state  
            self.after(2000, self._activate)

    
    # kill '# pictures deleted' popup
    def _destroyPopup(self):
        self.toplevel.destroy()
        self.popupCheck = False
        

    # delete pictures in /static/ directory
    def _deletePics(self):

        # count number of pictures, to display in popup window
        list = os.listdir('static/')
        file_count = len(list)

        # create popup window, if a popup does not currently exist
        if not self.popupCheck:
            self.toplevel = Toplevel()
            self.toplevel.title("pop")
            label1 = Label(self.toplevel, text="%s Pictures Deleted" % file_count)
            label1.pack(padx=20, pady=20)
            okButton = Button(self.toplevel, text='Close', command=self._destroyPopup)
            okButton.pack(padx=20, pady=10)
            self.popupCheck = True

        # Execute unix command to deleted files in /static, if directory exists
        if os.path.isdir('static/'):
            cmd = 'rm -r static/*'
            pid = subprocess.call(cmd, shell=True)

    # running/killing flask server script   
    def _serverSwitch(self):

        # if the server is currently not running
        if not self.serverCheck:            
            cmd = 'python /home/pi/Desktop/Coursework/flask_server.py'
            subprocess.Popen(cmd, shell=True)
            self.buttonServer.config(text="Turn Server Off")
            self.serverCheck = True
        else:
            self.buttonServer.config(text="Turn Server On")
            self.serverCheck = False
            # kill Flask processes
            cmd = "sudo kill $(ps aux | grep '[p]ython.*flask_server.py' | awk '{print $2}')"
            pid = subprocess.call(cmd, shell=True)
            
    # Handler for keyboard/arrow input
    def _JoystickPress(self, direction):
        self.fsm.step(str(direction))
        self.label2.config(text=self.fsm.lb, background=self.fsm.colour)
        if self.fsm.state == 'waiting':
          # specify delay for activation (60 seconds = 60000)
          self.after(2000, self._activate)

    
            
                 
    def __init__(self):
        super().__init__()
        
        self.geometry('600x420')
        self.title("CM2540 Coursework - Eilidh Southren 1513195")
        self.popupCheck = False

        # kill server if it's currently running to reset processes
        cmd = "sudo kill $(ps aux | grep '[p]ython.*flask_server.py' | awk '{print $2}')"
        pid = subprocess.call(cmd, shell=True)

        
        
        #keyboard input
        self.bind('<Key>', self.key_event_handler)

        # connect GUI to state machine that recognises input pattern: up/down/left/right
        self.fsm = ArrowFSM()
        # and start the FSM
        self.fsm.start()
        self.resizable(False, False)
        # Start Server/Delete pictures Buttons
        self.adminButtonsFrame = Frame(self)
        self.adminButtonsFrame.columnconfigure(0, weight=1)
        self.adminButtonsFrame.columnconfigure(1, weight=1)
        self.serverCheck = False
        self.buttonServer = Button(self.adminButtonsFrame,
                              text='Turn Server On',
                              background = '#dae6f1',
                              font = '10',
                              command=self._serverSwitch
                              )
        
        buttonDeletePics = Button(self.adminButtonsFrame,
                                  text='Delete all pictures',
                                  bg = '#dae6f1',
                                  font = '10',
                                  command=self._deletePics,
                                  )
        
        buttonDeletePics.grid(row=0, column=1, sticky=N+S+E+W)
        self.buttonServer.grid(row=0, column=0, sticky=N+S+E+W)
        self.adminButtonsFrame.pack(fill=BOTH)
        
        # label to display state
        self.label = Label(self, relief=RAISED, text='RasProtect System', font=("TkDefaultFont", 36), bg='#ffe6e6')
        self.label.pack(fill=BOTH, expand=1)
        # grid for on screen arrows
        self.arrowKeysGrid = Frame(self)
        # divide frame into columns, rows of equal weight
        self.arrowKeysGrid.columnconfigure(0, weight=1)
        self.arrowKeysGrid.columnconfigure(1, weight=1)
        self.arrowKeysGrid.columnconfigure(2, weight=1)
        self.arrowKeysGrid.rowconfigure(0, weight=1)
        self.arrowKeysGrid.rowconfigure(1, weight=1)

        buttonBlank1 = Button(self.arrowKeysGrid, text='', state=DISABLED, background='#a3c2c2', bd=1)
        buttonBlank1.grid(row=0, column=0, sticky=N+S+E+W)

        self.buttonUp = Button(self.arrowKeysGrid, text='Up', command=lambda: self._JoystickPress('Up'), background = '#dae6f1')
        self.buttonUp.grid(row=0, column=1,  sticky=N+S+E+W)
        
        self.buttonBlank1 = Button(self.arrowKeysGrid, text='', state=DISABLED, background='#a3c2c2', bd=1)
        self.buttonBlank1.grid(row=0, column=2, sticky=N+S+E+W)
        
        self.buttonLeft = Button(self.arrowKeysGrid, text='Left', command=lambda: self._JoystickPress('Left'), background = '#dae6f1')
        self.buttonLeft.grid(row=1, column=0, sticky=N+S+E+W)
       
        self.buttonDown = Button(self.arrowKeysGrid, text='Down', command=lambda: self._JoystickPress('Down'), background = '#dae6f1')
        self.buttonDown.grid(row=1, column=1,  sticky=N+S+E+W)
        
        self.buttonRight = Button(self.arrowKeysGrid, text='Right', command=lambda: self._JoystickPress('Right'),background = '#dae6f1' )
        self.buttonRight.grid(row=1, column=2,  sticky=N+S+E+W)
        
        self.arrowKeysGrid.pack(fill=BOTH,  expand=1)
        self.label2 = Label(self, text=self.fsm.lb, background='red')
        self.label2.pack(fill=BOTH, expand=1)
        
        # setup IR event handling
        GPIO.add_event_detect(33, GPIO.RISING, callback=self.IRevent)


    def key_event_handler(self, event):
       if event.keysym == 'Up':
           self._JoystickPress('Up')   
       elif event.keysym == 'Down':
           self._JoystickPress('Down')
       elif event.keysym == 'Left':
           self._JoystickPress('Left')
       elif event.keysym == 'Right':
           self._JoystickPress('Right')
           
               
if __name__ == '__main__':
    app = GUI()
    app.mainloop()

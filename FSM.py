# file: lab10_example3/Recogniser1234FSM.py
# Eilidh Southren 1513195
#
#
# Statement of Compliance
#
#
#
# 

import sense_hat
import picamera
import time
import datetime
import subprocess


hat = sense_hat.SenseHat()
camera = picamera.PiCamera()


#====== Set Colours to Display on SenseHat ======#

r = [255,0,0]
w = [255,255,255]
g = [0,255,0]
b = [0,0,255]

# Alarm in deactivated mode
deactivated = [
    r,w,w,w,w,w,w,r,
    w,r,w,w,w,w,r,w,
    w,w,r,w,w,r,w,w,
    w,w,w,r,r,w,w,w,
    w,w,w,r,r,w,w,w,
    w,w,r,w,w,r,w,w,
    w,r,w,w,w,w,r,w,
    r,w,w,w,w,w,w,r
    ]

# When passcode is being inputted (Alarm currently deactive)
inputSequenceActivate = [
    r,r,r,w,w,w,w,w,
    w,w,r,r,r,w,w,w,
    w,w,w,w,r,r,r,w,
    w,w,w,w,w,w,r,r,
    w,w,w,w,w,w,r,r,
    w,w,w,w,r,r,r,w,
    w,w,r,r,r,w,w,w,
    r,r,r,w,w,w,w,w,
    ]

# When passcode is being inputted (Alarm currently active)
inputSequenceDeactivate = [
    w,w,w,w,w,g,g,g,
    w,w,w,g,g,g,w,w,
    w,g,g,g,w,w,w,w,
    g,g,w,w,w,w,w,w,
    g,g,w,w,w,w,w,w,
    w,g,g,g,w,w,w,w,
    w,w,w,g,g,g,w,w,
    w,w,w,w,w,g,g,g,
    ]

# Triggered Alarm
blue = [
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b
    ]

# Sequence Correct and Alarm active
green = [
    w,w,w,g,g,w,w,w,
    w,g,g,g,g,g,g,w,
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g,
    g,g,g,g,g,g,g,g,
    w,g,g,g,g,g,g,w,
    w,w,w,g,g,w,w,w,
    ]

# Pause between sequence success and activation
activatePause = [
    w,w,w,r,r,w,w,w,
    w,r,r,w,w,r,r,w,
    r,r,w,w,w,w,r,r,
    r,w,w,w,w,w,w,r,
    r,w,w,w,w,w,w,r,
    r,r,w,w,w,w,r,r,
    w,r,r,w,w,r,r,w,
    w,w,w,r,r,w,w,w,
    ]
    
hat.set_pixels(deactivated)


# Verify GPIO settings         
try:
    import RPi.GPIO as GPIO
except RuntimeError:
        print('Error importing RPi.GPIO!\n',
              'This is probably because you need superuser privileges.\n',
              'You can achieve this by using "sudo" to run your script')

class FSM:
    def start(self):
        # Initial Alarm settings
        self.state = self.startState
     
        self.lb = 'Alarm Deactivated'
        self.colour = 'red'
        self.activeCheck = False


        
    # now prompt the FSM to step to its next state
    # return output prompted by this transition
    def step(self, inp):
        (s, o, lb, c, b) = self.getNextValues(self.state, inp, self.lb, self.colour, self.activeCheck)
        self.state = s
       
        self.lb = lb
        self.colour = c
        self.activeCheck = b
       
            

class ArrowFSM(FSM):
    # define start state for FSM
    startState = 'initial'

    
  
    def getNextValues(self, state, inp, lb, col, check):

        # States:   Initial 
        #   up ->   d1
        #   down -> d2
        #   left->  d3
        #   right-> waiting
        #
        #
        
            if state == 'initial':
                if check == False: 
                    if inp == 'Up':                        
                        hat.set_pixels(inputSequenceActivate)
                        return ('d1', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                    else:
                        hat.set_pixels(green)
                        return ('initial', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                elif check == True:
                    if inp == 'Up':
                        hat.set_pixels(inputSequenceDeactivate)
                        return('d1', None, 'Alarm Activated: Waiting for User Input', 'green', True)
                    else:
                        return('initial', None, 'Alarm Activated: Waiting for User input', 'green', True)

            if state == 'd1':
                if check == False: 
                    if inp == 'Down':
                        hat.set_pixels(inputSequenceActivate)
                        return ('d2', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                    else:
                        return ('d1', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                elif check == True:
                    if inp == 'Down':
                        hat.set_pixels(inputSequenceDeactivate)
                        return('d2', None, 'Alarm Activated: Waiting for User Input', 'green', True)
                    else:
                        return('d1', None, 'Alarm Activated: Waiting for User input', 'green', True)

            if state == 'd2':
                if check == False: 
                    if inp == 'Left':
                        hat.set_pixels(inputSequenceActivate)
                        return ('d3', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                    else:
                        return ('d2', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                elif check == True:
                    if inp == 'Left':
                        hat.set_pixels(inputSequenceDeactivate)
                        return('d3', None, 'Alarm Activated: Waiting for User Input', 'green', True)
                    else:
                        return('d2', None, 'Alarm Activated: Waiting for User input', 'green', True)

            if state == 'd3':
                if check == False: 
                    if inp == 'Right':
                        hat.set_pixels(activatePause)
                        return ('waiting', None, 'Alarm Activating,  please wait', 'purple', False)
                    else:
                        return ('d3', None, 'd3 Alarm Dectivated: Waiting for User Input', 'red', False)
                elif check == True:
                    if inp == 'Right':
                        hat.set_pixels(deactivated)
                        return('initial', None, 'Alarm Deactivated: Waiting for User Input', 'red', False)
                    else:
                        return('d3', None, 'Alarm Activated: Waiting for User Input', 'green', True)
                
                     
            # if any keys are pressed in 'triggered' or 'transitioning' state, do nothing   
            elif state == 'trig': 
               return(self.state, None, self.lb, self.colour, True)
            elif state == 'waiting':
                return(self.state, None, self.lb, self.colour, True)

                           

    
                
       

        
                   

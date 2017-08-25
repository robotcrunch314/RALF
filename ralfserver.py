@ -0,0 +1,367 @@
# ###
# fishserver.py
# Author: Robert Couch <robotcrunch314@gmail.com>
# Hey!  This is the Python 2.7
# script to receive commands from the app [insert
# URL for App Inventor Project here], and control
# a Pimoroni Explorer Hat!
# ###
# Created 7/28/2017

## *** Obviously still a work in progress*** ##

# ###

from bluetooth import *
#import RPi.GPIO as GPIO
import explorerhat
from time import sleep
import subprocess
from urllib import unquote_plus
import os

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

#
# initialise GPIO pins for LEDs
#

#pinLEDs = {16:'red', 18:'yellow', 22:'green'}
#for pin in pinLEDs:
#    GPIO.setup(pin, GPIO.OUT)
#    GPIO.output(pin, GPIO.LOW)

#
# initialise GPIO motor controller pins
#

#pinMotorAForwards = 36
#pinMotorABackwards = 38
#pinMotorAEnable = 40
#pinMotorBForwards = 19
#pinMotorBBackwards = 21
#pinMotorBEnable = 23

#GPIO.setup(pinMotorAForwards, GPIO.OUT)
#GPIO.setup(pinMotorABackwards, GPIO.OUT)
#GPIO.setup(pinMotorBForwards, GPIO.OUT)
#GPIO.setup(pinMotorBBackwards, GPIO.OUT)


## PWM parameters
#Frequency  = 20  # hertz
#DutyCycleA = 100 # max 100, adjust to equalise motors
#DutyCycleB = 100 # max 100, adjust to equalise motors
#Stop = 0
#
## enable PWM mode for motor control pins
#pwmMotorAForwards  = GPIO.PWM(pinMotorAForwards, Frequency)
#pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
#pwmMotorBForwards  = GPIO.PWM(pinMotorBForwards, Frequency)
#pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)
#
## start the software PWM with a duty cycle of zero (stop)
#pwmMotorAForwards.start(Stop)
#pwmMotorABackwards.start(Stop)
#pwmMotorBForwards.start(Stop)
#pwmMotorBBackwards.start(Stop)

#
# LED functions
#

#def ledson():
#    for pin in pinLEDs:
#        GPIO.output(pin, GPIO.HIGH)
#
#def ledsoff():
#    for pin in pinLEDs:
#        GPIO.output(pin, GPIO.LOW)
#
#def flashleds(count):
#    for i in range(count):
#        ledsoff()
#        sleep(0.2)
#        ledson()
#        sleep(0.2)
#        ledsoff()
#
#def ledcontrol(colour, state):
#    for pin in pinLEDs:
#        if pinLEDs[pin] == colour:
#            if state == 'on':
#                 GPIO.output(pin, GPIO.HIGH)
#            elif state == 'off':
#                 GPIO.output(pin, GPIO.LOW)


#
# motor control functions
#

def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()

def FF():
    explorerhat.motor.one.forward()
    explorerhat.motor.two.forward()

def RR():
    explorerhat.motor.one.backward()
    explorerhat.motor.two.backward()

#def TurnLeft():
#    pwmMotorAForwards.ChangeDutyCycle(Stop)
#    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
#    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
#    pwmMotorBBackwards.ChangeDutyCycle(Stop)
#
#def TurnRight():
#    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
#    pwmMotorABackwards.ChangeDutyCycle(Stop)
#    pwmMotorBForwards.ChangeDutyCycle(Stop)
#    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)

def RF():
    explorerhat.motor.one.forward()

def LF():
    explorerhat.motor.two.forward()

def RB():
    explorerhat.motor.one.backward()

def LB():
    explorerhat.motor.two.backward()


# inputs are integers in range [-100, +100]
#def MotorSpeed(left, right):
#    if left > 0:
#        pwmMotorAForwards.ChangeDutyCycle(DutyCycleA * left / 100)
#        pwmMotorABackwards.ChangeDutyCycle(Stop)
#    else:
#        pwmMotorAForwards.ChangeDutyCycle(Stop)
#        pwmMotorABackwards.ChangeDutyCycle(DutyCycleA * abs(left) / 100)
#    if right > 0:
#        pwmMotorBForwards.ChangeDutyCycle(DutyCycleA * right / 100)
#        pwmMotorBBackwards.ChangeDutyCycle(Stop)
#    else:
#        pwmMotorBForwards.ChangeDutyCycle(Stop)
#        pwmMotorBBackwards.ChangeDutyCycle(DutyCycleA * abs(right) / 100)



#
# command functions
#

#def ledflash():
#    flashleds(3)
#    ledcontrol('green', 'on')

#def ledstate(colour, state):
#    ledcontrol(colour, state)

def robot():
    stop()
#    ledcontrol('red', 'off')

def robotstop():
    stop()
#    ledcontrol('red', 'off')

def FF():
    FF()
#    ledcontrol('red', 'on')

def RR():
    RR()
#    ledcontrol('red', 'on')

#def robotleft():
#    RF()
#    ledcontrol('red', 'on')

#def robotright():
#    LF()
#    ledcontrol('red', 'on')

#def robotmotors(left, right):
#    # convert string arguments to integers
#    left = int(left)
#    right = int(right)
#    # allowed range [-100, +100]
#    if left > 100:
#        left = 100
#    elif left < -100:
#        left = -100
#    if right > 100:
#        right = 100
#    elif right < -100:
#        right = -100
#    MotorSpeed(left,right)
#    ledcontrol('red', 'on')

def speak(phrase):
    phrase = unquote_plus(phrase)
    p1 = subprocess.Popen(['echo', phrase], stdout=subprocess.PIPE)
    subprocess.Popen(['festival', '--tts'], stdin=p1.stdout) # don't wait for process to end

def fart():
    os.system("aplay /home/pi/fish-audio/fart-2.wav")

def scream():
    os.system("aplay /home/pi/fish-audio/scream1.wav")
    
#
# main loop
#

#add serial port service
subprocess.call(['sudo', 'sdptool', 'add', 'SP'])

# signal main loop start
#flashleds(3)


try:
    while True:

        # ###
        # The following is copied directly from rfcomm-server.py
        # ###

        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service( server_sock, "fishserver",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ],
        #                   protocols = [ OBEX_UUID ]
                            )

        print("Waiting for connection on RFCOMM channel %d" % port)
# eventually we'll replace this will festival reply or something

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
# same here, just a placeholder from rfcomm-server.py


        # receiver loop
        try:
            partial = ''

            while True:

                # read from serial port receive buffer
                data = client_sock.recv(1024)
                if len(data) == 0:
                    break
                elif len(data) == 1024:
                    bufferfull = True
                else:
                    bufferfull = False
                # prepend any partial command from last time, then split commands
                commands = (partial + data).split('$$')
                number = len(commands)

                # full buffer means last command may not be complete, so hold it over
                if bufferfull:
                    partial = commands[number-1]
                    number -= 1
                else:
                    partial = ''

                # loop through commands
                for i in range(number):
                    # parse the command
                    command = commands[i]
                    parts = command.split('/')
                    count = len(parts)

                    if command == '':
                        continue

                    elif command == '/':
                        root()

                    #elif command == '/led':
                    #   led()

                    #elif command == '/led/flash':
                    #    ledflash()

                    #elif command[0:5] == '/led/' and count == 4:
                    #    colour = parts[2] # green, yellow, red
                    #    state = parts[3]  # on, off
                    #    ledstate(colour, state)

                    elif command == '/robot':
                        robot()

                    elif command == '/robot/stop':
                        robotstop()

                    elif command == '/robot/FF':
                        FF()

                    elif command == '/robot/RR':
                        RR()

                    elif command =='RF':
                        RF()

                    elif command == 'LF':
                        LF()

                    elif command == 'RB':
                        RB()

                    elif command == 'LB':
                        LB()

                    elif command == '/sound/fart':
                        fart()

                    elif command == '/sound/scream':
                        scream()

                    #elif command[0:14] == '/robot/motors/' and count == 5:
                    #    left = parts[3]  # integer 0-100
                    #    right = parts[4] # integer 0-100
                    #    robotmotors(left, right)

                    elif command[0:7] == '/speak/' and count == 3:
                        phrase = parts[2] # URI-encoded
                        speak(phrase)

                    else:
                        robotstop()
                        speak("error " + command)

        # receiver loop try
        except IOError:
            pass

        # connection lost
        client_sock.close()
        server_sock.close()

        # signal disconnect
        #ledcontrol('green', 'off')




# main loop try
except KeyboardInterrupt:
    client_sock.close()
    server_sock.close()
    GPIO.cleanup()

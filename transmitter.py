import RPi.GPIO as GPIO 
import time
import bluetooth
from bluetooth import *
import sys



buttonRed = 5
buttonGreen = 6
buttonBlue = 13
buttonYellow = 19
buttonBlack = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonRed, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(buttonGreen, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(buttonBlue, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(buttonYellow, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(buttonBlack, GPIO.IN,pull_up_down=GPIO.PUD_UP)



    


def findDevices():
    global nearby_devices
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    i = 0
    for  addr, name in nearby_devices:
        
        print("Index %s)  %s - %s" % (i,addr, name))
        i =i + 1
    
    #return nearby_devices
def selectDevice():
    findDevices()
    time.sleep(2)
    if len(nearby_devices) > 0:
        print("Type your device index to connect, type R to reload the devices list or C to close the program")
        userInput = input()
        if userInput == "C":
            sys.exit()
        elif userInput == "R":
            selectDevice()
        elif  userInput.isdigit() and int(userInput) < len(nearby_devices) :
            global addr
            addr = nearby_devices[int(userInput)][0]
            selectService()
        else:
            print("Command %s not found" % (userInput))
            selectDevice()
    else:
        print("Whe could not find any device, type R to reload the devices list or C to close the program")
        userInput = input()
        if userInput == "C":
            sys.exit()
        elif userInput == "R":
            selectDevice()
        else:
            print("Command %s not found"% (userInput))
            selectDevice()
            
def selectService():
    global serviceMatches
    serviceMatches = find_service( address = addr )
    buf_size = 1024;

    if len(serviceMatches) == 0:
        print("couldn't find the SampleServer service =(")
        time.sleep(3)
        selectDevice()

    for s in range(len(serviceMatches)):
        print("Service index " + str(s) + ") " + str(serviceMatches[s]['name']))
       
    time.sleep(2)
    print("Type your service index to connect, type R to reload the devices list or C to close the program")
    userInput = input()
    if userInput == "C":
        sys.exit()
    elif userInput == "R":
        selectDevice()
    elif  userInput.isdigit() and int(userInput) < len(serviceMatches) :
        chosenService = serviceMatches[int(userInput)]
        port = chosenService["port"]
        name = chosenService["name"]
        host = chosenService["host"]
        print("connecting to \"%s\" on %s, port %s" % (name, host, port))
        sock=BluetoothSocket(RFCOMM)
        try:
            sock.connect((host, port))
            print("Connected")
            time.sleep(1)
            print("Type B for send button information or T for type and send you own information")
            userInput = input()
            if userInput == "B":
                sendButtonInfo()
            elif userInput == "T":
                sendUserInput()
            else:
                print("Command %s not found" % (userInput))
                time.sleep(1)
                selectService()
        except:
            print("Connection refused, please try a different service")
            time.sleep(3)
            selectService()
    else:
        print("Command %s not found" % (userInput))
        selectDevice()
         
def sendButtonInfo():
    while True:
        data = 0
        if GPIO.input(buttonRed) == 0:
            data = data + 1
        if GPIO.input(buttonGreen) == 0:
            data = data + 2
        if GPIO.input(buttonBlue) == 0:
            data = data + 4
        if GPIO.input(buttonYellow) == 0:
            data = data + 8
        if GPIO.input(buttonBlack) == 0:
            data = data + 16
        print(data)
        time.sleep(1)
def sendUserInput():
    while True:
        data = input() 
        sock.send(data)
        sock.send("\n")

print("Please remember to previously pair your devide to the raspberry bluetooth")
selectDevice()
    
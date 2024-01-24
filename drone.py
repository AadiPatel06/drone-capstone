from codrone_edu.drone import *                                                                                         #all of the imported libarys
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()                                                                                                         #setsup drone and drone pairing
drone.pair()
recording = sr.Recognizer()                                                                                             #sets up mic and recording/makes varibles for the speech recognition libary recognizer and microphone
mic = sr.Microphone()
recording.energy_threshold = 500                                                                                        #sets up energy and pause thresold for recording to be smoother and easier to read in
recording.pause_threshold = 0.5

Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)                                                          #resets drone LEDs incase there still on

#list of commands and methods for later use in recongizing commands from mic
#commands and methods are in the same spots in there lists so you can easily call one from the same index
ListOfCommandsStr = ["fly","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","turn around","attack","get color","get info"]
ListOfCommandsMed = ["DroneTakeoff()","DroneForward()","DroneBackward()","DroneLeftward()","DroneRightward()","DroneUpward()","DroneDownward()","DroneFlip()","DroneLand()","DroneEmergencyStop()","DroneSquare()","DroneSway()","DroneTriangle()","DroneCircle()","DroneSpiral()","DroneTurnLeft()","DroneTurnRight()","DroneTurnAround()","DroneAttack()","DroneGetColor()","DroneInfo()"]

#print statement of commands for user
print("""----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
the list of commands are fly, forward, back, left, right, up, down, flip, land, abort, square, sway, triangle, circle, spiral, negative, positive, turn around, attack, get color, get info. 
by saying these key words the drone will do the command, land-ends the code and fly-starts the drone up. To restart the drone land and then restart the program.
orange means listening to voice, green means doing action, red means action or emergency land or attack command, yellow means wall or floor is detected and is moving away
the first higher pitched beep meaning listening now, the lower pitched beep means stopped listening, beeping while red means emergency landing happened, 
beeping while yellow means wall or floor is detected and is moving away
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------""")


#Drone attack command: goes in a circle looking for a object within 24ins then flys into it
#whgile loop that roatates drone till obnject within 24ins then breaks loop and flys forward and then ends
def DroneAttack():
    print("drone is attacking")
    while True:
        time.sleep(0.1)
        if drone.get_front_range(unit="in") > 24:
            drone.turn(0.2, power=100)
        else:
            break
    for i in range(24):
        drone.move_forward(distance=2, units="in", speed=2)
    time.sleep(2)


#moves drone forward and checks for wall and floor withing a for loop so it can move and check at the same time
def DroneForward():
    print("drone move forward")
    for i in range(30):
        drone.move_forward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


#moves drone backward and checks for wall and floor withing a for loop so it can move and check at the same time
def DroneBackward():
    print("drone move backward")
    for i in range(30):
        drone.move_backward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


#moves drone left and checks for wall and floor withing a for loop so it can move and check at the same time
def DroneLeftward():
    print("drone moves left")
    for i in range(30):
        drone.move_left(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


#moves drone right and checks for wall and floor withing a for loop so it can move and check at the same time
def DroneRightward():
    print("drone moves right")
    for i in range(30):
        drone.move_right(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


#moves drone up and checks for wall and floor withing a for loop so it can move and check at the same time
#is a for loop moving it up and checking for walls and floors and sets throttle and move to move up
def DroneUpward():
    print("drone moves up")
    for i in range(12):
        drone.set_throttle(50)
        drone.move(0.1)
        if drone.detect_wall(distance=60):
            drone.reset_move()
            DroneCheckForWall()
            DroneCheckFixHeight()
    drone.reset_move()


#moves drone down and checks for wall and floor withing a for loop so it can move and check at the same time
#is a for loop moving it down and checking for walls and floors and sets throttle and move to move down
def DroneDownward():
    print("drone moves down")
    for i in range(12):
        drone.set_throttle(-50)
        drone.move(0.1)
        if drone.detect_wall(distance=60):
            drone.reset_move()
            DroneCheckForWall()
            DroneCheckFixHeight()
    drone.reset_move()


#makes the drone flip
def DroneFlip():
    print("drone flip")
    drone.flip()
    time.sleep(3)


#makes the drone land then ends the code
def DroneLand():
    print("drone land")
    drone.land()
    Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
    drone.stop_drone_buzzer()
    time.sleep(2)
    drone.close()
    exit()


#makes the drone takeoff and reset sensor
def DroneTakeoff():
    print("drone takeoff")
    drone.reset_sensor()
    drone.takeoff()


#emergency stop for drone, makes the drone red and stops it and makes a sound
def DroneEmergencyStop():
    print("drone EmergencyStop")
    Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
    drone.emergency_stop()
    for i in range(4):
        drone.drone_buzzer(200, 300)
        drone.drone_buzzer(400, 100)
        drone.drone_buzzer(100, 300)
        Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
        time.sleep(0.5)
    Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


#makes the drone move in a square
def DroneSquare():
    print("moving in square")
    drone.square()
    drone.reset_move()


#makes the drone sway back and forth
def DroneSway():
    print("Drone Swaying")
    drone.sway(speed=100, seconds=0.5)
    drone.reset_move()


#makes the drone move in a triangle
def DroneTriangle():
    print("moving in Triangle")
    drone.triangle()
    drone.reset_move()


#makes the drone move in a circle
def DroneCircle():
    print("moving in Circle")
    drone.circle(speed=50)
    drone.reset_move()


#makes the drone move in a spiral
def DroneSpiral():
    print("moving in Spiral")
    drone.spiral(speed=75, seconds=3)
    drone.reset_move()


#makes the drone turn to the left
def DroneTurnLeft():
    print("Drone Turning Left")
    drone.turn(0.65, power=-100)
    drone.reset_move()


#makes the drone turn to the right
def DroneTurnRight():
    print("Drone Turning Right")
    drone.turn(0.65, power=100)
    drone.reset_move()


#makes the drone turn around
def DroneTurnAround():
    print("Drone Turning Around")
    drone.turn(1.375, power=100)
    drone.reset_move()


#tells you what color the drone is detecting from the front and back and prints it
def DroneGetColor():
    print("Drone getting colors")
    print("drone back color is " + drone.get_back_color())
    print("drone front color is " + drone.get_front_color())


#gives all the info on the drone and prints it out, gives battery, wall distance, bottom distance, flight state, back color, front color, temp,pos for x,y,z and postition data
def DroneInfo():
    print("Getting drone info")
    print("-------------------------------------------------------")
    print("drone battery is at " + str(drone.get_battery()) + "%")
    print("closest wall from front sensor is " + str(drone.get_front_range(unit="in")) + "in")
    if drone.get_bottom_range(unit="in") > 0:
        print("closest floor from bottom sensor is " + str(drone.get_bottom_range(unit="in")) + "in")
    else:
        print("closest floor from bottom sensor is 0 in")
    if drone.get_flight_state() == ModeFlight.Ready:
        print("drones current flight state is Ready")
    else:
        print("drones current flight state is flying")
    print("drone back color is " + drone.get_back_color())
    print("drone front color is " + drone.get_front_color())
    print("temperature is " + str(drone.get_temperature()) + "C")
    print(drone.get_pos_x())
    print(drone.get_pos_y())
    print(drone.get_pos_z())
    print(drone.get_position_data())
    print("-------------------------------------------------------")


#checks for wall and moves if too close
#while loop that runs while wall is too close, if the drone isnt flying yet breaks, else changes the led color to yelloe and then moves away from wall and checks height as well
def DroneCheckForWall():
    while drone.get_front_range() < 60:
        if drone.get_flight_state() == ModeFlight.Ready:
           break
        else:
            Drone.set_drone_LED(r=255, g=255, b=0, brightness=100, self=drone)
            drone.move_backward(distance=2, units="cm", speed=3)
            DroneCheckFixHeight()
    Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)


#checks fir floor and if too close moves up
#while loop that runs while floor is too close, if the dro9ne isnt flying yet breaks, else changes drone color to yellow and moves away and then checks for wall
def DroneCheckFixHeight():
    while drone.get_height(unit="in") < 12:
        if drone.get_flight_state() == ModeFlight.Ready:
            break
        else:
            Drone.set_drone_LED(r=255, g=255, b=0, brightness=100, self=drone)
            drone.set_throttle(50)
            drone.move(0.1)
            drone.reset_move()
            DroneCheckForWall()
    Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)


#a method which runs the bulk of the program, a while lops thats always true repeats though everything
#gives the drone battery and then checks for wall and floor then sets the led to a color to resemble that its listening
def ListeningVoice(self):
    while True:
        print("drone battery is at " + str(drone.get_battery()) + "%")
        DroneCheckForWall()
        DroneCheckFixHeight()
        Drone.set_drone_LED(r=255, g=60, b=0, brightness=100, self=drone)
        print("speak")
        drone.drone_buzzer(1000, 100)                                                                                   #makes a sound to tell user that drone is ready for listening
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(1000, 100)
        drone.drone_buzzer(2000, 100)
        with mic as source:                                                                                             #uses the mic as source to listen for voice and record it as a varible called audio
            audio = recording.record(source, duration=2.5)
        text = str(recording.recognize_google(audio, language='en-IN', show_all=True)).lower()                          #turns the audio into a string and into the varible text by using the recongizer/google language and makes it all lower case
        print(text)                                                                                                     #prints out text so you can see what the program heard for your commands and if its in there and heard the right words
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)                                                  #turns off the led and then makes a sound to show that its done listening
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(250, 100)
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(1000, 100)
        for i in range(len(ListOfCommandsStr)):                                                                         #for loop that repeats the amount of types the lungth of the list of commands list
           if ListOfCommandsStr[i] in text:                                                                             #checks if the index in the list of commands is in the text varible of the recongized audio/what you said
               Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)
               eval(ListOfCommandsMed[i])                                                                               #changes the leds to green to show commands being done and then does the command that was heard at the same index as the method list and does evals it to do the method
               Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


#emergency key which stops the drone from flying
#listens for spce key if so then makes drone leds red and stops the drone, then makes a sound
def EmergencyKey(key):
    if key == Key.space:
        Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
        drone.emergency_stop()
        for i in range(4):
            drone.drone_buzzer(200, 300)
            drone.drone_buzzer(400, 100)
            drone.drone_buzzer(100, 300)
            Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
            time.sleep(0.5)
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


#makes two threads that run the emergency key method and the listeningvoice method
t1 = threading.Thread(target=EmergencyKey, args=(10,))
t2 = threading.Thread(target=ListeningVoice, args=(10,))

#sets the two threads and there methods
t1.start()
t2.start()

#uses a listener for the spce key in the emergency key method
with Listener(on_press=EmergencyKey) as listener:
    listener.join()

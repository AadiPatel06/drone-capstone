from codrone_edu.drone import *
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()
drone.pair()

Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)

ListOfCommandsStr = ["fly","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","turn around","attack"]
ListOfCommandsMed = ["DroneTakeoff()","DroneForward()","DroneBackward()","DroneLeftward()","DroneRightward()","DroneUpward()","DroneDownward()","DroneFlip()","DroneLand()","DroneEmergencyStop()","DroneSquare()","DroneSway()","DroneTriangle()","DroneCircle()","DroneSpiral()","DroneTurnLeft()","DroneTurnRight()","DroneTurnAround()","DroneAttack()"]


def DroneAttack():
    print("drone is attacking")


def DroneForward():
    print("drone move forward")
    for i in range(30):
        drone.move_forward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


def DroneBackward():
    print("drone move backward")
    for i in range(30):
        drone.move_backward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


def DroneLeftward():
    print("drone moves left")
    for i in range(30):
        drone.move_left(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


def DroneRightward():
    print("drone moves right")
    for i in range(30):
        drone.move_right(distance=3, units="cm", speed=2)
        DroneCheckForWall()
        DroneCheckFixHeight()


def DroneUpward():
    print("drone moves up")
    for i in range(12):
        drone.set_throttle(50 )
        drone.move(0.1)
        if drone.detect_wall(distance=60):
            drone.reset_move()
            DroneCheckForWall()
            DroneCheckFixHeight()
    drone.reset_move()


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


def DroneFlip():
    print("drone flip")
    drone.flip()
    time.sleep(3)


def DroneLand():
    print("drone land")
    drone.land()
    Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
    exit()


def DroneTakeoff():
    print("drone takeoff")
    drone.reset_sensor()
    drone.takeoff()


def DroneEmergencyStop():
    print("drone EmergencyStop")
    drone.emergency_stop()


def DroneSquare():
    print("moving in square")
    drone.square()
    drone.reset_move()


def DroneSway():
    print("Drone Swaying")
    drone.sway(speed=100, seconds=0.5)
    drone.reset_move()


def DroneTriangle():
    print("moving in Triangle")
    drone.triangle()
    drone.reset_move()


def DroneCircle():
    print("moving in Circle")
    drone.circle(speed=50)
    drone.reset_move()


def DroneSpiral():
    print("moving in Spiral")
    drone.spiral(speed=75, seconds=3)
    drone.reset_move()


def DroneTurnLeft():
    print("Drone Turning Left")
    drone.turn(0.65, power=-100)
    drone.reset_move()


def DroneTurnRight():
    print("Drone Turning Right")
    drone.turn(0.65, power=100)
    drone.reset_move()


def DroneTurnAround():
    print("Drone Turning Around")
    drone.turn(1.375, power=100)
    drone.reset_move()


def DroneCheckForWall():
    CheckWall = True
    while CheckWall:
        if drone.get_flight_state() == ModeFlight.Ready:
            CheckWall = False
        elif drone.detect_wall(distance=60):
            print("wall detected in range")
            Drone.set_drone_LED(r=255, g=255, b=0, brightness=100, self=drone)
            drone.move_backward(distance=2, units="cm", speed = 3)
            DroneCheckFixHeight()
        else:
            CheckWall = False
            Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)


def DroneCheckFixHeight():
    while drone.get_height(unit="in") < 12:
        if drone.get_flight_state() == ModeFlight.Ready:
            break
        else:
            drone.set_throttle(50)
            drone.move(0.1)
            drone.reset_move()
            DroneCheckForWall()


def ListeningVoice(self):
    recording = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        DroneCheckForWall()
        DroneCheckFixHeight()
        with mic as source:
            Drone.set_drone_LED(r=255, g=60, b=0, brightness=100, self=drone)
            print("speak")
            audio = recording.record(source, duration=2.5)
            recording.energy_threshold = 500
            recording.pause_threshold = 0.5
        text = str(recording.recognize_google(audio, language='en-IN', show_all=True)).lower()
        print(text)
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
        for i in range(len(ListOfCommandsStr)):
           if ListOfCommandsStr[i] in text:
               Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)
               eval(ListOfCommandsMed[i])
               Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


def EmergencyKey(key):
    if key == Key.space:
        Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
        drone.emergency_stop()
        for i in range(4):
            Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
            time.sleep(0.5)


t1 = threading.Thread(target=EmergencyKey, args=(10,))
t2 = threading.Thread(target=ListeningVoice, args=(10,))

t1.start()
t2.start()

with Listener(on_press=EmergencyKey) as listener:
    listener.join()


#buzzer
#attack
#print out all things with drone/height and sensors and everything

from codrone_edu.drone import *
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()
drone.pair()

Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)

ListOfCommandsStr = ["fly","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","turn around","record","begin","attack"]
ListOfCommandsMed = ["DroneTakeoff(RecordingOn, RecordingMoves)","DroneForward(RecordingOn,RecordingMoves)","DroneBackward(RecordingOn, RecordingMoves)","DroneLeftward(RecordingOn,RecordingMoves)","DroneRightward(RecordingOn, RecordingMoves)","DroneUpward(RecordingOn, RecordingMoves)","DroneDownward(RecordingOn, RecordingMoves)","DroneFlip(RecordingOn, RecordingMoves)","DroneLand(RecordingOn, RecordingMoves)","DroneEmergencyStop(RecordingOn, RecordingMoves)","DroneSquare(RecordingOn, RecordingMoves)","DroneSway(RecordingOn, RecordingMoves)","DroneTriangle(RecordingOn, RecordingMoves)","DroneCircle(RecordingOn, RecordingMoves)","DroneSpiral(RecordingOn, RecordingMoves)","DroneTurnLeft(RecordingOn, RecordingMoves)","DroneTurnRight(RecordingOn, RecordingMoves)","DroneTurnAround(RecordingOn, RecordingMoves)","DroneRecord()","DroneBeginRecording(RecordingMoves)","DroneAttack()"]
RecordingMoves = []
RecordingOn = False


def DroneAttack():
    print("drone is attacking")


def DroneForward(RecordingOn,RecordingMoves):
    print("drone move forward")
    for i in range(30):
        drone.move_forward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
    if RecordingOn:
        RecordingMoves.append("forward")
        print("movement added to record: forward")


def DroneBackward(RecordingOn,RecordingMoves):
    print("drone move backward")
    for i in range(30):
        drone.move_backward(distance=3, units="cm", speed=2)
        DroneCheckForWall()
    if RecordingOn:
        RecordingMoves.append("back")
        print("movement added to record: backward")


def DroneLeftward(RecordingOn,RecordingMoves):
    print("drone moves left")
    for i in range(30):
        drone.move_left(distance=3, units="cm", speed=2)
        DroneCheckForWall()
    if RecordingOn:
        RecordingMoves.append("left")
        print("movement added to record: left")


def DroneRightward(RecordingOn,RecordingMoves):
    print("drone moves right")
    for i in range(30):
        drone.move_right(distance=3, units="cm", speed=2)
        DroneCheckForWall()
    if RecordingOn:
        RecordingMoves.append("right")
        print("movement added to record: right")


def DroneUpward(RecordingOn,RecordingMoves):
    print("drone moves up")
    for i in range(12):
        drone.set_throttle(50 )
        drone.move(0.1)
        if drone.detect_wall(distance=60):
            drone.reset_move()
            DroneCheckForWall()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("up")
        print("movement added to record: up")


def DroneDownward(RecordingOn,RecordingMoves):
    print("drone moves down")
    for i in range(12):
        drone.set_throttle(-50)
        drone.move(0.1)
        if drone.detect_wall(distance=60):
            drone.reset_move()
            DroneCheckForWall()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("down")
        print("movement added to record: down")


def DroneFlip(RecordingOn,RecordingMoves):
    print("drone flip")
    drone.flip()
    if RecordingOn:
        RecordingMoves.append("flip")
        print("movement added to record: flip")
    time.sleep(3)


def DroneLand(RecordingOn,RecordingMoves):
    print("drone land")
    drone.land()
    if RecordingOn:
        RecordingMoves.append("land")
        print("movement added to record: land")


def DroneTakeoff(RecordingOn,RecordingMoves):
    print("drone takeoff")
    drone.takeoff()
    if RecordingOn:
        RecordingMoves.append("fly")
        print("movement added to record: fly")


def DroneEmergencyStop(RecordingOn,RecordingMoves):
    print("drone EmergencyStop")
    drone.emergency_stop()
    if RecordingOn:
        RecordingMoves.append("abort")
        print("movement added to record: emergency stop")


def DroneSquare(RecordingOn,RecordingMoves):
    print("moving in square")
    drone.square()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("square")
        print("movement added to record: Square")


def DroneSway(RecordingOn,RecordingMoves):
    print("Drone Swaying")
    drone.sway(speed=100, seconds=0.5)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("sway")
        print("movement added to record: Sway")


def DroneTriangle(RecordingOn,RecordingMoves):
    print("moving in Triangle")
    drone.triangle()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("triangle")
        print("movement added to record: Triangle")


def DroneCircle(RecordingOn,RecordingMoves):
    print("moving in Circle")
    drone.circle(speed=50)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("circle")
        print("movement added to record: Circle")


def DroneSpiral(RecordingOn,RecordingMoves):
    print("moving in Spiral")
    drone.spiral(speed=75, seconds=3)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("spiral")
        print("movement added to record: Spiral")


def DroneTurnLeft(RecordingOn,RecordingMoves):
    print("Drone Turning Left")
    drone.turn(0.65, power=-100)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("negative")
        print("movement added to record: turn left")


def DroneTurnRight(RecordingOn,RecordingMoves):
    print("Drone Turning Right")
    drone.turn(0.65, power=100)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("positive")
        print("movement added to record: turn right")


def DroneTurnAround(RecordingOn,RecordingMoves):
    print("Drone Turning Around")
    drone.turn(1.375, power=100)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("turn around")
        print("movement added to record: turn around")


def DroneRecord():
    global RecordingOn
    global RecordingMoves
    print("recording movements now")
    RecordingOn = True
    RecordingMoves = []
    Drone.set_drone_LED(r=100, g=255, b=200, brightness=100, self=drone)
    time.sleep(2)
    Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


def DroneBeginRecording(RecordingMoves):
    global RecordingOn
    print("drone recording playing")
    print(RecordingMoves)
    RecordingOn = False
    for a in range(len(RecordingMoves)):
        for i in range(len(ListOfCommandsStr)):
            if RecordingMoves[a] in ListOfCommandsStr[i]:
                Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)
                eval(ListOfCommandsMed[i])
                time.sleep(3)
                Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
    RecordingOn = True


def DroneCheckForWall():
    CheckWall = True
    while CheckWall:
        if drone.get_flight_state() == ModeFlight.Ready:
            CheckWall = False
        elif drone.detect_wall(distance=60):
            print("wall dectected in range")
            Drone.set_drone_LED(r=255, g=255, b=0, brightness=100, self=drone)
            drone.move_backward(distance=2, units="cm", speed = 3)
        else:
            CheckWall = False
            Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)


def ListeningVoice(self):
    recording = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        DroneCheckForWall()
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

from codrone_edu.drone import *
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()
drone.pair()
Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
LookingForWall = False

ListOfCommandsStr = ["take off","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","turn around","record","begin"]
ListOfCommandsMed = ["DroneTakeoff(RecordingOn, RecordingMoves)","DroneForward(RecordingOn,RecordingMoves)","DroneBackward(RecordingOn, RecordingMoves)","DroneLeftward(RecordingOn,RecordingMoves)","DroneRightward(RecordingOn, RecordingMoves)","DroneUpward(RecordingOn, RecordingMoves)","DroneDownward(RecordingOn, RecordingMoves)","DroneFlip(RecordingOn, RecordingMoves)","DroneLand(RecordingOn, RecordingMoves)","DroneEmergencyStop(RecordingOn, RecordingMoves)","DroneSquare(RecordingOn, RecordingMoves)","DroneSway(RecordingOn, RecordingMoves)","DroneTriangle(RecordingOn, RecordingMoves)","DroneCircle(RecordingOn, RecordingMoves)","DroneSpiral(RecordingOn, RecordingMoves)","DroneTurnLeft(RecordingOn, RecordingMoves)","DroneTurnRight(RecordingOn, RecordingMoves)","DroneTurnAround(RecordingOn, RecordingMoves)","DroneRecord()","DroneBeginRecording(RecordingMoves)"]
RecordingMoves = []
RecordingOn = False


def DroneForward(RecordingOn,RecordingMoves):
    print("drone move forward")
    drone.move_forward(distance=3, units="ft", speed=1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("forward")
        print("movement added to record: forward")
    time.sleep(2)


def DroneBackward(RecordingOn,RecordingMoves):
    print("drone move backward")
    drone.move_backward(distance=3, units="ft", speed=1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("back")
        print("movement added to record: backward")
    time.sleep(2)


def DroneLeftward(RecordingOn,RecordingMoves):
    print("drone moves left")
    drone.move_left(distance=3, units="ft", speed=1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("left")
        print("movement added to record: left")
    time.sleep(2)


def DroneRightward(RecordingOn,RecordingMoves):
    print("drone moves right")
    drone.move_right(distance=3, units="ft", speed=1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("right")
        print("movement added to record: right")
    time.sleep(2)


def DroneUpward(RecordingOn,RecordingMoves):
    print("drone moves up")
    drone.set_throttle(100)
    drone.move(1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("up")
        print("movement added to record: up")


def DroneDownward(RecordingOn,RecordingMoves):
    print("drone moves down")
    drone.set_throttle(-100)
    drone.move(1)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("down")
        print("movement added to record: down")


def DroneFlip(RecordingOn,RecordingMoves):
    print("drone flip")
    drone.flip()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("flip")
        print("movement added to record: flip")
    time.sleep(2)


def DroneLand(RecordingOn,RecordingMoves):
    global LookingForWall
    LookingForWall = False
    print("drone land")
    drone.land()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("land")
        print("movement added to record: land")


def DroneTakeoff(RecordingOn,RecordingMoves):
    global LookingForWall
    LookingForWall = True
    print("drone takeoff")
    drone.takeoff()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("take off")
        print("movement added to record: takeoff")


def DroneEmergencyStop(RecordingOn,RecordingMoves):
    global LookingForWall
    LookingForWall = False
    print("drone EmergencyStop")
    Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
    drone.emergency_stop()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("abort")
        print("movement added to record: emergency stop")
    for i in range(4):
        Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
        time.sleep(0.5)


def DroneSquare(RecordingOn,RecordingMoves):
    print("moving in square")
    drone.square()
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("square")
        print("movement added to record: Square")


def DroneSway(RecordingOn,RecordingMoves):
    print("Drone Swaying")
    drone.sway(speed=100,seconds=0.5)
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
    drone.circle(speed=100)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("circle")
        print("movement added to record: Circle")


def DroneSpiral(RecordingOn,RecordingMoves):
    print("moving in Spiral")
    drone.spiral(speed=75,seconds=2)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("spiral")
        print("movement added to record: Spiral")


def DroneTurnLeft(RecordingOn,RecordingMoves):
    print("Drone Turning Left")
    drone.turn_left(45)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("negative")
        print("movement added to record: turn left")


def DroneTurnRight(RecordingOn,RecordingMoves):
    print("Drone Turning Right")
    drone.turn_right(45)
    drone.reset_move()
    if RecordingOn:
        RecordingMoves.append("positive")
        print("movement added to record: turn right")


def DroneTurnAround(RecordingOn,RecordingMoves):
    print("Drone Turning Around")
    drone.turn_right(180)
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
    for a in range(len(RecordingMoves)):
        for i in range(len(ListOfCommandsStr)):
            RecordingOn = False
            if RecordingMoves[a] in ListOfCommandsStr[i]:
                Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)
                eval(ListOfCommandsMed[i])
                Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
            RecordingOn = True


def EmergencyKey(key):
    global LookingForWall
    LookingForWall = False
    if key == Key.space:
        Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
        drone.emergency_stop()
        for i in range(4):
            Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
            time.sleep(0.5)


def DroneDectectingWall(self):
    global LookingForWall
    while True:
        while LookingForWall:
            if drone.detect_wall() == True:
                drone.move_backward(distance=10)


def ListeningVoice(self):
    recording = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            print("speak")
            Drone.set_drone_LED(r=255, g=60, b=0, brightness=100, self=drone)
            audio = recording.record(source, duration=2.5)
            recording.energy_threshold = 500
            recording.pause_threshold = 0.5
        text = str(recording.recognize_google(audio, language='en-IN', show_all=True)).lower()
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
        print(text)
        for i in range(len(ListOfCommandsStr)):
            if ListOfCommandsStr[i] in text:
                Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)
                eval(ListOfCommandsMed[i])
                Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


t1 = threading.Thread(target=EmergencyKey, args=(10,))
t2 = threading.Thread(target=ListeningVoice, args=(10,))
t3 = threading.Thread(target=DroneDectectingWall, args=(10,))

t1.start()
t2.start()
t3.start()

with Listener(on_press=EmergencyKey) as listener:
    listener.join()

#dectect wall needs to be tested
#try out keep distance

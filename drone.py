from codrone_edu.drone import *
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()
drone.pair()

ListOfCommandsStr = ["take off","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","180","record","begin"]
ListOfCommandsMed = ["DroneTakeoff(RecordingOn, RecordingMoves)","DroneForward(RecordingOn,RecordingMoves)","DroneBackward(RecordingOn, RecordingMoves)","DroneLeftward(RecordingOn,RecordingMoves)","DroneRightward(RecordingOn, RecordingMoves)","DroneUpward(RecordingOn, RecordingMoves)","DroneDownward(RecordingOn, RecordingMoves)","DroneFlip(RecordingOn, RecordingMoves)","DroneLand(RecordingOn, RecordingMoves)","DroneEmergencyStop(RecordingOn, RecordingMoves)","DroneSquare(RecordingOn, RecordingMoves)","DroneSway(RecordingOn, RecordingMoves)","DroneTriangle(RecordingOn, RecordingMoves)","DroneCircle(RecordingOn, RecordingMoves)","DroneSpiral(RecordingOn, RecordingMoves)","DroneTurnLeft(RecordingOn, RecordingMoves)","DroneTurnRight(RecordingOn, RecordingMoves)","DroneTurn180(RecordingOn, RecordingMoves)","DroneRecord()","DroneBeginRecording(RecordingMoves)"]
RecordingMoves = []
RecordingOn = False


def DroneForward(RecordingOn,RecordingMoves):
    print("drone move forward")
    drone.move_forward(distance=3, units="ft", speed=1)
    if RecordingOn:
        RecordingMoves.append("forward")
        print("movement added to record: forward")


def DroneBackward(RecordingOn,RecordingMoves):
    print("drone move backward")
    drone.move_backward(distance=3, units="ft", speed=1)
    if RecordingOn:
        RecordingMoves.append("back")
        print("movement added to record: backward")


def DroneLeftward(RecordingOn,RecordingMoves):
    print("drone moves left")
    drone.move_left(distance=3, units="ft", speed=1)
    if RecordingOn:
        RecordingMoves.append("left")
        print("movement added to record: left")


def DroneRightward(RecordingOn,RecordingMoves):
    print("drone moves right")
    drone.move_right(distance=3, units="ft", speed=1)
    if RecordingOn:
        RecordingMoves.append("right")
        print("movement added to record: right")


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
    if RecordingOn:
        RecordingMoves.append("flip")
        print("movement added to record: flip")


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
        RecordingMoves.append("take off")
        print("movement added to record: takeoff")


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
    if RecordingOn:
        RecordingMoves.append("negative")
        print("movement added to record: turn left")


def DroneTurnRight(RecordingOn,RecordingMoves):
    print("Drone Turning Right")
    drone.turn_right(45)
    if RecordingOn:
        RecordingMoves.append("positive")
        print("movement added to record: turn right")


def DroneTurn180(RecordingOn,RecordingMoves):
    print("Drone Turning 180")
    drone.turn_right(180)
    if RecordingOn:
        RecordingMoves.append("180")
        print("movement added to record: turn 180")


def DroneRecord():
    global RecordingOn
    global RecordingMoves
    print("recording movements now")
    RecordingOn = True
    RecordingMoves = []


def DroneBeginRecording(RecordingMoves):
    global RecordingOn
    print("drone recording playing")
    print(RecordingMoves)
    for a in range(len(RecordingMoves)):
        for i in range(len(ListOfCommandsStr)):
            RecordingOn = False
            if RecordingMoves[a] in ListOfCommandsStr[i]:
                eval(ListOfCommandsMed[i])
                time.sleep(2)
            RecordingOn = True


def show(key):
  if key == Key.space:
    drone.emergency_stop()


def ListeningVoice(self):
    recording = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            print("speak")
            audio = recording.record(source, duration=2.5)
            recording.energy_threshold = 500
            recording.pause_threshold = 0.5
        text = str(recording.recognize_google(audio, language='en-IN', show_all=True)).lower()
        print(text)
        for i in range(len(ListOfCommandsStr)):
            if ListOfCommandsStr[i] in text:
                eval(ListOfCommandsMed[i])


t1 = threading.Thread(target=show, args=(10,))
t2 = threading.Thread(target=ListeningVoice, args=(10,))

t1.start()
t2.start()

with Listener(on_press=show) as listener:
    listener.join()

#dection for all around
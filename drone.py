from codrone_edu.drone import *
from pynput.keyboard import Key, Listener
import threading
import speech_recognition as sr
import time

drone = Drone()
drone.pair()
recording = sr.Recognizer()
mic = sr.Microphone()
recording.energy_threshold = 500
recording.pause_threshold = 0.5

Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)

ListOfCommandsStr = ["fly","forward","back","left","right","up","down","flip","land","abort","square","sway","triangle","circle","spiral","negative","positive","turn around","attack","get color","get info"]
ListOfCommandsMed = ["DroneTakeoff()","DroneForward()","DroneBackward()","DroneLeftward()","DroneRightward()","DroneUpward()","DroneDownward()","DroneFlip()","DroneLand()","DroneEmergencyStop()","DroneSquare()","DroneSway()","DroneTriangle()","DroneCircle()","DroneSpiral()","DroneTurnLeft()","DroneTurnRight()","DroneTurnAround()","DroneAttack()","DroneGetColor()","DroneInfo()"]

print("""----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
the list of commands are fly, forward, back, left, right, up, down, flip, land, abort, square, sway, triangle, circle, spiral, negative, positive, turn around, attack, get color, get info. 
by saying these key words the drone will do the command, land-ends the code and fly-starts the drone up. To restart the drone land and then restart the program.
orange means listening to voice, green means doing action, red means action or emergency land or attack command, yellow means wall or floor is detected and is moving away
the first higher pitched beep meaning listening now, the lower pitched beep means stopped listening, beeping while red means emergency landing happened, 
beeping while yellow means wall or floor is detected and is moving away
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------""")


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
    drone.stop_drone_buzzer()
    time.sleep(2)
    drone.close()
    exit()


def DroneTakeoff():
    print("drone takeoff")
    drone.reset_sensor()
    drone.takeoff()


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


def DroneGetColor():
    print("Drone getting colors")
    print("drone back color is " + drone.get_back_color())
    print("drone front color is " + drone.get_front_color())


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


def DroneCheckForWall():
    while drone.get_front_range() < 60:
        if drone.get_flight_state() == ModeFlight.Ready:
           break
        else:
            Drone.set_drone_LED(r=255, g=255, b=0, brightness=100, self=drone)
            drone.move_backward(distance=2, units="cm", speed=3)
            DroneCheckFixHeight()
    Drone.set_drone_LED(r=0, g=255, b=0, brightness=100, self=drone)


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


def ListeningVoice(self):
    while True:
        print("drone battery is at " + str(drone.get_battery()) + "%")
        DroneCheckForWall()
        DroneCheckFixHeight()
        Drone.set_drone_LED(r=255, g=60, b=0, brightness=100, self=drone)
        print("speak")
        drone.drone_buzzer(1000, 100)
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(1000, 100)
        drone.drone_buzzer(2000, 100)
        with mic as source:
            audio = recording.record(source, duration=2.5)
        text = str(recording.recognize_google(audio, language='en-IN', show_all=True)).lower()
        print(text)
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(250, 100)
        drone.drone_buzzer(500, 100)
        drone.drone_buzzer(1000, 100)
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
            drone.drone_buzzer(200, 300)
            drone.drone_buzzer(400, 100)
            drone.drone_buzzer(100, 300)
            Drone.set_drone_LED(r=255, g=0, b=0, brightness=100, self=drone)
            time.sleep(0.5)
        Drone.set_drone_LED(r=0, g=0, b=0, brightness=100, self=drone)


t1 = threading.Thread(target=EmergencyKey, args=(10,))
t2 = threading.Thread(target=ListeningVoice, args=(10,))

t1.start()
t2.start()

with Listener(on_press=EmergencyKey) as listener:
    listener.join()

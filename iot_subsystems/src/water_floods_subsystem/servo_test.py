from gpiozero import AngularServo
import time

servo = AngularServo(12, min_angle=0, max_angle=180, initial_angle=0)

print("Moving to 90°")
servo.angle = 90
time.sleep(2)

print("Moving to 0°")
servo.angle = 0
time.sleep(2)

print("Moving to 180°")
servo.angle = 180
time.sleep(2)

servo.detach()

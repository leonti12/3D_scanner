from motor_control import StepperSerial

step = StepperSerial("/dev/ttyESP", 115200, 2.0, 1.0)

while True:
    step.step()
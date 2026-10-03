# scan.py
from picamera2 import Picamera2
from pic_proccessing import StegerExtractor
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.set_controls({"AeEnable": False, "ExposureTime": 5000, "AnalogueGain": 1.0})



picam2.start()

start = time.time_ns()

steger = StegerExtractor(threshold=40)

frame = picam2.capture_array()
pts = steger.process(frame)
end = time.time_ns()


print(f"the proccess took {(end-start)/1e6:.2f} ms")


print(f"Steger: {len(pts)} points in {steger.last_time_ms:.2f} ms")

picam2.stop()
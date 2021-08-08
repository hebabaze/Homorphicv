import sys
import time 
from kafka import KafkaProducer 
import numpy as np 
import cv2 


# Define the codec and create VideoWriter object (note isColor is False for Gray) 
fourcc = cv2.VideoWriter_fourcc(*'DIVX') 
#fourcc = cv2.CV_FOURCC('M','P','E','G')
#out = cv2.VideoWriter('output.avi', fourcc, 10.0, (1280, 720)) 
out = cv2.VideoWriter('motiondetect.avi',fourcc, 30.0, (1280,720), isColor = False) 

foreground = cv2.createBackgroundSubtractorMOG2(detectShadows =False) 
topic="kafka_video" 
def publish_video(video_file):
  #run producer.py
  producer = KafkaProducer(bootstrap_servers='localhost:9092')
  #define videoCapture
  cap= cv2.VideoCapture(video_file)
  print('publishing video ...')
  while(cap.isOpened()):
    success,camframe=cap.read()
    #make sure it works
    if not success:
      print("bad read!")
      break
    # Convert image to jpg
    ret, buffer= cv2.imencode('.jpg', camframe)
    #break them up into bytes for kafka
    producer.send(topic, buffer.tobytes())
    time.sleep(0.2)
  cap.release()
  print('end of stream') 

def publish_camera():
  #run producer.py
  producer = KafkaProducer(bootstrap_servers='localhost:9092')
  camera= cv2.VideoCapture(0)
  camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  camera.set(cv2.CAP_PROP_FPS,30)
  try:
    while(True):
      success,camframe=camera.read()
      grayframe = cv2.cvtColor(camframe, cv2.COLOR_BGR2GRAY)
      blurframe = cv2.GaussianBlur(camframe, (5, 5), 0)
      #Capture motion
      motionframe = foreground.apply(grayframe)
      detect = (np.sum(motionframe))//255
      if detect > 30:
        print("object in motion size = ", detect)
        # Save stream to .avi file
        out.write(grayframe)
      ret, buffer = cv2.imencode('.jpg',grayframe)
      producer.send(topic, buffer.tobytes())
      # give some time for processing
      time.sleep(0.2)
  except:
    print("\nWe are done.")
    sys.exit(1)
  camera.release()
  out.release() 

if __name__ == '__main__' :
  if (len(sys.argv) > 1):
    video_path = sys.argv[1]
    publish_video(video_path)
  else :
    print("we are live ") 
publish_camera() 


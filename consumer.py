#Code Jdid Consumer
import datetime 
from flask import Flask, Response 
from kafka import KafkaConsumer 
#start consumper.py 
#importing the topic for the apache kafka so it can communicate with the #producer 
topic="kafka_video" 
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092']) 
# Get the flask app ready for view 
app = Flask(__name__)
@app.route('/video',methods=['GET']) 
#this function takes the stream function  
def video():
  return Response(get_video_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

#for each message on the consumer puts all the frames all together again and #creates an image on the video stream  
def get_video_stream():
  for msg in consumer:
    yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')
if __name__ == "__main__":
  app.run(host='0.0.0.0' , debug=True) 
  #Done

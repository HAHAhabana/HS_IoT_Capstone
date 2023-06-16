import time
import math
import random
import subprocess
import numpy as np
import tensorflow as tf
import pandas as pd
import RPi.GPIO as GPIO

from mpu6050 import mpu6050




mpu = mpu6050(0x68)

#부저의 gpio핀을 17로 선언
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

#부저 작동 함수(pm) 
def buzzer_on():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer_pin, GPIO.LOW)
#부저 작동 함수(moto)
def buzzer_on_2():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer_pin, GPIO.LOW)
    

model = tf.keras.models.load_model('Acc_LSTM.h5')

#크기 50인 일반 배열 선언
data_array = [0]*50

#count를 0으로 선언
count = 0




while True:
    
    
    #data_array[49]까지 0.3초마다 종합가속도를 측정하고 측정값을 data_array[i]에 넣는다.
    while count < 50:
        acc_data = mpu.get_accel_data()
        acc_x = round(acc_data["x"], 2) 
        acc_y = round(acc_data["y"], 2)
        acc_z = round(acc_data["z"], 2)

        
        acc = math.sqrt((acc_x**2) + (acc_y**2) + (acc_z**2))-9.8
        
        
        data_array[count] = round(acc, 2)
        count += 1

        time.sleep(0.3)
        
        
    #random값 i를 10~40 사이에서 구한다.
    i = random.randint(10,40)
    
    #data_array[i:i+10]를 input_data에 넣고 이를 LSTM 모델에 입력값으로 넣을 수 있게 가공
    input_data = data_array[i:i+10]
    input_data = np.array(input_data)
    input_data = input_data.reshape((1,10,1))
    
    
   #입력값에 대한 예측 진행
    p = model.predict(input_data)
    
    
    print(p)
    print(input_data)
    
    #만약 예측값이 0.5 이상이면 'buzzer_on_2()'과 'subprocess.Popen(["python3", "/home/hansung/YOLOv5_Version_MOTO.py"])'을 실행
    if(p[0] > 0.5):
        buzzer_on_2()
        subprocess.Popen(["python3", "/home/hansung/YOLOv5_Version_MOTO.py"])
    #만약 예측값이 0.5 이하면 'buzzer_on()'과 'subprocess.Popen(["python3", "/home/hansung/YOLOv5_Version_PM.py"])'을 실행
    else:
       buzzer_on()
       subprocess.Popen(["python3", "/home/hansung/YOLOv5_Version_PM.py"])
        
    GPIO.cleanup()
    break




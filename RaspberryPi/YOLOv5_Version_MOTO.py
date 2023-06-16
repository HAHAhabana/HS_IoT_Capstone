import torch
import cv2
import RPi.GPIO as GPIO
import time

#부저의 gpio핀을 17로 설정
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

#로컬에 존재하는 yolov5의 모델을 로드
model = torch.hub.load('./','custom', 'JIKIDU.pt', source='local')

#카메라모듈을 오픈
img = cv2.VideoCapture(0)

#count를 0으로 초기화
count = 0

#부저 관련 함수
def buzzer_on():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    
def buzzer_off():
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(1)
    
    print("start MOTO_Version")
    
while True:
    
    #프레임 값을 읽어온다. (ret는 불리언값)
    ret, frame = img.read()
    
    #frame에 대한 yolov5 결과를 results에 저장
    results = model(frame)
    
    #pandas 데이터프레임으로 변환하고 객체의 정보를 results_str에 문자열로 저장
    results_str =''
    for results in results.pandas().xyxy[0].values:
        results_str += f"{results}\n"
        
        
    print(results_str)
    
    #만약 'results_str' 안에 'Road'라는 클래스가 존재하면 count를 0으로 초기화
    if "Road" in results_str:
        count = 0
        print(count)
    
    #'Road'가 존재하지 않는다면 count를 1 증가
    else:
        count += 1
        print(count)
    
    # count가 10 이상이라면 buzzer_on() 실행
    if count >= 10:
        buzzer_on()
        print("yolo!")
    #count가 10 미만이라면 buzzer_off() 실행
    else:
        buzzer_off()
        print("off")
    
    #해당 코드는 백그라운드에서 실행하고자 하면 사용하면 안됨
    #cv2.imshow("Frame", frame)
    #cv2.waitKey(100)
        
    

img.release()
cv2.destroyAllWindows()




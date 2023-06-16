import subprocess
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from bluetooth import *

#SPI 통신 객체 spi를 생성
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

#디지털 입출력 객체 cs를 생성
cs = digitalio.DigitalInOut(board.CE0)
#mcp 객체 생성
mcp = MCP.MCP3008(spi, cs)

#아날로그 입력 채널 설정
channel = AnalogIn(mcp, MCP.P0)

#아날로그 채널의 값을 읽는 함수
def read_data():
    
        return channel.value

#RFCOMM 프로토콜을 사용하는 서버쪽 블루투스 객체를 생성
server_socket = BluetoothSocket(RFCOMM)

#Port를 1로 선언하고 서버 소켓이 모든 네트워크 인터페이스와 포트 1로 통신할 수 있게 바인딩하고 연결을 기다림
port = 1
server_socket.bind(("", port))
server_socket.listen(1)

print("waiting.....")

#클라이언트의 블루투스 연결을 수락
client_socket, address = server_socket.accept()
print("Accepted connection from", address)

#블루투스 연결 시, 'subprocess.Popen(["python3", "/home/hansung/Acceleration_DeepLearning.py"])'실행
client_socket.send("Bluetooth connection!")
subprocess.Popen(["python3", "/home/hansung/Acceleration_DeepLearning.py"])



#0.5초마다 아날로그 데이터를 읽어와 아날로그 값이 600을 초과하면 클라이언트로 신호를 전송
while True:
    result = read_data()
    if(result > 600):
        print("warning!")
        client_socket.send(str(result))
        print("send")
    time.sleep(0.5)
        
    
    
    
client_socket.close()
server_socket.close()
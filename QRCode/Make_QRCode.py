import qrcode

#라즈베리파이의 블루투스 MAC 주소
bluetooth_address = 'E4:5F:01:76:D7:34'

#QR코드 객체를 라이브러리에서 생성한다. 이때 버전은 1이고 모듈 박스의 크기는 10, 여백은 4로 설정한다.
qr = qrcode.QRCode(version=1, box_size=10, border=4)
#QR코드 객체에 라즈베리파이의 블루투스 MAC 주소를 넣는다.
qr.add_data(bluetooth_address)
#QR 객체를 생성한다. 이때, 크기는 자동으로 조정한다.
qr.make(fit=True)

#QR코드의 색을 흑백으로 한다.
img = qr.make_image(fill_color='black', back_color='white')

#생성된 QR코드를 저장한다.
img.save("QRCode_Bluetooth_MAC_Address.png")
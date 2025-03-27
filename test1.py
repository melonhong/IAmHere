import time # 기다리기를 위해 참조
from pyfingerprint.pyfingerprint import PyFingerprint # 지문인식 라이브러리
try:
    f = PyFingerprint('/dev/ttyAMA0',57600, 0xFFFFFFFF, 0x00000000) # 지문인식센서와 통신
    if(f.verifyPassword() == False):
        raise ValueError('Password wrong!')
except Exception as e:
    print(str(e))
    exit(1)

try:
    print('지문을 저장합니다... 손가락을 대주세요...') # 지문 기다리기 안내
    while(f.readImage() == False): # 지문 인식될때까지 기다리기
        pass
    f.convertImage(0x01) # 인식 된 지문을 버퍼 0x01 주소에 저장
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8') # 0x01에 저장된 값을 문자열로 변환
    print(characterics) # 문자열로 변환한 지문 값을 출력
except Exception as e:
    print('error')
    print(str(e))
    exit(1)

time.sleep(1)

try:
    print('저장한 지문과 대조해봅니다... 손가락을 대주세요...') # 위에서 인식한 지문과 일치한지 검사 시작
    while(f.readImage() == False): # 지문 인식 기다리기
        pass
    f.convertImage(0x01) # 인식 된 지문을 버퍼 0x01주소에 저장
    print(f.uploadCharacteristics(0x02,eval(characterics))) # 이전에 입력한 지문을 0x02주소에 넣고 출력
    score = f.compareCharacteristics() # 0x01 지문과 0x02 주소의 지문을 비교

    if score >= 60:
        print('지문이 일치합니다!')
    else:
        print('지문이 일치하지 않습니다!')
    print(score) # 일치율 출력
except Exception as e:
    print('error')
    print(str(e))
    exit(1)

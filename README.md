# 🛰IAmHere – IoT 기반 스마트 출석 시스템

> 라즈베리파이와 지문 인식 센서, 블루투스 통신을 활용한 자동 출석 시스템입니다.  
> 출석 시간을 단축하고 정확도를 높이기 위한 IoT 기반 솔루션입니다.

## 📌 프로젝트 소개

**IAmHere**는 지문 인식 센서와 Raspberry Pi, 블루투스 통신을 이용하여  
출석을 자동으로 처리하는 시스템입니다.**

- 강의자의 기기와 블루투스 연결하여 출석 시작
- 강의자의 기기와 연결이 끊길 때까지 학생의 기기를 블루투스 탐지하여 출석 처리
- 블루투스 탐지가 되지 않은 학생은 강의 종료 시 지문 인식으로 출석 처리

## 🛠️ 사용 기술 (Tech Stack)

- **하드웨어**
  - Raspberry Pi 4
  - 지문 인식 센서 (JB-101B)
  - 블루투스 모듈 내장

- **소프트웨어**
  - Python 3.8+
  - RPi.GPIO
  - `pyserial`, `bluetoothctl`, `requests` 등

- **통신**
  - GPIO 통신 (센서 ↔ 라즈베리파이)
  - Bluetooth (기기 근접 확인)
  - REST API (출석 정보 서버 전송)

## 👀 데모 영상
[IAmHere 시연 영상](https://youtu.be/DxXN-7ntfTQhttps://youtu.be/DxXN-7ntfTQ)

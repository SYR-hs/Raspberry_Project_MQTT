import paho.mqtt.client as mqtt                  # MQTT 통신을 지원하는 paho-mqtt 라이브러리의 클라이언트 클래스.
import time                                      # 프로그램 실행 중 일정 시간 대기(sleep) 기능을 사용하기 위한 모듈.
from gpiozero import LED                         # 라즈베리파이의 GPIO 핀에 연결된 LED 하드웨어를 제어하기 위한 클래스.
import threading                                 # 메인 루프와 동시에 실행될 별도의 백그라운드 작업 흐름을 생성하기 위한 모듈.

greenLed = LED(16)                               # GPIO 16번 핀을 제어할 초록색 LED 객체를 생성.
blueLed = LED(20)                                # GPIO 20번 핀을 제어할 파란색 LED 객체를 생성.
redLed = LED(21)                                 # GPIO 21번 핀을 제어할 빨간색 LED 객체를 생성.

def on_message(client, userdata, msg):           # MQTT 브로커로부터 메시지가 수신되었을 때 자동으로 실행되는 콜백 함수를 정의.
    print(msg.topic+" "+str(msg.payload))        # 메시지가 도착한 토픽 이름과 수신된 실제 데이터를 터미널에 출력.
    message = msg.payload.decode()               # 바이트(byte) 형태로 수신된 데이터 내용을 파이썬에서 처리 가능한 문자열로 변환.
    print(message)                               # 변환된 문자열 메시지를 다시 한 번 출력하여 내용을 확인.
    if message == "green_on":                    # 수신된 메시지가 "green_on" 문자열인 경우
        greenLed.on()                            # 초록색 LED를 점등.
    elif message == "green_off":                 # 수신된 메시지가 "green_off" 문자열인 경우
        greenLed.off()                           # 초록색 LED를 소등.
    elif message == "blue_on":                   # 수신된 메시지가 "blue_on" 문자열인 경우
        blueLed.on()                             # 파란색 LED를 점등.
    elif message == "blue_off":                  # 수신된 메시지가 "blue_off" 문자열인 경우
        blueLed.off()                            # 파란색 LED를 소등.
    elif message == "red_on":                    # 수신된 메시지가 "red_on" 문자열인 경우
        redLed.on()                              # 빨간색 LED를 점등.
    elif message == "red_off":                   # 수신된 메시지가 "red_off" 문자열인 경우
        redLed.off()                             # 빨간색 LED를 소등.

client = mqtt.Client()                           # MQTT 통신을 담당할 클라이언트 인스턴스 객체를 생성.
client.on_message = on_message                   # 수신된 메시지 처리를 위해 정의한 on_message 함수를 클라이언트의 콜백으로 등록.

broker_address="192.xxx.xxx.xxx"                 # 통신 중개 역할을 수행할 MQTT 브로커 서버(라즈베리파이)의 IP 주소를 설정.
client.connect(broker_address)                   # 설정된 IP 주소의 브로커 서버에 연결을 시도.
client.subscribe("led",1)                        # "led"라는 이름의 토픽을 구독(수신) 등록하며, QoS 단계를 1로 설정하여 최소 1회 전달을 보장받기.

count = 0                                        # 브로커로 보낼 숫자의 초기값을 0으로 설정.
def send_thread():                               # 주기적으로 데이터를 발행(Publish)하기 위한 스레드 전용 함수를 정의.
    global count                                 # 함수 밖에서 선언된 count 변수를 가져와서 수정하기 위해 전역 변수로 선언.
    while 1:                                     # 프로그램이 작동하는 동안 무한히 반복.
        count = count + 1                        # count 값을 1씩 증가.
        client.publish("hello", str(count))      # "hello"라는 토픽으로 현재 count 값을 문자열로 변환하여 서버에 전송(발행).
        time.sleep(1.0)                          # 다음 전송까지 1초 동안 실행을 일시 정지.

task = threading.Thread(target = send_thread)    # send_thread 함수를 별도의 실행 흐름(스레드)으로 지정.
task.start()                                     # 백그라운드 스레드를 시작하여 주기적인 숫자 데이터 전송을 개시.

client.loop_forever()                            # 메인 루프를 실행하여 브로커와의 연결을 유지하고 수신되는 제어 메시지를 실시간으로 대기.

import socket
import threading
import requests
import os

host = input("서버 ip입력: ") #ip입력 받음
port = 7385

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port)) #클라이언트 소켓을 생성하고 ip와 포트를 사용하여 서버 연결

#서버에서 데이터 수신 및 출력
def recieve_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print(repr(data.decode()))

# 별도의 스레드에서 데이터 수신 및 출력 실행
threading.Thread(target=recieve_data, args=(client_socket,)).start()

print("서버 연결됨")
ip = requests.get("http://ip.jsontest.com").json()['ip'] #외부 ip(닉네임 표시용)
ip_short = ip[:ip.rfind('.')][:ip[:ip.rfind('.')].rfind('.')]

nickname = input("닉네임 입력: ") #닉네임 입력 받음

while True:
    message = input()
    if message == "quit": #quit 입력 시 종료
        break

    full_message = f"{nickname}({ip_short}): {message}"
    client_socket.send(full_message.encode()) #quit가 아니면 메시지 전송

client_socket.close()
os.system('pause') #종료 후 사라짐 방지

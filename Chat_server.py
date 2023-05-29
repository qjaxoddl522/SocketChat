import socket
import threading
import time

client_sockets = [] #클라이언트 소켓 정보 리스트

#host = socket.gethostbyname(socket.gethostname()) #ip 담기
host = '192.168.0.11' #공유기 ip 175.204.6.51
port = 7385

#새로운 클라이언트 접속시 새로운 스레드 생성
def participants(client_socket, address):
    time.sleep(0.1)
    print("연결됨: ", address[0], ":", address[1])

    #연결 끊기기까지의 과정
    while True:
        try:
            data = client_socket.recv(1024) #recv()를 실행하면 소켓에 메시지가 실제로 수신될 때까지 파이썬 코드는 대기

            if not data:
                print("연결 끊김: ", address[0], ":", address[1], data.decode())

            #클라이언트끼리 채팅
            for client in client_sockets:
                if client != client_socket:
                    client.send(data)
        except ConnectionResetError as e:
            print("연결 끊김: ", address[0], ":", address[1])
            break

    #참가자 제거 후 소켓 삭제
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print("제거 후 참가자 수: ", len(client_sockets))

    client_socket.close()

print("내부 ip: ", host)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #서버 소켓 담기
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port)) #ip와 포트 설정

server_socket.listen() #클라이언트 접속 요청 대기

try:
    while True:
        client_socket, address = server_socket.accept() #클라이언트 연결 대기
        client_sockets.append(client_socket)
        threading.Thread(target=participants, args=(client_socket, address)).start()
        print("참가자 수: ", len(client_sockets))
except Exception as e:
    print("ERROR: ", e)
finally:
    server_socket.close()

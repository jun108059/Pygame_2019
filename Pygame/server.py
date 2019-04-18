from socket import *

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 8081))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속이 확인되었습니다.')

data = connectionSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

if data.decode('utf-8') == 'hochan':
    connectionSock.send('success'.encode('utf-8'))
else:
    connectionSock.send('fail'.encode('utf-8'))

print('메시지를 보냈습니다.')

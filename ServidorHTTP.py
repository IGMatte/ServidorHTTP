import socket

host, porta = 'localhost', 8000
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_servidor.bind((host, porta))

socket_servidor.listen(1)
 
print('Servidor ouvindo na porta: ', porta)
 
while True:
    conexao, endereco = socket_servidor.accept()
    requisicao = conexao.recv(1024).decode('utf-8')
	
    lista_string = requisicao.split(' ')
    metodo = lista_string[0]
    print('Método utilizado: ' + metodo)
    requisicao_arquivo = lista_string[1]
    print('Arquivo solicitado: ', requisicao_arquivo)
 
    arquivo = requisicao_arquivo.split(' ')[0]
    arquivo = arquivo.lstrip('/')
    if(arquivo == ''):
        arquivo = 'index.html'
 
    try:
        arquivo_byte = open(arquivo, 'rb')
        resposta = arquivo_byte.read()
        arquivo_byte.close()
 
        header = 'HTTP/1.1 200 OK\n'
 
        if(arquivo.endswith(".jpg")):
            print(arquivo + " é image/jpg")
            extensao = 'image/jpg'
        elif(arquivo.endswith(".png")):
            print(arquivo + " é image/png")
            extensao = 'image/png'
        else:
            print(arquivo + " é text/html")
            extensao = 'text/html'
 
        header += 'Content-Type: '+str(extensao)+'\n\n'
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        resposta = '<html><body><center><h3>Erro 404: Arquivo não encontrado</h3><p>Servidor HTTP</p></center></body></html>'.encode('utf-8')
 
    resposta_final = header.encode('utf-8')
    resposta_final += resposta
    conexao.send(resposta_final)
    conexao.close()
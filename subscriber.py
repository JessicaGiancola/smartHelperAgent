import redis
import requests as req
from switchcase import switch
import time

# Canale su cui il MAS invia i messaggi
CH_IN = 'RESPONSE'
SEPARATOR = '_'


# Svuota la lista dei messaggi inviati dal MAS
def clearList(redisInstance, channel):
    for i in range(0, redisInstance.llen(channel)):
        redisInstance.lpop(channel)
    return


def sendResponse(message, nome):
    # Elaboro la risposta e la invio al database
    splitted_message = message.split(SEPARATOR)
    urlbase = "http://www.lorenzodelauretis.it/tesi/index.php?"
    to_send = ""
    for case in switch(splitted_message[0]):
        if case('misura'):
            to_send = "Devi misurare " + splitted_message[1]
            break
        if case('medicina'):
            to_send = "remindermedicina=1&nome=" + nome.replace(" ", "%20") + "&nomemedicina=" + splitted_message[1] + "&quantita=" + splitted_message[2] + "&message=Devi prendere la medicina " + splitted_message[1] + " quantita " + splitted_message[2]
        else:
            print('Risposta non valida')

    to_send_url = to_send.replace(" ", "%20")
    url = urlbase + to_send_url
    #url = "http://localhost/prova.php?message=" + to_send_url
    print(url)
    req.get(url)
    
    return


def run(nome):
    R = redis.Redis()
    clearList(R, CH_IN)

    while True:
        response = R.lpop(CH_IN)
        if response:
            # Ho ricevuto un messaggio
            sendResponse(response.decode('utf-8'), nome)
            print(response.decode('utf-8'))


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        nome = file.read()
        print(nome)
        file.close()
        run(nome)  # Passo come parametro il nome del paziente
    except IOError:
        print("File not accessible")

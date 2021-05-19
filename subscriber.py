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


def sendResponse(message):
    # Elaboro la risposta e la invio al database
    splitted_message = message.split(SEPARATOR)

    for case in switch(splitted_message):
        if case('misura'):
            to_send = "Devi misurare " + splitted_message[1]
            print(to_send)
            break
        if case('medicina'):
            to_send = "Devi prendere la medicina " + splitted_message[1] + " quantità " + splitted_message[2]
            print(to_send)
        else:
            print('Risposta non valida')

    url = "http://www.lorenzodelauretis.it/tesi/index.php?message="+to_send
    req.get(url)
    
    return


#def runSubscriber():
R = redis.Redis()
clearList(R, CH_IN)

while True:
    response = R.lpop(CH_IN)
    if response:
        # Ho ricevuto un messaggio
        sendResponse(response.decode('utf-8'))
        print(response.decode('utf-8'))


# if __name__ == '__main__':
#     runSubscriber()
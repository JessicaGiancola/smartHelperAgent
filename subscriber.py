import redis
import requests as req

CH_IN = 'RESPONSE'


# Svuota la lista dei messaggi inviati dal MAS
def clearList(redisInstance, channel):
    for i in range(0, redisInstance.llen(channel)):
        redisInstance.lpop(channel)
    return


def sendResponse(message):
    # Elaboro la risposta e la invio al database

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
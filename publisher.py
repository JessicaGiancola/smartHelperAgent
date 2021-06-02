#!/usr/bin/env python3
import requests as req
import redis
import time
import json

# Nome del canale su cui invio i parametri (deve corrispondere al canale su cui Lindaproxy ascolta)
CH_OUT = 'TO_AGENT'


def getParameters(parameters, redisInstance, name):
    for parameter in parameters:
        request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name + "&" + parameter[1] + "=1"
        # request_url = "http://localhost/prova.php?nome=" + name + "&" + parameter[1] + "=1"
        response = req.get (request_url)
        prologParam = parameter[0] + "(" + response.text + ")"
        redisInstance.publish (CH_OUT, prologParam)  # Pubblico sul canale il parametro raccolto
        print (prologParam)


def run(patientName):
    R = redis.Redis()  # Istanza 1 di Redis
    # patientName = "Lorenzo De Lauretis"
    name_url = patientName.replace(" ", "%20")

    parameters = [["saturazione", "get_saturazione"], ["battito", "get_battito"], ["presminima", "get_presminima"], ["presmassima", "get_presmassima"], ["temperatura", "get_temperatura"], ["peso", "get_peso"], ["altezza", "get_altezza"], ["stato", "get_stato"]]

    # # Inserisco le malattie pregresse
    #
    # request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name_url + "&get_patologia=1"
    # patologies = req.get(request_url)
    # patologiesList = patologies.text.split(";")
    #
    # for patology in patologiesList:
    #     if patology != '':
    #         prolog = "patologia(" + patology + ")"
    #         R.publish(CH_OUT, prolog)
    #
    # # Inserisco la terapia
    #
    # request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name_url + "&get_terapia=1"
    # therapies = req.get(request_url)
    # therapiesList = json.loads(therapies)
    #
    # for therapy in therapiesList['terapia']:
    #     ora = therapy['orario'][0:2]
    #     minuti = therapy['orario'][-2:]
    #     if therapy != '':
    #         prolog = "terapia(medicine(" + therapy['medicina'] + "," + therapy['quantita'] + "),'" + ora + "','" + minuti + "')"
    #         print("stringa prolog " + prolog)
    #         R.publish(CH_OUT, prolog)

    for i in range(0, 10):
        getParameters(parameters, R, name_url)
        time.sleep(10)


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        nome = file.read()
        print(nome)
        file.close()
        run(nome)  # Passo come parametro il nome del paziente
    except IOError:
        print("File not accessible")

import requests as req
import redis
import time
import json

# Nome del canale su cui invio i parametri (deve corrispondere al canale su cui Lindaproxy ascolta)
CH_OUT = 'TO_AGENT'


def makeAtomic(s, therapy=False):
    out = s.replace("'", 'I')
    out = out.replace(' ', '_')
    if therapy:
        out = out.replace('(', 'A')
        out = out.replace(')', 'B')
        out = out.replace(',', 'F')
    return out


def getParameters(parameters, redisInstance, url_base):
    for parameter in parameters:
        request_url = url_base + "&" + parameter[1] + "=1"
        response = req.get(request_url).text
        if parameter[0] == 'stato' or parameter[0] == 'sensazione':
            array = response.lower().split(";")
            for feel in array:
                if feel:
                    prologParam = parameter[0] + "(" + feel + ")"
                    prolog = makeAtomic(prologParam)
                    redisInstance.publish(CH_OUT, prolog)  # Pubblico sul canale il parametro raccolto

        else:
            prologParam = parameter[0] + "(" + response + ")"
            prolog = makeAtomic(prologParam)
            redisInstance.publish(CH_OUT, prolog)  # Pubblico sul canale il parametro raccolto

        print(prologParam)


def run(patientName):
    R = redis.Redis()  # Istanza 1 di Redis
    name_url = patientName.replace(" ", "%20")
    #url_base = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name_url
    url_base = "http://localhost/prova.php?"

    parameters = [["anni", "get_eta"], ["altezza", "get_altezza"], ["peso", "get_peso"], ["temperatura", "get_temperatura"], ["saturazione", "get_saturazione"], ["battito", "get_battito"], ["presminima", "get_presminima"], ["presmassima", "get_presmassima"], ["stato", "get_stato"], ["sensazione", "get_sensazione"]]
    #parameters = [["sensazione", "get_sensazione"]]
    # # Inserisco le malattie pregresse
    #
    # request_url = url_base + "&get_patologia=1"
    # patologies = req.get(request_url)
    # patologiesList = patologies.text.split(";")
    #
    #
    # for patology in patologiesList:
    #     if patology != '':
    #         prolog = "patologia('" + patology.lower() + "')"
    #         prologAtomic = makeAtomic(prolog)
    #         R.publish(CH_OUT, prologAtomic)
    # print('inserite patologie')
    #
    # time.sleep(5)
    #
    # # Inserisco la terapia
    #
    # request_url = url_base + "&get_terapia=1"
    # therapies = req.get(request_url).text
    # print(therapies)
    # therapiesList = json.loads(therapies)
    #
    # for therapy in therapiesList:
    #     orario = therapy['orario'].split(":")
    #
    #     if therapy != '':
    #         prolog = "'" + therapy['medicina'].lower() + "','" + therapy['quantita'].lower() + "'," + orario[0] + "," + orario[1]
    #         prologAtomic = makeAtomic(prolog, True)
    #         prologAtomic = "terapia(" + prologAtomic + ")"
    #         print("stringa prolog " + prolog + " e " + prologAtomic)
    #         R.publish(CH_OUT, prologAtomic)
    # print('inserita terapia')
    #
    # time.sleep(5)

    for i in range(0, 10):
        getParameters(parameters, R, url_base)
        print(' inviati parametri n ' + str(i))
        time.sleep(10)


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        nome = file.read()  # leggo il nome del paziente dal file
        file.close()
        run(nome)  # Passo come parametro il nome del paziente

    except IOError:
        print("File not accessible")

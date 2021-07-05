import requests as req
import redis
import time
import json

CH_OUT = 'TO_AGENT'  # Nome del canale su cui invio i parametri (deve corrispondere al canale su cui Lindaproxy ascolta)
LIST_SEPARATOR = ';'


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
        if response:
            if parameter[0] == 'stato' or parameter[0] == 'sensazione':
                array = response.lower().split(LIST_SEPARATOR)
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
    url_base = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + patientName
    #url_base = "http://localhost/prova.php?"

    parameters = [["anni", "get_eta"], ["altezza", "get_altezza"], ["peso", "get_peso"], ["temperatura", "get_temperatura"], ["saturazione", "get_saturazione"], ["battito", "get_battito"], ["presminima", "get_presminima"], ["presmassima", "get_presmassima"], ["stato", "get_stato"], ["sensazione", "get_sensazione"]]

    # Inserisco le malattie pregresse

    request_url = url_base + "&get_patologia=1"
    patologies = req.get(request_url)
    if patologies:
        patologiesList = patologies.text.split(LIST_SEPARATOR)
        for patology in patologiesList:
            if patology:
                prolog = "patologia('" + patology.lower() + "')"
                prologAtomic = makeAtomic(prolog)
                R.publish(CH_OUT, prologAtomic)

    print('Inviate patologie pregresse')

    time.sleep(5)

    # Inserisco la terapia

    request_url = url_base + "&get_terapia=1"
    therapies = req.get(request_url).text
    if therapies:
        therapiesList = json.loads(therapies)
        for therapy in therapiesList:
            orario = therapy['orario'].split(":")
            if therapy:
                prolog = "'" + therapy['medicina'].lower() + "','" + therapy['quantita'].lower() + "'," + orario[0] + "," + orario[1]
                prologAtomic = makeAtomic(prolog, True)
                prologAtomic = "terapia(" + prologAtomic + ")"
                R.publish(CH_OUT, prologAtomic)

    print('Inviata terapia')

    time.sleep(5)

    for i in range(0, 10):
        getParameters(parameters, R, url_base)
        print('Inviati parametri n ' + str(i))
        time.sleep(10)


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        patientName = file.read()  # Leggo il nome del paziente dal file
        file.close()
        if patientName:
            name = ' '.join(patientName.split())  # Elimina eventuali spazi in eccesso
            run(name)  # Passo come parametro il nome del paziente
        else:
            print("Nome del paziente non presente")

    except IOError:
        print("File not accessible")

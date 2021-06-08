import requests as req
import redis
import time
import json

# Nome del canale su cui invio i parametri (deve corrispondere al canale su cui Lindaproxy ascolta)
CH_OUT = 'TO_AGENT'

def makeAtomic(s, therapy=False):
    out = s.replace("'", 'I')
    out = out.replace(' ', '-')
    if therapy:
        out = out.replace('(', 'A')
        out = out.replace(')', 'B')
        out = out.replace(',', 'F')
    # out = out.replace('[', 'C')
    # out = out.replace(']', 'D')
    # out = out.replace('.', 'E')
    # out = out.replace('/', 'G')
    # out = out.replace('\\', 'H')
    return out


def getParameters(parameters, redisInstance, name):
    for parameter in parameters:
        #request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name + "&" + parameter[1] + "=1"
        request_url = "http://localhost/prova.php?nome=" + name + "&" + parameter[1] + "=1"
        response = req.get(request_url).text
        if parameter[0] == 'stato':
            prologParam = parameter[0] + "('" + response.replace(";","").lower() + "')"
        else:
            prologParam = parameter[0] + "(" + response + ")"
        prolog = makeAtomic(prologParam)
        redisInstance.publish(CH_OUT, prolog)  # Pubblico sul canale il parametro raccolto
        print(prologParam)


def run(patientName):
    R = redis.Redis()  # Istanza 1 di Redis
    name_url = patientName.replace(" ", "%20")

    parameters = [["saturazione", "get_saturazione"], ["battito", "get_battito"], ["presminima", "get_presminima"], ["presmassima", "get_presmassima"], ["temperatura", "get_temperatura"], ["peso", "get_peso"], ["altezza", "get_altezza"], ["stato", "get_stato"]]
    #parameters = [["presminima", "get_presminima"], ["presmassima", "get_presmassima"]]

    # Inserisco le malattie pregresse

    request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name_url + "&get_patologia=1"
    patologies = req.get(request_url)
    patologiesList = patologies.text.split(";")


    for patology in patologiesList:
        if patology != '':
            prolog = "patologia('" + patology.lower() + "')"
            prologAtomic = makeAtomic(prolog)
            R.publish(CH_OUT, prologAtomic)
    print('inserite patologie')

    # Inserisco la terapia

    request_url = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + name_url + "&get_terapia=1"
    therapies = req.get(request_url).text
    print(therapies)
    therapiesList = json.loads(therapies)

    for therapy in therapiesList:
        orario = therapy['orario'].split(":")

        if therapy != '':
            prolog = "'" + therapy['medicina'].lower() + "','" + therapy['quantita'].lower() + "'," + orario[0] + "," + orario[1]
            prologAtomic = makeAtomic(prolog, True)
            prologAtomic = "terapia(" + prologAtomic + ")"
            print("stringa prolog " + prolog + " e " + prologAtomic)
            R.publish(CH_OUT, prologAtomic)
    print('inserita terapia')

    for i in range(0, 10):
        getParameters(parameters, R, name_url)
        print(' inviati parametri n ' + str(i))
        time.sleep(5)


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        nome = file.read()  # leggo il nome del paziente dal file
        print(nome)
        file.close()
        run(nome)  # Passo come parametro il nome del paziente
    except IOError:
        print("File not accessible")

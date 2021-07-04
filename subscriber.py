import redis
import requests as req
from switchcase import switch
import time

# Canale su cui il MAS invia i messaggi
CH_IN = 'RESPONSE'
SEPARATOR = '+'


# Svuota la lista dei messaggi inviati dal MAS
def clearList(redisInstance, channel):
    for i in range(0, redisInstance.llen(channel)):
        redisInstance.lpop(channel)
    return


# Elaboro la risposta e la invio al database
def sendResponse(message, url_base):
    splitted_message = message.split(SEPARATOR)
    to_send = ""
    mes = ""
    for case in switch(splitted_message[0]):
        if case('misura'):
            to_send = "&remindermisura=" + splitted_message[1] + "&message=Devi misurare " + splitted_message[1]
            break

        if case('medicina'):
            to_send = "&remindermedicina=1&nomemedicina=" + splitted_message[1].replace("-", " ") + "&quantita=" \
                      + splitted_message[2].replace("-", " ") + "&message=Devi prendere la medicina " \
                      + splitted_message[1] + " quantita " + splitted_message[2]
            break

        if case('sei'):
            chili = abs(round(float(splitted_message[2]), 2))
            kg = "chilo" if chili == 1 else "chili"

            if splitted_message[1] == 'invariato':
                mes = "Il tuo peso non ha subito variazioni"
            else:
                mes = "Sei " + splitted_message[1] + " di " + str(chili) + " " + kg

            to_send = "&feed=peso&message=" + mes
            break

        if case('saturazione'):
            for feed in switch(splitted_message[1]):
                if feed('high'):
                    mes = "Hai problemi di ossigenazione"
                    break
                if feed('normal'):
                    mes = "Non hai problemi di ossigenazione"
                    break
                if feed('low'):
                    mes = "Hai un leggero problema di ossigenazione"
                    break
            to_send = "&feed=" + splitted_message[0] + "&message=" + mes
            break

        if case('battito'):
            for feed in switch(splitted_message[1]):
                if feed('low'):
                    mes = "La tua frequenza cardiaca presenta una leggera bradicardia"
                    break
                if feed('normal'):
                    mes = "La tua frequenza cardiaca non presenta problemi"
                    break
                if feed('high'):
                    mes = "La tua frequenza cardiaca presenta una leggera tachicardia"
                    break
            to_send = "&feed=" + splitted_message[0] + "&message=" + mes
            break

        if case('presminima'):
            for feed in switch(splitted_message[1]):
                if feed('low'):
                    mes = "La tua pressione minima presenta una ipotensione"
                    break
                if feed('normal'):
                    mes = "La tua pressione minima non presenta problemi"
                    break
                if feed('high'):
                    mes = "La tua pressione minima presenta una ipertensione"
                    break
            to_send = "&feed=" + splitted_message[0] + "&message=" + mes
            break

        if case('presmassima'):
            for feed in switch(splitted_message[1]):
                if feed('low'):
                    mes = "La tua pressione massima presenta una ipotensione"
                    break
                if feed('normal'):
                    mes = "La tua pressione massima non presenta problemi"
                    break
                if feed('high'):
                    mes = "La tua pressione massima presenta una ipertensione"
                    break
            to_send = "&feed=" + splitted_message[0] + "&message=" + mes
            break

        if case('temperatura'):
            for feed in switch(splitted_message[1]):
                if feed('low'):
                    mes = "Hai qualche linea di febbre, ti consiglio di riposare"
                    break
                if feed('ok'):
                    mes = "Non hai febbre"
                    break
                else:
                    break
            to_send = "&feed=" + splitted_message[0] + "&message=" + mes
            break

        if case('doctor'):
            for feed in switch(splitted_message[1]):
                if feed('prontosoccorso'):
                    mes = "Devi correre al pronto soccorso"
                    break
                if feed('bevi'):
                    mes = "Il dottore suggerisce di ridurre il consumo di acqua"
                    break
                else:
                    mes = "Il dottore suggerisce di prendere " + splitted_message[1].replace("_", " ")

            to_send = "&feed=medico&message=" + mes
            break

        if case('how'):
            to_send = "&message=Come ti senti?"
            break

        else:
            to_send = ''
            print('Risposta non valida: ' + message)

    to_send_url = url_base + to_send
    url = to_send_url.replace(" ", "%20")
    print(url)
    req.get(url)
    return


def run(patientName):
    R = redis.Redis()
    clearList(R, CH_IN)
    #url_base = "http://www.lorenzodelauretis.it/tesi/index.php?nome=" + patientName
    url_base = "http://localhost/prova.php?"
    while True:
        response = R.lpop(CH_IN)
        if response:
            # Ho ricevuto un messaggio
            sendResponse(response.decode('utf-8'), url_base)
            print(response.decode('utf-8'))


if __name__ == '__main__':

    try:
        file = open('nome_paziente.txt', 'r')
        patientName = file.read()  # leggo il nome del paziente dal file
        file.close()
        run(patientName)  # Passo come parametro il nome del paziente

    except IOError:
        print("File not accessible")

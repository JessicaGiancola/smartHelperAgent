
'''
Copyright 2016-2018 Agnese Salutari.
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on 
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and limitations under the License
'''

__author__ = 'Agnese'

import re
import json
import os
import time
import sys

class ServerPyProlog:

    def __init__(self):
        self.result = "" #risultato, stato attuale della conversione
        path = sys.path[0]
        self.root = path[:path.rfind('DALI')]
        #print(path)
        #print (self.root)

    def findRoot(self):
        #restituisce il path di root
        return self.root

    def addToResult(self,string): 
        #aggiunge una stringa al risultato
        string = string + os.linesep
        self.result = self.result + string

    def getResult(self): 
        #restituisce la stringa risultato
        return self.result

    def delResult(self): 
        #cancella la stringa contenuta in result
        self.result = ""

    def notificationTXT(txtName,path): 
        #crea un file testuale vuoto di notifica
        path = path + os.sep + txtName + ".txt"
        handle = False
        while handle is False:
            file = open(path, "w")
        file.close()

    def RESULTtoPL(self, fileName, path, replace):
        # Scrive il risultato su un file Prolog.
        # Se replace è true, cancella un eventuale file precedente con lo stesso nome nel path dato,
        # altrimenti aggiunge result a questo file.
        if path is '':
            destinazione = fileName+'.pl'
        else:
            destinazione = path+os.sep+fileName+".pl"
        handle = False
        if replace is False:
            while (handle is False):
                handle = open(destinazione, 'a')
                time.sleep(0.1)
        else:
            while handle is False:
                handle = open(destinazione, 'w')
                time.sleep(0.1)
        handle.write(os.linesep+self.getResult())
        handle.close()

    def RESULTtoTXT(self, fileName, path, replace):
        # Scrive il risultato su un file Prolog.
        # Se replace è true, cancella un eventuale file precedente con lo stesso nome nel path dato,
        # altrimenti aggiunge result a questo file.
        if path is '':
            destinazione = fileName+'.txt'
        else:
            destinazione = path+os.sep+fileName+".txt"
        handle = False
        if replace is False:
            while (handle is False):
                handle = open(destinazione, 'a')
                time.sleep(0.1)
        else:
            while handle is False:
                handle = open(destinazione, 'w')
                time.sleep(0.1)
        handle.write(os.linesep+self.getResult())
        handle.close()

    def cleanName(self,string): 
        # "pulisce" una stringa da trasformare in nome Prolog da caratteri non contemplati 
        string = string.replace(' ', '_')
        string = string.replace('.', '')
        string = string.replace(',', '')
        string = string.replace('=', '')
        string = re.sub("/[^a-zA-Z0-9_-]/", "", string)
        string = string.lower()
        if re.findall('/^[a-z]+$/i', string[0]) is False:
            string = string[1:]
        return string

    def cleanJson(self,string): 
        #"pulisce" il Json da caratteri non contemplati da Prolog
        string = string.replace("{", "")
        string = string.replace("}", "")
        string = string.replace('"', "")
        string = string.replace(' ', "")
        string = string.lower()
        return string

    def idConverter(self,numericId): 
        # converte i numeri degli id numerici in lettere (il Prolog non gestisce gli id numerici)
        string = str(numericId)
        string = string.replace('0', 'a')
        string = string.replace('1', 'b')
        string = string.replace('2', 'c')
        string = string.replace('3', 'd')
        string = string.replace('4', 'e')
        string = string.replace('5', 'f')
        string = string.replace('6', 'g')
        string = string.replace('7', 'h')
        string = string.replace('8', 'i')
        string = string.replace('9', 'l')
        return string

    def JSONtoPmap(self,json,mapName): 
        # Converte una stringa Json in una stringa lista Prolog
        json = str(json)
        list = self.cleanJson(json)
        mapName = self.cleanName(mapName)
        risultato = ""
        array = list.strip().split(',') #strip() rimuove gli spazi; split() splitta la stringa in un array
        l = len(array)
        for i in range(0,l):
            map = array[i].split(':')
            r = mapName+"("+map[0].lower()+","+map[1]+")." + os.linesep
            risultato = risultato + r
        return risultato

    def cleanDictionary(self,dict): 
        # "pulisce" i dictionary per elaborarli in Prolog
        dict = json.dumps(dict)
        return dict

    def DICTIONARYtoPmap(self,dict,mapName): 
        # trasforma un dictionary in una mappa Prolog
        mapName = self.cleanName(mapName)
        dict = self.cleanDictionary(dict)
        dict = self.cleanJson(dict)
        risultato = self.JSONtoPmap(dict,mapName)
        return risultato

    def DICTIONARYtoPpredicate(self,dict,predicateName): 
        #trasforma un dictionary in un insieme di predicati Prolog
        predicateName = self.cleanName(predicateName)
        dict = str(dict)
        dict = self.cleanJson(dict)
        array = dict.split(',')
        a = ""
        risultato = ""
        l = len(array)
        for i in range(0,l):
            subarray = str(array[i]).split(':')
            pred = predicateName+"("+subarray[0]+","+subarray[1]+").\r\n"
            risultato = risultato+pred
        return risultato

    def VALUEStoPlist(self,valuesArray,listName): 
        # trasforma un'array di valori in una lista Prolog
        v = str(valuesArray[0])
        l = len(valuesArray)
        for i in range(1,l-1):
            v = v+","+str(valuesArray[i])
        name = self.cleanName(listName)
        risultato = name + "=["+v+"]." + os.linesep
        return risultato

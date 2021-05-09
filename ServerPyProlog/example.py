
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

#YOU CAN USE THIS FILE TO TEST "serverPyProlog" LIBRARY WORK.

import ServerPyProlog as SPP

translator=SPP.ServerPyProlog()     #Creation of a ServerPyProlog object

json = '{"nome  ":"felix","cognome":"domesticus"}' #A JSON string (it could be a normal JSON too)
print("Json:")
print(json)
t=translator.JSONtoPmap(json,"gatto")
print("mio "+ t)
translator.addToResult(t)
print("Result:")
print(translator.getResult())


id=translator.idConverter(1231)
print("Id:")
print(id)

translator.delResult()

persona={            #A dictionary
    "nome":"agnese",
    "cognome":"salutari"
}
print("Persona:")
print(persona)
t=translator.DICTIONARYtoPmap(persona,id)
translator.addToResult(t)
print("Result:")
print(translator.getResult())

translator.delResult()    #Delete old results collected by serverPyProlog in self.result. Use ADDtoResult(string)
                       #to add a Prolog string to add to result.
print("Result cancellato:")
print("Result="+translator.getResult())


values=["0",2,3]
print("Array of values:")
print(values)
t=translator.VALUEStoPlist(values, "numbers")
translator.addToResult(t) #Convert an array to a Prolog list (in this case, the list is called numbers)
print("Result:")
print(translator.getResult())

translator.RESULTtoPL('prova', '', False)

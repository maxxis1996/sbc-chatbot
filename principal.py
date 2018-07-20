from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram
import telebot
import snips_nlu
from snips_nlu import SnipsNLUEngine
from SPARQLWrapper import SPARQLWrapper, JSON
import es_core_news_md
import  textacy.datasets as ds
import textacy
import io
import json


#bot = telegram.Bot(token='553612224:AAGCsUpMJ0BJS-IAagAkia06gD3hmr4X87c')
#print(bot.get_me())
snips_nlu.load_resources("es")
nlp = es_core_news_md.load()
bot=telebot.TeleBot("605016230:AAEPuIIJGVVoeHaGbP6iroaYdi3uhkvJXrQ")

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    #print(message)
    chatid=message.chat.id
    nombreUsuario=message.chat.first_name+""+message.chat.last_name
    saludo="hola {nombre}, Bienvenido a nuestro Bot"
    bot.send_message(chatid, saludo.format(nombre=nombreUsuario))
   # bot.send_message(message,"Hola Mundo")

@bot.message_handler(commands=["hola"])
def enviarSaludo(message):
    chatid=message.chat.id
    saludo="Este comando respondera cuando ingreses el comando  /hola"
    bot.send_message(chatid, saludo)

@bot.message_handler(func=lambda m: True)
def imprimirmensaje(message):
    campo=""
    predicado=""
    lista=[]
    chatid=message.chat.id
    with io.open('dataset.json') as file:
        dataset = json.load(file)
    engine = SnipsNLUEngine()
    engine.fit(dataset)
    parsing = engine.parse(unicode(message.text))
    temp=json.dumps(parsing, indent=2)
    #   try: 
        
    intentName=parsing["intent"]["intentName"]
    entidad=""
    try :
        enti=parsing["slots"][0]
        entidad=enti["rawValue"]
    except:
        pass
    if len(intentName)>0 and len(entidad)>0:
        print ("good")
        
        if intentName=="descripcion":
            print ("si entraaaaaaaaaaaaaaaaaaa")
            predicado="http://usefulinc.com/ns/doap#description"
            campo=consultaSparql1(entidad,predicado)
        elif intentName=="imagen":
            predicado="http://schema.org/image"
            campo=consultaSparql1(entidad,predicado)
        elif intentName=="igualEn":
            predicado="http://www.w3.org/2002/07/owl#sameAs"
            campo=consultaSparql1(entidad,predicado)
        elif intentName=="igualKi":
            predicado="http://www.w3.org/2002/07/owl#sameAs"
            campo=consultaSparql1(entidad,predicado)
        elif intentName=="nombreCientifico":
            predicado="http://lod.taxonconcept.org/ontology/txn.owl#scientificName"
            campo=consultaSparql1(entidad,predicado)   
        bot.send_message(chatid,campo)
    else:
        print ("bad")
        lista=consultaSparql()
        bot.send_message(message,"perro")
    #except:
        #campo="No entiendo tu pregunta, puedes preguntarme de nuevo"
        #bot.send_message(message,campo)
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    chatid=message.chat.id
    bot.send_message(chatid ,"No existe este comando de bot solo acepta comandos de /start y /help")

def consultaSparql1(entidad, predicado):    
    resultados = []
    sparql = SPARQLWrapper("http://localhost:8890/sparql/Animales")    
    entidad = entidad.capitalize()
    print entidad
    print predicado
    print("""
                        select distinct ?o
                        where {
                            <Animales:"""+entidad+"""> <"""+predicado+"""> ?o
                        }
                                   
                                """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        resultados.append((result["o"]["value"]))
    for resu in resultados:
        print (resu)
    return resultados


def consultaSparql():
    resultados = []

    sparql = SPARQLWrapper("http://localhost:8890/sparql/Animales")        
    sparql.setQuery("""
                        select distinct ?a
                        where {
                            ?a ?p ?o
                        }
                        LIMIT 2
                                   
                                """)  # the previous query as a literal string
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print((result["a"]["value"]))
        resultados.append((result["a"]["value"]))
    return resultados
bot.polling ()
"""
snips-nlu generate-dataset en intent_descripcion.txt intent_allAnimal.txt entity_animals.txt > dataset.json
"""
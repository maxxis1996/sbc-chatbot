# coding=utf-8
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


snips_nlu.load_resources("es")
nlp = es_core_news_md.load()
mi_bot=telebot.TeleBot("605016230:AAEPuIIJGVVoeHaGbP6iroaYdi3uhkvJXrQ")

@mi_bot.message_handler(commands=['start','help'])
def send_welcome(message):
    mi_bot.reply_to(message, "Howdy, how are you doing?")

@mi_bot.message_handler(func=lambda m: True)
def imprimirmensaje(message):
    campo=""
    predicado=""
    bandera1=False
    chatid=message.chat.id
    with io.open('dataset.json') as file:
        dataset = json.load(file)
    engine = SnipsNLUEngine()
    engine.fit(dataset)
    parsing = engine.parse(unicode(message.text))
    entidad=""
    intentName=""
    try:     
        intentName=parsing["intent"]["intentName"]
        try :
            enti=parsing["slots"][0]
            entidad=enti["rawValue"]
        except:
            bandera1=True
        if len(intentName)>0 and len(entidad)>0:
            print ("good")
            
            if intentName=="descripcion":
                print ("si entraaaaaaaaaaaaaaaaaaa")
                predicado="http://usefulinc.com/ns/doap#description"
                campo=consultaSparql1(entidad,predicado)
                
            elif intentName=="imagen":
                predicado="http://schema.org/image"
                campo=consultaSparql1(entidad,predicado)
                campo=("La imagen de "+entidad+" es: "+campo[0])
            elif intentName=="igualEn":
                predicado="http://www.w3.org/2002/07/owl#sameAs"
                campo=consultaSparql2(entidad,predicado,"en")
                campo=("La traduccion de "+entidad+" en ingles es: "+campo[0])
            elif intentName=="igualKi":
                predicado="http://www.w3.org/2002/07/owl#sameAs"
                campo=consultaSparql2(entidad,predicado,"ki")
                campo=("La traduccion de "+entidad+" en kitchwa es: "+campo[0])
            elif intentName=="nombreCientifico":
                predicado="http://lod.taxonconcept.org/ontology/txn.owl#scientificName"
                campo=consultaSparql1(entidad,predicado)   
                campo=("El nombre cientifico de "+entidad+" es: "+campo[0])                
            mi_bot.reply_to(message,campo)
        elif intentName=="allAnimal":            
            cam=consultaSparql()
            campo=""
            for ca in cam:
                campo+=ca+", "
            mi_bot.reply_to(message,campo)
        else:
            print (entidad)
            print (intentName)
            print ("bad")

        if bandera1:
            print("¿Dime de animal deseas saber la descripción?")

        
    #except Exception,e: print str(e) 
    except:
        campo="No entiendo tu pregunta, puedes preguntarme de nuevo"
        mi_bot.reply_to(message,campo)

def consultaSparql1(entidad, predicado):    
    resultados = []
    sparql = SPARQLWrapper("http://localhost:8890/sparql/Animales")    
    entidad = entidad.capitalize()
    print entidad
    print predicado
    sparql.setQuery("""
                        select distinct ?o
                        where {
                            <Animales:"""+entidad+"""> <"""+predicado+"""> ?o
                        }
                                   
                                """)  # the previous query as a literal string
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        #print((result["a"]["value"]))
        resultados.append((result["o"]["value"]))
    for resu in resultados:
        print (resu)
    return resultados

def consultaSparql2(entidad, predicado,idioma):    
    resultados = []
    sparql = SPARQLWrapper("http://localhost:8890/sparql/Animales")    
    entidad = entidad.capitalize()
    print entidad
    print predicado
    sparql.setQuery("""
                        select ?o
                        where {
                            <Animales:"""+entidad+"""> <"""+predicado+"""> ?o .
                            FILTER (lang(?o)='"""+idioma+"""')
                        }
                                   
                                """)  # the previous query as a literal string
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        #print((result["a"]["value"]))
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
                            ?a <http://usefulinc.com/ns/doap#description> ?o
                        }
                                   
                                """)  # the previous query as a literal string
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print((result["a"]["value"]).replace('Animales:', ''))
        resultados.append((result["a"]["value"]).replace('Animales:', ''))
    return resultados

mi_bot.polling ()
"""
snips-nlu generate-dataset en intent_descripcion.txt intent_nombreCientifico.txt intent_imagen.txt intent_igualEn.txt intent_igualKi.txt intent_allAnimal.txt entity_animals.txt > dataset.json
"""
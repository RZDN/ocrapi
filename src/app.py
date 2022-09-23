from distutils.log import debug
from json import dumps
import json
from logging.config import dictConfig
import re
from sched import scheduler
import flask
from flask import request, Response
from bson import json_util
import pymongo
from flask_cors import CORS
from flask_apscheduler import APScheduler
import datetime
from bson.objectid import ObjectId
import os
from paddleocr import PaddleOCR, draw_ocr
from controllers.user_controller import USERS
from controllers.consultation_controller import CONSULTATIOS
from controllers.history_controller import STORIES
from PIL import Image, ImageOps

app = flask.Flask(__name__)
# app.config['MONGO_URI'] = "mongodb://localhost/ocrapp"
myclient = pymongo.MongoClient("mongodb://3ce4e613-0ee0-4-231-b9ee:qfDSkSADTncQVX9L0T4910t4uhxe7QJpPaJCcWcNr5SYqB1EzXOZDPQz34bTXNCrdVcZ1X9ga6M4tRyepsRP7g==@3ce4e613-0ee0-4-231-b9ee.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@3ce4e613-0ee0-4-231-b9ee@")

#cors = CORS(app)

endpoint = "https://ocr-app-ocr-app.cognitiveservices.azure.com/"
key = "c33dd42ea5a84541b2d1ff04bd82c314"
valor = '/image.jpeg'
path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
pathfinal = path + valor
filepath = 'E:/dev/python/OCRAPI/src/image.jpeg'
picture = Image.open(pathfinal)
picture = ImageOps.exif_transpose(picture)
picture.save('image.jpeg', 'JPEG', optimize=True, quality=50)


@app.route("/consulta")
def pruebas():

    # -------------------------------

    ultima_cadena = ""
    cadena_vacía = ""
    diccionario = {}
    diccionario["Fec_Atencion"] = ""
    diccionario["Hora"] = ""
    diccionario["Edad"] = ""
    diccionario["Motivo"] = ""
    diccionario["Tipo_Enf"] = ""
    diccionario["Signos_Sintomas"] = ""
    diccionario["Apetito"] = ""
    diccionario["Sed"] = ""
    diccionario["Suenio"] = ""
    diccionario["Estado_Animo"] = ""
    diccionario["Orina"] = ""
    diccionario["Deposiciones"] = ""
    diccionario["Ex_Fisico"] = ""
    diccionario["Temperatura"] = ""
    diccionario["Pa"] = ""
    diccionario["Fc"] = ""
    diccionario["Fr"] = ""
    diccionario["Peso"] = ""
    diccionario["Talla"] = ""
    diccionario["Imc"] = ""
    diccionario["Diagnostico"] = ""
    diccionario["Tratamiento"] = ""
    diccionario["Examenes_Auxiliares"] = ""
    diccionario["Referencia"] = ""
    diccionario["Proxima_Cita"] = ""
    diccionario["Atendido_Por"] = ""
    diccionario["Observaciones"] = ""

    with open("C:/Users/Sebastian/APP_OCR_APP/imageprueba.png", "rb") as fd:
        invoice = fd.read()
        # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key))
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", invoice)
        result = poller.result()
        for kv_pair in result.key_value_pairs:
            if kv_pair.key.content == "FECHA:":
                diccionario["Fec_Atencion"] = kv_pair.value.content
            if kv_pair.key.content == "HORA:":
                diccionario["Hora"] = kv_pair.value.content
            if kv_pair.key.content == "EDAD:":
                diccionario["Edad"] = kv_pair.value.content
            if kv_pair.key.content == "Motivo de consulta:":
                diccionario["Motivo"] = kv_pair.value.content
            if kv_pair.key.content == "Tiempo de enfermedad:":
                diccionario["Tipo_Enf"] = kv_pair.value.content
            if kv_pair.key.content == "Apetito:":
                diccionario["Apetito"] = kv_pair.value.content
            if kv_pair.key.content == "Sed:":
                diccionario["Sed"] = kv_pair.value.content
            if kv_pair.key.content == "Sue":
                diccionario["Suenio"] = kv_pair.value.content
            if kv_pair.key.content == "Orina:":
                diccionario["Orina"] = kv_pair.value.content
            if kv_pair.key.content == "Ex. Fisico:" or kv_pair.key.content.startswith("Ex"):
                diccionario["Ex_Fisico"] = kv_pair.value.content
            if kv_pair.key.content == "FC:":
                diccionario["Fc"] = kv_pair.value.content
            if kv_pair.key.content == "FR:":
                diccionario["Fr"] = kv_pair.value.content
            if kv_pair.key.content == "Peso:":
                diccionario["Peso"] = kv_pair.value.content
            if kv_pair.key.content == "Talla:":
                diccionario["Talla"] = kv_pair.value.content
            if kv_pair.key.content == "IMC:":
                diccionario["Imc"] = kv_pair.value.content
            if kv_pair.key.content == "Exámenes auxiliares:":
                diccionario["Examenes_Auxiliares"] = kv_pair.value.content
            # if kv_pair.key.content == "Referencia (lugar y motivo):" or kv_pair.key.content.startswith("Referen"):
            #        diccionario["Referencia"] = kv_pair.value.content
            if kv_pair.key.content == "Atendido por:" or kv_pair.key.content.startswith("Atendido"):
                diccionario["Atendido_Por"] = kv_pair.value.content
            if kv_pair.key.content == "Próxima cita:":
                diccionario["Proxima_Cita"] = kv_pair.value.content
            if kv_pair.key.content == "Estado de ánimo:":
                diccionario["Estado_Animo"] = kv_pair.value.content

        for style in result.styles:
            if style.is_handwritten:
                for span in style.spans:
                    cadena = result.content[span.offset:span.offset + span.length]

                    Estado = cadena.find("Estado")
                    Orina = cadena.find("Orina")
                    Temperatura = cadena.find("To:")
                    Presion = cadena.find("PA:")
                    Diagnostico = cadena.find("· ")
                    Tratamiento = cadena.find("· ") or cadena.find(".")
                    if Estado > -1:
                        if len(diccionario["Estado_Animo"]) == 0:
                            subcadena = cadena[Estado +
                                               17:span.offset + span.length]
                            diccionario["Estado_Animo"] = subcadena
                    if Orina > -1:
                        if len(diccionario["Orina"]) == 0:
                            subcadena = cadena[Orina +
                                               2:span.offset + span.length]
                            diccionario["Orina"] = subcadena
                    if Temperatura > -1:
                        Nuevo = len("To:")
                        if len(diccionario["Temperatura"]) == 0:
                            subcadena = cadena[Temperatura+Nuevo:4]
                            diccionario["Temperatura"] = subcadena
                    if Presion > -1:
                        Nuevo = len("PA:")
                        if len(diccionario["Pa"]) == 0:
                            subcadena = cadena[Presion+Nuevo:5]
                            diccionario["Pa"] = subcadena
                    if Diagnostico > -1:
                        Nuevo = len("· ")
                        if len(diccionario["Diagnostico"]) == 0:
                            subcadena = cadena[Diagnostico+Nuevo:]
                            diccionario["Diagnostico"] = subcadena
                    if Tratamiento > -1:
                        Nuevo = len("· ")
                        if len(diccionario["Tratamiento"]) == 0:
                            subcadena = cadena[Tratamiento:]
                            diccionario["Tratamiento"] = subcadena
                    # if x.startswith("2.-"):
                    #    Orina=x.find("Orina")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Orina+2:]
                    #    print(subcadena)
                    # if x.startswith("3.-"):
                    #    Temperatura=x.find("T")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Temperatura:]
                    #    print(subcadena)
                    # if x.startswith("4.-"):
                    #    Presion=x.find("P")
                    #    FC=x.find("FC")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Presion:FC-3]
                    #    print(subcadena)
                    # if x.startswith("5.-"):
                    #    Diagnostico=x.find(" ")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Diagnostico-1:]
                    #    print(subcadena)
                    # if x.startswith("6.-"):
                    #    Tratamiento=x.find(" ")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Tratamiento-1:]
                    #    print(subcadena)
                    # if x.startswith("7.-"):
                    # Presion=x.find("PA")
                    # FC=x.find("FC")
                    ##    cadena=result.content[span.offset:span.offset+ span.length]
                    ##    subcadena = cadena[Presion:FC]
                    # print(subcadena)
                    # if x.startswith("8.-"):
                    #    Atendido=x.find("Atendido")
                    #    cadena=result.content[span.offset:span.offset+ span.length]
                    #    subcadena = cadena[Atendido+10:]
                    #    print(subcadena)

                # if (kv_pair.key.content == "FECHA:"):
                #    ed = [kv_pair.value.content]
                #    # Dos opciones, El string viene con HORA O SIN HORA
                #    obj1_Fec_Atencion = ed[0]
                #    diccionario["Fec_Atencion"] = obj1_Fec_Atencion
                # else:
                #    cadena_fecha = [""]
                #    # Dos opciones, El string viene con HORA O SIN HORA
                #    obj1_Fec_Atencion = cadena_fecha[0]
                #    diccionario["Fec_Atencion"] = obj1_Fec_Atencion
    #ocr = PaddleOCR(use_angle_cls=True, lang='en')
    # Rutabase = 'C:/Users/Sebastian/APP_OCR_APP/image.jpeg'     #E:/escritorio/Taller-Spring1/APP_OCR_APP/apiocr/src/images/image.jpeg
    #img_path = os.path.abspath(Rutabase)
    #result = ocr.ocr(img_path, cls=True)

    # for res in result:
    #    print(res[1][0])
#
    #    if (res[1][0].upper().startswith("EX.")):
    #        ultima_cadena = res[1][0]
    #    if (res[1][0].upper().startswith("EXAMENES AUXILIARES")):
    #        ultima_cadena = res[1][0]
    #    if (res[1][0].upper().startswith("REFERENCIA")):
    #        ultima_cadena = res[1][0]
    #    if (res[1][0].upper().startswith("TRATAMIENTO")):
    #        ultima_cadena = res[1][0]
    #    if (res[1][0].upper().startswith("DIAGNOSTICO")):
    #        ultima_cadena = res[1][0]

    # Primero las validaciones sencillas (cuando empiezan con el nombre del objeto)

    # Esto valida en caso viene la fecha con hora

    # En caso la fecha viene sola
    # if (res[1][0].upper().startswith("HORA")):
    #    edit_string_hora = re.split(r'a| |H|O|R|A|:', res[1][0])
    #    obj1_Hora = edit_string_hora[0]
    #    diccionario["Hora"] = obj1_Hora
    # if (res[1][0].upper().startswith("APETITO")):
    #    string_apetito = res[1][0].split('.')
    #    edit_string_apetito = re.split(
    #        r'Apetito|Sed| |Estado|de|animo|Sueno|Suerio', ''.join(string_apetito))
    #    remove_apetito_list = [""]
    #    ed = [word for word in edit_string_apetito if word not in remove_apetito_list]
    #    for i, text_line in enumerate(ed):
    #        if (i == 0):
    #            obj1_Apetito = ed[0]
    #            diccionario["Apetito"] = obj1_Apetito
    #        if (i == 1):
    #            obj1_Sed = ed[1]
    #            diccionario["Sed"] = obj1_Sed
    #        if (i == 2):
    #            obj1_Suenio = ed[2]
    #            diccionario["Suenio"] = obj1_Suenio
    #        if (i == 3):
    #            obj1_Estado_Animo = ','.join(ed[3:])
    #            diccionario["Estado_Animo"] = obj1_Estado_Animo
    # if (res[1][0].upper().startswith("ORINA")):
    #    primer_corte = re.split(r'Deposiciones|Depos', res[1][0])
    #    edit_string_orina = re.split(r'Orina:|Orina| ', primer_corte[0])
    #    obj1_Orina = ''.join(edit_string_orina)
    #    diccionario["Orina"] = obj1_Orina
    # if (res[1][0].upper().startswith("DEPOSI")):
    #    edit_string_deposiciones = re.split(
    #        r'Deposiciones:|Deposiciones|Deposicione ', res[1][0])
    #    remove_deposiciones_list = [""]
    #    ed = [
    #        word for word in edit_string_deposiciones if word not in remove_deposiciones_list]
    #    obj1_Deposiciones = ' '.join(ed)
    #    diccionario["Deposiciones"] = obj1_Deposiciones
    # if (res[1][0].upper().startswith("T") and ultima_cadena.upper().startswith("EX.") and not (res[1][0].upper().startswith("EX."))):
    #    string_tem = res[1][0].split('.')
    #    edit_string_temp = re.split(
    #        r'T|Pa|PA| |FC|FR|Peso|Talla|IMC|:|alla', ''.join(string_tem))
    #    remove_temp_list = [""]
    #    ed = [word for word in edit_string_temp if word not in remove_temp_list]
    #    for i, text_line in enumerate(ed):
    #        if (i == 0):
    #            obj1_Temperatura = ed[0]
    #            diccionario["Temperatura"] = obj1_Temperatura
    #        if (i == 1):
    #            obj1_Pa = ed[1]
    #            diccionario["Pa"] = obj1_Pa
    #        if (i == 2):
    #            obj1_Fc = ed[2]
    #            diccionario["Fc"] = obj1_Fc
    #        if (i == 3):
    #            obj1_Fr = ed[3]
    #            diccionario["Fr"] = obj1_Fr
    #        if (i == 4):
    #            obj1_Peso = ed[4]
    #            diccionario["Peso"] = obj1_Peso
    #        if (i == 5):
    #            obj1_Talla = ed[5]
    #            diccionario["Talla"] = obj1_Talla
    #        if (i == 6):
    #            obj1_Imc = ed[6]
    #            diccionario["Imc"] = obj1_Imc
    # if (res[1][0].upper().startswith("PA") and ultima_cadena.upper().startswith("EX.") and not (res[1][0].upper().startswith("EX."))):
    #    edit_string_temp = re.split(
    #        r'T|Pa|PA| |FC|FR|Peso|Talla|IMC|:|alla', res[1][0])
    #    remove_temp_list = [""]
    #    ed = [word for word in edit_string_temp if word not in remove_temp_list]
    #    for i, text_line in enumerate(ed):
    #        if (i == 0):
    #            obj1_Pa = ed[0]
    #            diccionario["Pa"] = obj1_Pa
    #        if (i == 1):
    #            obj1_Fc = ed[1]
    #            diccionario["Fc"] = obj1_Fc
    #        if (i == 2):
    #            obj1_Fr = ed[2]
    #            diccionario["Fr"] = obj1_Fr
    #        if (i == 3):
    #            obj1_Peso = ed[3]
    #            diccionario["Peso"] = obj1_Peso
    #        if (i == 4):
    #            obj1_Talla = ed[4]
    #            diccionario["Talla"] = obj1_Talla
    #        if (i == 5):
    #            obj1_Imc = ed[5]
    #            diccionario["Imc"] = obj1_Imc
    # if (res[1][0].upper().startswith("PES") and ultima_cadena.upper().startswith("EX.") and not (res[1][0].upper().startswith("EX."))):
    #    print("1:", res[1][0])
    #    edit_string_temp = re.split(r'Peso|Talla|IMC|:|alla|MC', res[1][0])
    #    remove_temp_list = [""]
    #    print("2:", edit_string_temp)
    #    ed = [word for word in edit_string_temp if word not in remove_temp_list]
    #    print("3:", ed)
    #    for i, text_line in enumerate(ed):
    #        if (i == 0):
    #            obj1_Peso = ed[0]
    #            diccionario["Peso"] = obj1_Peso
    #        if (i == 1):
    #            obj1_Talla = ed[1]
    #            diccionario["Talla"] = obj1_Talla
    #        if (i == 2):
    #            obj1_Imc = ed[2]
    #            diccionario["Imc"] = obj1_Imc
    # Examenes auxiliares -> Si empieza en la misma linea o empieza abajo
    # if (ultima_cadena.upper().startswith("EXAMENES AUXILIARES") and not (res[1][0].upper().startswith("EXAMENES AUXILIARES"))):
    #    obj1_Examenes_Auxiliares += " " + res[1][0]
    #    diccionario["Examenes_Auxiliares"] = obj1_Examenes_Auxiliares

    # No me preguntes por que pero cuando lo retorno como un diccionario aunque en el postman aparentemente es lo mismo el front vuela asi que hago esta webada
    return {
        'Fec_Atencion': diccionario["Fec_Atencion"],
        'Hora': diccionario["Hora"],
        'Edad': diccionario["Edad"],
        'Motivo': diccionario["Motivo"],
        'Tipo_Enf': diccionario["Tipo_Enf"],
        'Signos_Sintomas': diccionario["Signos_Sintomas"],
        'Apetito': diccionario["Apetito"],
        'Sed': diccionario["Sed"],
        'Suenio': diccionario["Suenio"],
        'Estado_Animo': diccionario["Estado_Animo"],
        'Orina': diccionario["Orina"],
        'Deposiciones': diccionario["Deposiciones"],
        'Ex_Fisico': diccionario["Ex_Fisico"],
        'Temperatura': diccionario["Temperatura"],
        'Pa': diccionario["Pa"],
        'Fc': diccionario["Fc"],
        'Fr': diccionario["Fr"],
        'Peso': diccionario["Peso"],
        'Talla': diccionario["Talla"],
        'Imc': diccionario["Imc"],
        'Diagnostico': diccionario["Diagnostico"],
        'Tratamiento': diccionario["Tratamiento"],
        'Examenes_Auxiliares': diccionario["Examenes_Auxiliares"],
        'Referencia': diccionario["Referencia"],
        'Proxima_Cita': diccionario["Proxima_Cita"],
        'Atendido_Por': diccionario["Atendido_Por"],
        'Observaciones': diccionario["Observaciones"]
    }


@app.route("/resultado", methods=['GET'])
def getResultado():
    response = json_util.dumps(pruebas())
    return Response(response, mimetype='application/json')


@app.route("/image", methods=['GET', 'POST'])
def image():
    if (request.method == "POST"):
        bytesOfImage = request.get_data()
        with open('image.jpeg', 'wb') as out:
            out.write(bytesOfImage)
        return "Image read"


@app.route("/", methods=["GET"])
def getTest():
    return {"message": "API UPC OCR"}


app.register_blueprint(USERS)
app.register_blueprint(CONSULTATIOS)
app.register_blueprint(STORIES)

if __name__ == '__main__':
    # scheduler = APScheduler()
    # scheduler.allowed_hosts = ['localhost:19006']
    # scheduler.init_app(app)
    # scheduler.start()
    app.run()

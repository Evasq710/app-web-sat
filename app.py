from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.etree import ElementTree as ET
from clases import *

app = Flask(__name__)
CORS(app)

solicitudes_DTE = []

def is_number(caracter):
    if ord(caracter) >= 48 and ord(caracter) <= 57:
        return True
    return False
    
def is_letter(caracter):
    if (ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 160 and ord(caracter) <= 165):
        return True
    return False

@app.route('/carga_archivo', methods=['POST'])
def carga_archivo():
    global solicitudes_DTE
    entry = request.data.decode('utf-8')
    entrada = entry.replace('\n', '').replace('\r', '').replace('\t', '').upper()
    root_solicitudes = ET.fromstring(entrada)
    contador = 0
    for solicitud in root_solicitudes.findall("DTE"):
        try:
            tiempo = solicitud.find('TIEMPO').text
            lugar = ""
            dia = ""
            mes = ""
            year = ""
            hora_completa = ""
            hora = ""
            minutos = ""
            estado = "q0"
            lexema_actual = ""
            for caracter in tiempo:
                if estado == "q0":
                    if is_letter(caracter):
                        lexema_actual += caracter
                        estado = "q1"
                    elif ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                        pass
                elif estado == "q1":
                    if is_letter(caracter):
                        lexema_actual += caracter
                    elif ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32 or caracter == ",":
                        lugar = lexema_actual.capitalize()
                        lexema_actual = ""
                        estado = "q2"
                elif estado == "q2":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q3"
                    elif ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                        pass
                elif estado == "q3":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q4"
                elif estado == "q4":
                    if caracter == "/":
                        dia = lexema_actual
                        lexema_actual = ""
                        estado = "q5"
                elif estado == "q5":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q6"
                elif estado == "q6":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q7"
                elif estado == "q7":
                    if caracter == "/":
                        mes = lexema_actual
                        lexema_actual = ""
                        estado = "q8"
                elif estado == "q8":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q9"
                elif estado == "q9":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q10"
                elif estado == "q10":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q11"
                elif estado == "q11":
                    if is_number(caracter):
                        lexema_actual += caracter
                        estado = "q12"
                elif estado == "q12":
                    if ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                        year = lexema_actual
                        lexema_actual = ""
                        estado = "q13"
                elif estado == "q13":
                    if is_number(caracter):
                        hora += caracter
                        lexema_actual += caracter
                        estado = "q14"
                elif estado == "q14":
                    if is_number(caracter):
                        hora += caracter
                        lexema_actual += caracter
                        estado = "q15"
                elif estado == "q15":
                    if caracter == ":":
                        lexema_actual += caracter
                        estado = "q16"
                elif estado == "q16":
                    if is_number(caracter):
                        minutos += caracter
                        lexema_actual += caracter
                        estado = "q17"
                elif estado == "q17":
                    if is_number(caracter):
                        minutos += caracter
                        lexema_actual += caracter
                        estado = "q18"
                elif estado == "q18":
                    if ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                        lexema_actual += caracter
                        estado = "q19"
                    elif is_letter(caracter):
                        lexema_actual += caracter
                        estado = "q19"
                elif estado == "q19":
                    if is_letter(caracter):
                        lexema_actual += caracter
                    elif caracter == ".":
                        lexema_actual += caracter
            hora_completa = lexema_actual.lower()
            referencia = solicitud.find('REFERENCIA').text.replace(' ', '')
            nit_emisor = solicitud.find('NIT_EMISOR').text.replace(' ', '').replace('-', '')
            nit_receptor = solicitud.find('NIT_RECEPTOR').text.replace(' ', '').replace('-', '')
            valor = solicitud.find('VALOR').text.replace(' ', '')
            iva = solicitud.find('IVA').text.replace(' ', '')
            total = solicitud.find('TOTAL').text.replace(' ', '')
            solicitudes_DTE.append(DTE(lugar, dia, mes, year,hora, minutos, hora_completa, referencia, nit_emisor, nit_receptor, valor, iva, total))
            contador += 1
        except:
            continue

    referencias = []
    for solicitud in solicitudes_DTE:
        referencias.append(solicitud.referencia)
    ref_repetidas = []
    for referencia in referencias:
        if referencias.count(referencia) > 1:
            if ref_repetidas.count(referencia) == 0:
                ref_repetidas.append(referencia)
    for repetida in ref_repetidas:
        for solicitud in solicitudes_DTE:
            if solicitud.referencia == repetida:
                solicitud.error_referencia_doble = True

    bubbleSort_fecha()
    bubbleSort_hora()
    correlativos()
    crear_archivo_salida()

    for solicitud in solicitudes_DTE:
        print(solicitud.fecha, solicitud.hora_completa, solicitud.num_autorizacion)

    return jsonify({'nuevas': contador, 'total_guardadas': len(solicitudes_DTE)})

def bubbleSort_fecha():
    global solicitudes_DTE
    solicitudes_aux = None
    while (True):
        cambios = False
        for i in range(1, len(solicitudes_DTE)):
            if solicitudes_DTE[i].fecha_concatenada < solicitudes_DTE[i-1].fecha_concatenada:
                solicitudes_aux = solicitudes_DTE[i]
                solicitudes_DTE[i] = solicitudes_DTE[i-1] #pasando el mayor una posición adelante
                solicitudes_DTE[i-1] = solicitudes_aux #pasando al menor una posición atras
                cambios = True
        if not cambios: #lista ordenada
            break

def bubbleSort_hora():
    global solicitudes_DTE
    solicitudes_aux = None
    for solicitud in solicitudes_DTE:
        fecha = solicitud.fecha_concatenada
        while (True):
            cambios = False
            for i in range(1, len(solicitudes_DTE)):
                if solicitudes_DTE[i].hora < solicitudes_DTE[i-1].hora and solicitudes_DTE[i-1].fecha_concatenada == fecha and solicitudes_DTE[i].fecha_concatenada == fecha:
                    solicitudes_aux = solicitudes_DTE[i]
                    solicitudes_DTE[i] = solicitudes_DTE[i-1] #pasando el mayor una posición adelante
                    solicitudes_DTE[i-1] = solicitudes_aux #pasando al menor una posición atras
                    cambios = True
            if not cambios: #lista ordenada
                break
    for solicitud in solicitudes_DTE:
        fecha = solicitud.fecha_concatenada
        hora = solicitud.hora
        while (True):
            cambios = False
            for i in range(1, len(solicitudes_DTE)):
                if solicitudes_DTE[i].minutos < solicitudes_DTE[i-1].minutos and solicitudes_DTE[i-1].hora == hora and solicitudes_DTE[i].hora == hora and solicitudes_DTE[i-1].fecha_concatenada == fecha and solicitudes_DTE[i].fecha_concatenada == fecha:
                    solicitudes_aux = solicitudes_DTE[i]
                    solicitudes_DTE[i] = solicitudes_DTE[i-1] #pasando el mayor una posición adelante
                    solicitudes_DTE[i-1] = solicitudes_aux #pasando al menor una posición atras
                    cambios = True
            if not cambios: #lista ordenada
                break

def correlativos():
    global solicitudes_DTE
    fechas = []
    for solicitud in solicitudes_DTE:
        if fechas.count(solicitud.fecha_concatenada) == 0:
            fechas.append(solicitud.fecha_concatenada)
    for fecha in fechas:
        correlativo = 0
        for solicitud in solicitudes_DTE:
            if solicitud.fecha_concatenada == fecha:
                correlativo += 1
                solicitud.crear_num_autorizacion(correlativo)

def crear_archivo_salida():
    pass

#Test de que el server está corriendo (GET por default)
@app.route('/ping')
def ping():
    return jsonify({"message": "pong!"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)
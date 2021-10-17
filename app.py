from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.etree import ElementTree as ET

from jinja2.utils import object_type_repr

app = Flask(__name__)
CORS(app)


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
    entry = request.data.decode('utf-8')
    entrada = entry.replace('\n', '').replace('\r', '').replace('\t', '').upper()
    root_solicitudes = ET.fromstring(entrada)
    for solicitud in root_solicitudes.findall("DTE"):
        tiempo = solicitud.find('TIEMPO').text
        lugar = ""
        dia = ""
        mes = ""
        year = ""
        hora = ""
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
                    dia = int(lexema_actual)
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
                    mes = int(lexema_actual)
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
                    year = int(lexema_actual)
                    lexema_actual = ""
                    estado = "q13"
            elif estado == "q13":
                if is_number(caracter):
                    lexema_actual += caracter
                    estado = "q14"
            elif estado == "q14":
                if is_number(caracter):
                    lexema_actual += caracter
                    estado = "q15"
            elif estado == "q15":
                if caracter == ":":
                    lexema_actual += caracter
                    estado = "q16"
            elif estado == "q16":
                if is_number(caracter):
                    lexema_actual += caracter
                    estado = "q17"
            elif estado == "q17":
                if is_number(caracter):
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
        hora = lexema_actual.lower()
        referencia = solicitud.find('REFERENCIA').text.replace(' ', '')
        nit_emisor = solicitud.find('NIT_EMISOR').text.replace(' ', '')
        nit_receptor = solicitud.find('NIT_RECEPTOR').text.replace(' ', '')
        valor = solicitud.find('VALOR').text.replace(' ', '')
        valor = float(valor)
        iva = solicitud.find('IVA').text.replace(' ', '')
        iva = float(iva)
        total = solicitud.find('TOTAL').text.replace(' ', '')
        total = float(iva)
        print(lugar, end= ' ')
        print(dia, end= ' / ')
        print(mes, end= ' / ')
        print(year, end= ' ')
        print(hora, end= ' ')
        print(referencia, end= ' ')
        print(nit_emisor, end= ' ')
        print(nit_receptor, end= ' ')
        print(valor, end= ' ')
        print(iva, end= ' ')
        print(total)
    return jsonify({'entrada': entrada})

#Test de que el server está corriendo (GET por default)
@app.route('/ping')
def ping():
    return jsonify({"message": "pong!"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)
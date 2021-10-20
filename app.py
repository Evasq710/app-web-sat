from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.etree import ElementTree as ET
from clases import *

app = Flask(__name__)
CORS(app)

solicitudes_DTE = []
autorizaciones_global = []

@app.route('/actualizar')
def actualizar_aprobaciones():
    global autorizaciones_global
    tree_xml_autorizaciones = ET.parse('autorizaciones.xml')
    root_autorizaciones = tree_xml_autorizaciones.getroot()
    for autorizacion in root_autorizaciones:
        fecha = autorizacion.find('FECHA').text
        facturas_recibidas = int(autorizacion.find('FACTURAS_RECIBIDAS').text)
        errores_nit_emisor = int(autorizacion.find('ERRORES').find('NIT_EMISOR').text)
        errores_nit_receptor = int(autorizacion.find('ERRORES').find('NIT_RECEPTOR').text)
        errores_iva = int(autorizacion.find('ERRORES').find('IVA').text)
        errores_total = int(autorizacion.find('ERRORES').find('TOTAL').text)
        errores_ref_doble = int(autorizacion.find('ERRORES').find('REFERENCIA_DUPLICADA').text)
        facturas_correctas = int(autorizacion.find('FACTURAS_CORRECTAS').text)
        emisores = int(autorizacion.find('CANTIDAD_EMISORES').text)
        receptores = int(autorizacion.find('CANTIDAD_RECEPTORES').text)
        lista_aprobaciones = []
        for aprobacion in autorizacion.find('LISTADO_AUTORIZACIONES').findall('APROBACION'):
            referencia = aprobacion.find('NIT_EMISOR').attrib
            nit_emisor = aprobacion.find('NIT_EMISOR').text
            codigo_aprobacion = int(aprobacion.find('CODIGO_APROBACION').text)
            lista_aprobaciones.append({'referencia': referencia, 'nit_emisor': nit_emisor, 'codigo_aprobacion': codigo_aprobacion})
        total_aprobaciones = int(autorizacion.find('LISTADO_AUTORIZACIONES').find('TOTAL_APROBACIONES').text)
        autorizaciones_global.append(Autorizacion(
            fecha, facturas_recibidas, errores_nit_emisor, errores_nit_receptor, errores_iva, errores_total, errores_ref_doble,
            facturas_correctas, emisores, receptores, lista_aprobaciones, total_aprobaciones
            ))
            
    return jsonify({'autorizaciones': len(autorizaciones_global)})

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
    solicitudes_DTE = []
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
            hora_completa = lexema_actual.lower()
            referencia = solicitud.find('REFERENCIA').text.replace(' ', '')
            nit_emisor = solicitud.find('NIT_EMISOR').text.replace(' ', '').replace('-', '')
            nit_receptor = solicitud.find('NIT_RECEPTOR').text.replace(' ', '').replace('-', '')
            valor = solicitud.find('VALOR').text.replace(' ', '')
            iva = solicitud.find('IVA').text.replace(' ', '')
            total = solicitud.find('TOTAL').text.replace(' ', '')
            solicitudes_DTE.append(DTE(lugar, dia, mes, year, hora_completa, referencia, nit_emisor, nit_receptor, valor, iva, total))
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
                solicitud.factura_aprobada = False

    bubbleSort_fecha()
    correlativos()
    resumen_autorizaciones()

    return jsonify({'solicitudes_recibidas': contador, 'total_analizadas': len(solicitudes_DTE)})

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
                if solicitud.factura_aprobada:
                    correlativo += 1
                    solicitud.crear_num_autorizacion(correlativo)

def resumen_autorizaciones():
    global solicitudes_DTE
    autorizaciones = []
    fechas = []
    for solicitud in solicitudes_DTE:
        if fechas.count(solicitud.fecha) == 0:
            fechas.append(solicitud.fecha)
    for fecha in fechas:
        total_facturas = 0
        errores_nit_emisor = 0
        errores_nit_receptor = 0
        errores_iva = 0
        errores_total = 0
        errores_referencia = 0
        facturas_sin_error = 0
        emisores = []
        receptores = []
        hay_error = False
        facturas_con_error = 0
        for solicitud in solicitudes_DTE:
            if solicitud.fecha == fecha:
                total_facturas += 1
                if solicitud.error_nit_emisor:
                    errores_nit_emisor += 1
                    hay_error = True
                if solicitud.error_nit_receptor:
                    errores_nit_receptor += 1
                    hay_error = True
                if solicitud.error_iva:
                    errores_iva += 1
                    hay_error = True
                if solicitud.error_total:
                    errores_total += 1
                    hay_error = True
                if solicitud.error_referencia_doble:
                    errores_referencia += 1
                    hay_error = True
                if hay_error:
                    facturas_con_error += 1
                if emisores.count(solicitud.nit_emisor) == 0 and not solicitud.error_nit_emisor:
                    emisores.append(solicitud.nit_emisor)
                if receptores.count(solicitud.nit_receptor) == 0 and not solicitud.error_nit_receptor:
                    receptores.append(solicitud.nit_receptor)
        facturas_sin_error = total_facturas - facturas_con_error
        total_emisores = len(emisores)
        total_receptores = len(receptores)
        lista_facturas_aprobadas = []
        for solicitud in solicitudes_DTE:
            if solicitud.fecha == fecha and solicitud.factura_aprobada:
                lista_facturas_aprobadas.append(solicitud)
        autorizaciones.append(Autorizacion(fecha, total_facturas, errores_nit_emisor, errores_nit_receptor, errores_iva, errores_total, errores_referencia, facturas_sin_error, total_emisores, total_receptores, lista_facturas_aprobadas))
    crear_archivo_salida(autorizaciones)
    
def crear_archivo_salida(autorizaciones):
    xml = "<LISTAAUTORIZACIONES>\n"
    for autorizacion in autorizaciones:
        xml += "\t<AUTORIZACION>\n"
        xml += f"\t\t<FECHA>{autorizacion.fecha}</FECHA>\n"
        xml += f"\t\t<FACTURAS_RECIBIDAS>{autorizacion.total_facturas}</FACTURAS_RECIBIDAS>\n"
        xml += "\t\t<ERRORES>\n"
        xml += f"\t\t\t<NIT_EMISOR>{autorizacion.errores_nit_emisor}</NIT_EMISOR>\n"
        xml += f"\t\t\t<NIT_RECEPTOR>{autorizacion.errores_nit_receptor}</NIT_RECEPTOR>\n"
        xml += f"\t\t\t<IVA>{autorizacion.errores_iva}</IVA>\n"
        xml += f"\t\t\t<TOTAL>{autorizacion.errores_total}</TOTAL>\n"
        xml += f"\t\t\t<REFERENCIA_DUPLICADA>{autorizacion.errores_referencia}</REFERENCIA_DUPLICADA>\n"
        xml += "\t\t</ERRORES>\n"
        xml += f"\t\t<FACTURAS_CORRECTAS>{autorizacion.facturas_sin_error}</FACTURAS_CORRECTAS>\n"
        xml += f"\t\t<CANTIDAD_EMISORES>{autorizacion.total_emisores}</CANTIDAD_EMISORES>\n"
        xml += f"\t\t<CANTIDAD_RECEPTORES>{autorizacion.total_receptores}</CANTIDAD_RECEPTORES>\n"
        xml += "\t\t<LISTADO_AUTORIZACIONES>\n"
        for factura in autorizacion.lista_facturas_aprobadas:
            xml += "\t\t\t<APROBACION>\n"
            xml += f'\t\t\t\t<NIT_EMISOR ref="{factura.referencia}">{factura.nit_emisor}</NIT_EMISOR>\n'
            xml += f'\t\t\t\t<CODIGO_APROBACION>{factura.num_autorizacion}</CODIGO_APROBACION>\n'
            xml += "\t\t\t</APROBACION>\n"
        xml += "\t\t</LISTADO_AUTORIZACIONES>\n"
        xml += "\t</AUTORIZACION>\n"
    xml += '</LISTAAUTORIZACIONES>'
    try:
        root = ET.fromstring(xml)
        tree_xml_salida = ET.ElementTree(element=root)
        tree_xml_salida.write("autorizaciones.xml", encoding="utf-8", xml_declaration=True)
        print("> El archivo XML se creo exitosamente.\n")
    except Exception as e:
        print(e)
        print("> No pudo crearse el archivo XML en la ruta indicada.\n")
    

#Test de que el server está corriendo (GET por default)
@app.route('/ping')
def ping():
    return jsonify({"message": "pong!"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)
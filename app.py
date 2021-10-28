from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.etree import ElementTree as ET
from clases import *
import json

app = Flask(__name__)
CORS(app)

autorizaciones_global = []
data_JSON = ""
solicitudes_DTE = []
solicitudes_rechazadas = []

@app.route('/actualizar')
def actualizar_aprobaciones():
    global autorizaciones_global
    global data_JSON
    autorizaciones_global = []
    with open('aprobaciones.json') as apr_JSON:
        data_JSON = json.load(apr_JSON)
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
        for aut_JSON in data_JSON['autorizaciones']:
            if aut_JSON['fecha'] == fecha:
                for aprobacion in aut_JSON['aprobaciones']:
                    referencia = aprobacion['referencia']
                    nit_emisor = aprobacion['nit_emisor']
                    codigo_aprobacion = aprobacion['codigo_aprobacion']
                    nit_receptor_DB = aprobacion['nit_receptor_DB']
                    valor_DB = aprobacion['valor_DB']
                    iva_DB = aprobacion['iva_DB']
                    total_DB = aprobacion['total_DB']
                    lista_aprobaciones.append(Aprobacion(
                        referencia, nit_emisor, codigo_aprobacion, nit_receptor_DB, valor_DB, iva_DB, total_DB
                        ))
                break
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

@app.route('/carga_solicitudes', methods=['POST'])
def carga_archivo():
    global autorizaciones_global
    global solicitudes_DTE
    global solicitudes_rechazadas
    solicitudes_DTE = []
    
    entry = request.data.decode('utf-8')
    entrada = entry.replace('\n', '').replace('\r', '').replace('\t', '').upper()
    try:
        root_solicitudes = ET.fromstring(entrada)
    except Exception as e:
        print(e)
        return jsonify({'exito': False})
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

    validacion_ref_dobles()
    bubbleSort_fecha()
    rechazar_solicitudes()
    correctas = len(solicitudes_DTE)
    incorrectas = len(solicitudes_rechazadas)
    correlativos()
    actualizar_errores()
    solo_errores()
    bubbleSort_fecha_autorizaciones()
    crear_xml_salida()
    crear_dataJSON()

    return jsonify({'exito': True, 'solicitudes_recibidas': contador, 'facturas_correctas': correctas, 'facturas_malas': incorrectas,
    'solicitudes_sin_analizar': len(solicitudes_DTE), 'rechazadas_sin_analizar': len(solicitudes_rechazadas), 'aut_total': len(autorizaciones_global)})

def validacion_ref_dobles():
    global solicitudes_DTE
    global autorizaciones_global

    referencias_nuevas = []
    for solicitud in solicitudes_DTE:
        referencias_nuevas.append(solicitud.referencia)
    referencias_antiguas = []
    for autorizacion in autorizaciones_global:
        for aprobacion in autorizacion.lista_facturas_aprobadas:
            referencias_antiguas.append(aprobacion.referencia)

    # Validando referencias repetidas dentro de las solicitudes
    ref_repetidas = []
    for referencia in referencias_nuevas:
        if referencias_nuevas.count(referencia) > 1:
            if ref_repetidas.count(referencia) == 0:
                ref_repetidas.append(referencia)
    # Validando referencias repetidas entre las solicitudes y las referencias ya guardadas previamente
    for ref_nueva in referencias_nuevas:
        for ref_antigua in referencias_antiguas:
            if ref_nueva == ref_antigua:
                if ref_repetidas.count(ref_nueva) == 0:
                    ref_repetidas.append(ref_nueva)
                    break

    for repetida in ref_repetidas:
        for solicitud in solicitudes_DTE:
            if solicitud.referencia == repetida:
                solicitud.error_referencia_doble = True
                solicitud.factura_aprobada = False

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

def rechazar_solicitudes():
    global solicitudes_DTE
    global solicitudes_rechazadas
    solicitudes_rechazadas = []
    list_index = []
    index = 0
    for solicitud in solicitudes_DTE:
        if not solicitud.factura_aprobada:
            solicitudes_rechazadas.append(solicitud)
            list_index.append(index)
        else:
            index += 1
    for i in list_index:
        del solicitudes_DTE[i]

def correlativos():
    global solicitudes_DTE
    global autorizaciones_global
    # Guardando las nuevas fechas, solo de las facturas aprobadas
    fechas_nuevas = []
    for solicitud in solicitudes_DTE:
        if fechas_nuevas.count(solicitud.fecha) == 0:
            fechas_nuevas.append(solicitud.fecha)
    # Guardando fechas de las que ya se cuenta registro
    fechas_antiguas = []
    for autorizacion in autorizaciones_global:
        fechas_antiguas.append(autorizacion.fecha)

    print(f"Solicitudes correctas: {len(solicitudes_DTE)}")

    for fecha in fechas_nuevas:
        if fechas_antiguas.count(fecha) > 0: # La fecha ya se encuentra registrada
            print(fecha, "ya se encuentra registrada")
            for autorizacion in autorizaciones_global:
                if fecha == autorizacion.fecha:
                    correlativo = autorizacion.total_aprobaciones
                    nuevas_aprobaciones = []
                    list_index = []
                    index = 0
                    agregadas = 0
                    for solicitud in solicitudes_DTE:
                        if solicitud.fecha == fecha:
                            correlativo += 1
                            agregadas += 1
                            solicitud.crear_num_autorizacion(correlativo)
                            nuevas_aprobaciones.append(Aprobacion(
                                solicitud.referencia, solicitud.nit_emisor, solicitud.num_autorizacion, solicitud.nit_receptor, solicitud.valor, solicitud.iva, solicitud.total
                            ))
                            list_index.append(index)
                        else:
                            index += 1
                    for i in list_index:
                        del solicitudes_DTE[i]
                    actualizar_aprobaciones(fecha, nuevas_aprobaciones)
                    print(f"Coinciden con {fecha} {agregadas} solicitudes")
                    break
        else: # La fecha no está registrada previamente
            print(fecha, "no se encuentra registrada")
            correlativo = 0
            nuevas_aprobaciones = []
            index = 0
            list_index = []
            iteraciones = 0
            for solicitud in solicitudes_DTE:
                iteraciones += 1
                if solicitud.fecha == fecha:
                    correlativo += 1
                    solicitud.crear_num_autorizacion(correlativo)
                    nuevas_aprobaciones.append(Aprobacion(
                        solicitud.referencia, solicitud.nit_emisor, solicitud.num_autorizacion, solicitud.nit_receptor, solicitud.valor, solicitud.iva, solicitud.total
                    ))
                    list_index.append(index)
                else:
                    index += 1
            for i in list_index:
                del solicitudes_DTE[i]
            print(f"Coinciden con {fecha} {correlativo} solicitudes")
            crear_autorizacion(fecha, nuevas_aprobaciones)

def actualizar_aprobaciones(fecha, nuevas_aprobaciones):
    global autorizaciones_global
    global data_JSON
    for autorizacion in autorizaciones_global:
        if autorizacion.fecha == fecha:
            autorizacion.agregar_aprobaciones(nuevas_aprobaciones)
            for aut in data_JSON['autorizaciones']:
                if aut['fecha'] == fecha:
                    for aprobacion in nuevas_aprobaciones:
                        aut['aprobaciones'].append({
                            "referencia": aprobacion.referencia,
                            "nit_emisor": aprobacion.nit_emisor,
                            "codigo_aprobacion": aprobacion.codigo_aprobacion,
                            "nit_receptor_DB": aprobacion.nit_receptor_DB,
                            "valor_DB": aprobacion.valor_DB,
                            "iva_DB": aprobacion.iva_DB,
                            "total_DB": aprobacion.total_DB
                        })
                    break

def crear_autorizacion(fecha, nuevas_aprobaciones):
    global solicitudes_rechazadas
    global autorizaciones_global
    global data_JSON
    facturas_malas = []
    index = 0
    list_index = []
    for factura_mala in solicitudes_rechazadas:
        if factura_mala.fecha == fecha:
            facturas_malas.append(factura_mala)
            list_index.append(index)
        else:
            index += 1
    for i in list_index:
        del solicitudes_rechazadas[i]

    errores_nit_emisor = 0
    errores_nit_receptor = 0
    errores_iva = 0
    errores_total = 0
    errores_referencia = 0
    for factura_mala in facturas_malas:
        if factura_mala.error_nit_emisor:
            errores_nit_emisor += 1
        if factura_mala.error_nit_receptor:
            errores_nit_receptor += 1
        if factura_mala.error_iva:
            errores_iva += 1
        if factura_mala.error_total:
            errores_total += 1
        if factura_mala.error_referencia_doble:
            errores_referencia += 1
    nit_emisores = []
    for aprobacion in nuevas_aprobaciones:
        if nit_emisores.count(aprobacion.nit_emisor) == 0:
            nit_emisores.append(aprobacion.nit_emisor)
    for factura_mala in facturas_malas:
        if not factura_mala.error_nit_emisor:
            if nit_emisores.count(factura_mala.nit_emisor) == 0:
                nit_emisores.append(factura_mala.nit_emisor)
    nit_receptores = []
    for aprobacion in nuevas_aprobaciones:
        if nit_receptores.count(aprobacion.nit_receptor_DB) == 0:
            nit_receptores.append(aprobacion.nit_receptor_DB)
    for factura_mala in facturas_malas:
        if not factura_mala.error_nit_receptor:
            if nit_receptores.count(factura_mala.nit_receptor) == 0:
                nit_receptores.append(factura_mala.nit_receptor)
    new_Aut = Autorizacion(fecha, len(facturas_malas)+len(nuevas_aprobaciones), errores_nit_emisor, errores_nit_receptor, errores_iva,
    errores_total, errores_referencia, len(nuevas_aprobaciones), len(nit_emisores), len(nit_receptores), nuevas_aprobaciones, len(nuevas_aprobaciones))    
    autorizaciones_global.append(new_Aut)

    aprobaciones = []
    for aprobacion in nuevas_aprobaciones:
        aprobaciones.append({
            "referencia": aprobacion.referencia,
            "nit_emisor": aprobacion.nit_emisor,
            "codigo_aprobacion": aprobacion.codigo_aprobacion,
            "nit_receptor_DB": aprobacion.nit_receptor_DB,
            "valor_DB": aprobacion.valor_DB,
            "iva_DB": aprobacion.iva_DB,
            "total_DB": aprobacion.total_DB
        })
    data_JSON['autorizaciones'].append({"fecha": fecha, "aprobaciones": aprobaciones})

def actualizar_errores():
    global autorizaciones_global
    global solicitudes_rechazadas
    fechas = []
    for factura in solicitudes_rechazadas:
        if fechas.count(factura.fecha) == 0:
            fechas.append(factura.fecha)
    fechas_antiguas = []
    for autorizacion in autorizaciones_global:
        fechas_antiguas.append(autorizacion.fecha)
    
    for fecha in fechas:
        if fechas_antiguas.count(fecha) > 0: # La fecha ya se encuentra registrada
            for autorizacion in autorizaciones_global:
                if fecha == autorizacion.fecha:
                    facturas_malas = 0
                    errores_nit_emisor = 0
                    errores_nit_receptor = 0
                    errores_iva = 0
                    errores_total = 0
                    errores_referencia = 0
                    nit_emisores = []
                    nit_receptores = []
                    index = 0
                    list_index = []
                    for factura_rechazada in solicitudes_rechazadas:
                        if factura_rechazada.fecha == fecha:
                            facturas_malas += 1
                            if factura_rechazada.error_nit_emisor:
                                errores_nit_emisor += 1
                            if factura_rechazada.error_nit_receptor:
                                errores_nit_receptor += 1
                            if factura_rechazada.error_iva:
                                errores_iva += 1
                            if factura_rechazada.error_total:
                                errores_total += 1
                            if factura_rechazada.error_referencia_doble:
                                errores_referencia += 1
                            if not factura_rechazada.error_nit_emisor:
                                if nit_emisores.count(factura_rechazada.nit_emisor) == 0:
                                    nit_emisores.append(factura_rechazada.nit_emisor)
                            if not factura_rechazada.error_nit_receptor:
                                if nit_receptores.count(factura_rechazada.nit_receptor) == 0:
                                    nit_receptores.append(factura_rechazada.nit_receptor)
                            list_index.append(index)
                        else:
                            index += 1
                    for i in list_index:
                        del solicitudes_rechazadas[i]
                    autorizacion.agregar_errores(facturas_malas, errores_nit_emisor, errores_nit_receptor, errores_iva,
                    errores_total, errores_referencia, len(nit_emisores), len(nit_receptores))
                    break

def solo_errores():
    global solicitudes_rechazadas
    global autorizaciones_global
    fechas = []
    for factura in solicitudes_rechazadas:
        if fechas.count(factura.fecha) == 0:
            fechas.append(factura.fecha)
    for fecha in fechas:
        facturas_malas = []
        index = 0
        list_index = []
        for factura_mala in solicitudes_rechazadas:
            if factura_mala.fecha == fecha:
                facturas_malas.append(factura_mala)
                list_index.append(index)
            else:
                index += 1
        for i in list_index:
            del solicitudes_rechazadas[i]
        errores_nit_emisor = 0
        errores_nit_receptor = 0
        errores_iva = 0
        errores_total = 0
        errores_referencia = 0
        for factura_mala in facturas_malas:
            if factura_mala.error_nit_emisor:
                errores_nit_emisor += 1
            if factura_mala.error_nit_receptor:
                errores_nit_receptor += 1
            if factura_mala.error_iva:
                errores_iva += 1
            if factura_mala.error_total:
                errores_total += 1
            if factura_mala.error_referencia_doble:
                errores_referencia += 1
        nit_emisores = []
        for factura_mala in facturas_malas:
            if not factura_mala.error_nit_emisor:
                if nit_emisores.count(factura_mala.nit_emisor) == 0:
                    nit_emisores.append(factura_mala.nit_emisor)
        nit_receptores = []
        for factura_mala in facturas_malas:
            if not factura_mala.error_nit_receptor:
                if nit_receptores.count(factura_mala.nit_receptor) == 0:
                    nit_receptores.append(factura_mala.nit_receptor)
        Aut = Autorizacion(fecha, len(facturas_malas), errores_nit_emisor, errores_nit_receptor, errores_iva, errores_total, errores_referencia,
        0, len(nit_emisores), len(nit_receptores), [], 0)
        autorizaciones_global.append(Aut)

def bubbleSort_fecha_autorizaciones():
    global autorizaciones_global
    autorizaciones_aux = None
    while (True):
        cambios = False
        for i in range(1, len(autorizaciones_global)):
            if autorizaciones_global[i].fecha_concatenada < autorizaciones_global[i-1].fecha_concatenada:
                autorizaciones_aux = autorizaciones_global[i]
                autorizaciones_global[i] = autorizaciones_global[i-1] #pasando el mayor una posición adelante
                autorizaciones_global[i-1] = autorizaciones_aux #pasando al menor una posición atras
                cambios = True
        if not cambios: #lista ordenada
            break

def crear_xml_salida():
    global autorizaciones_global
    xml = "<LISTAAUTORIZACIONES>\n"
    for autorizacion in autorizaciones_global:
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
            xml += f'\t\t\t\t<CODIGO_APROBACION>{factura.codigo_aprobacion}</CODIGO_APROBACION>\n'
            xml += "\t\t\t</APROBACION>\n"
        xml += f"\t\t\t<TOTAL_APROBACIONES>{len(autorizacion.lista_facturas_aprobadas)}</TOTAL_APROBACIONES>\n"
        xml += "\t\t</LISTADO_AUTORIZACIONES>\n"
        xml += "\t</AUTORIZACION>\n"
    xml += '</LISTAAUTORIZACIONES>'
    try:
        root = ET.fromstring(xml)
        tree_xml_salida = ET.ElementTree(element=root)
        tree_xml_salida.write("autorizaciones.xml", encoding="utf-8", xml_declaration=True)
        print("> El archivo XML se creo exitosamente.")
    except Exception as e:
        print(e)
        print("> No pudo crearse el archivo XML.")

def crear_dataJSON():
    global data_JSON
    try:
        with open('aprobaciones.json', 'w') as file_apr:
            json.dump(data_JSON, file_apr, indent=2)
        print("> El archivo JSON se creo exitosamente.")
    except Exception as e:
        print(e)
        print("> No pudo crearse el archivo JSON.")

@app.route('/autorizaciones')
def get_autorizaciones():
    global autorizaciones_global
    autorizaciones = []
    id_aut = 0
    for autorizacion in autorizaciones_global:
        aprobaciones = []
        for aprobacion in autorizacion.lista_facturas_aprobadas:
            apr = {
                'referencia': aprobacion.referencia,
                'nit_emisor': aprobacion.nit_emisor,
                'codigo_aprobacion': aprobacion.codigo_aprobacion
            }
            aprobaciones.append(apr)

        id_aut += 1
        aut = {
            'id_aut': f"fecha{id_aut}",
            'fecha': autorizacion.fecha,
            'total_facturas': autorizacion.total_facturas,
            'errores_nit_emisor': autorizacion.errores_nit_emisor,
            'errores_nit_receptor': autorizacion.errores_nit_receptor,
            'errores_iva': autorizacion.errores_iva,
            'errores_total': autorizacion.errores_total,
            'errores_referencia': autorizacion.errores_referencia,
            'facturas_sin_error': autorizacion.facturas_sin_error,
            'total_emisores': autorizacion.total_emisores,
            'total_receptores': autorizacion.total_receptores,
            'lista_aprobaciones': aprobaciones,
            'total_aprobaciones': autorizacion.total_aprobaciones
        }
        autorizaciones.append(aut)
    return jsonify(autorizaciones)

@app.route('/autorizaciones/reset', methods=['DELETE'])
def reset_autorizaciones():
    global autorizaciones_global
    global data_JSON

    autorizaciones_global = []
    crear_xml_salida()

    aprobaciones = '''{
        "autorizaciones": [
        ]
    }'''
    try:
        file_json = open('aprobaciones.json', 'w')
        file_json.write(aprobaciones)
        file_json.close()
        print("> El archivo JSON se creo exitosamente.")
        with open('aprobaciones.json') as apr_JSON:
            data_JSON = json.load(apr_JSON)
        return jsonify({'exito': True})
    except Exception as e:
        print(e)
        print("> No pudo crearse el archivo JSON.")
        return jsonify({'exito': False})

@app.route('/movimientos_nit/<string:fecha>')
def get_movimientos_fecha(fecha):
    global autorizaciones_global
    
    arr_fecha = fecha.split('-')
    fecha = arr_fecha[0] + "/" + arr_fecha[1] + "/" + arr_fecha[2]

    for autorizacion in autorizaciones_global:
        if fecha == autorizacion.fecha:
            nits = []
            for aprobacion in autorizacion.lista_facturas_aprobadas:
                if nits.count(aprobacion.nit_emisor) == 0:
                    nits.append(aprobacion.nit_emisor)
                if nits.count(aprobacion.nit_receptor_DB) == 0:
                    nits.append(aprobacion.nit_receptor_DB)

            movimientos = []
            for nit in nits:
                iva_emitido = 0
                iva_recibido = 0
                for aprobacion in autorizacion.lista_facturas_aprobadas:
                    if aprobacion.nit_emisor == nit:
                        iva_emitido += aprobacion.iva_DB
                    if aprobacion.nit_receptor_DB == nit:
                        iva_recibido += aprobacion.iva_DB
                movimiento = {
                    'nit': nit,
                    'iva_emitido': iva_emitido,
                    'iva_recibido': iva_recibido
                }
                movimientos.append(movimiento)

            return jsonify({'exito': True, 'movimientos': movimientos})

    return jsonify({'exito': False})

#Test de que el server está corriendo (GET por default)
@app.route('/ping')
def ping():
    return jsonify({"message": "pong!"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)
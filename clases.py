class DTE:
    def __init__(self, lugar, dia, mes, year, hora, minutos, hora_completa, referencia, nit_emisor, nit_receptor, valor, iva, total):
        self.lugar = lugar
        self.fecha = f"{dia}/{mes}/{year}"
        self.fecha_concatenada = int(f"{year}{mes}{dia}")
        self.hora = int(hora)
        self.minutos = int(minutos)
        self.hora_completa = hora_completa
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        try:
            self.error_valor = False
            self.valor = float(valor)
            if self.valor < 0:
                self.error_valor = True
                self.factura_aprobada = False
        except:
            self.error_valor = True
            self.factura_aprobada = False
        try:
            self.error_iva = False
            self.iva = float(iva)
        except:
            self.error_iva = True
            self.factura_aprobada = False
        try:
            self.error_total = False
            self.total = float(total)
        except:
            self.error_total = True
            self.factura_aprobada = False
        self.error_referencia_doble = False
        self.error_nit_emisor = False
        self.error_nit_receptor = False
        self.factura_aprobada = True
        self.validar_nit_emisor()
        self.validar_nit_receptor()
        self.validar_iva_total()
    
    def validar_nit_emisor(self):
        nit_inverso = self.nit_emisor[::-1]
        # Productos numero*posicion
        productos_caracter_posicion = []
        pos = 1
        for caracter in nit_inverso:
            if pos == 1:
                pos += 1
            else:
                try:
                    productos_caracter_posicion.append(int(caracter)*pos)
                    pos += 1
                except:
                    self.error_nit_emisor = True
                    self.factura_aprobada = False
                    return
        # Suma de productos
        suma = 0
        for producto in productos_caracter_posicion:
            suma += producto
        # Modulo 11 de la sumatoria
        modulo1 = suma % 11
        # 11 - módulo
        resta = 11 - modulo1
        # Módulo 11 de la resta
        modulo2 = resta % 11
        if modulo2 >= 0 and modulo2 <= 9:
            try:
                if modulo2 != int(nit_inverso[0]):
                    self.error_nit_emisor = True
                    self.factura_aprobada = False
            except:
                self.error_nit_emisor = True
                self.factura_aprobada = False
        elif modulo2 == 10:
            if nit_inverso[0] != "K":
                self.error_nit_emisor = True
                self.factura_aprobada = False
        else:
            self.error_nit_emisor = True
            self.factura_aprobada = False
    
    def validar_nit_receptor(self):
        nit_inverso = self.nit_receptor[::-1]
        # Productos numero*posicion
        productos_caracter_posicion = []
        pos = 1
        for caracter in nit_inverso:
            if pos == 1:
                pos += 1
            else:
                try:
                    productos_caracter_posicion.append(int(caracter)*pos)
                    pos += 1
                except:
                    self.error_nit_emisor = True
                    self.factura_aprobada = False
                    return
        # Suma de productos
        suma = 0
        for producto in productos_caracter_posicion:
            suma += producto
        # Modulo 11 de la sumatoria
        modulo1 = suma % 11
        # 11 - módulo
        resta = 11 - modulo1
        # Módulo 11 de la resta
        modulo2 = resta % 11
        if modulo2 >= 0 and modulo2 <= 9:
            try:
                if modulo2 != int(nit_inverso[0]):
                    self.error_nit_receptor = True
                    self.factura_aprobada = False
            except:
                self.error_nit_receptor = True
                self.factura_aprobada = False
        elif modulo2 == 10:
            if nit_inverso[0] != "K":
                self.error_nit_receptor = True
                self.factura_aprobada = False
        else:
            self.error_nit_receptor = True
            self.factura_aprobada = False

    def validar_iva_total(self):
        if not self.error_valor:
            iva = round(self.valor*0.12, 2)
            if not self.error_iva:
                if iva != self.iva:
                    self.error_iva = True
                    self.factura_aprobada = False
            total = iva + self.valor
            if not self.error_total:
                if total != self.total:
                    self.error_total = True
                    self.factura_aprobada = False
        else:
            self.error_iva = True
            self.error_total = True
            self.factura_aprobada = False
    
    def crear_num_autorizacion(self, correlativo):
        str_correlativo = ""
        for i in range(8 - len(str(correlativo))):
            str_correlativo += "0"
        str_correlativo += str(correlativo)
        self.num_autorizacion = int(f"{self.fecha_concatenada}{str_correlativo}")

class Autorizacion:
    def __init__(self, fecha, total_facturas, errores_nit_emisor, errores_nit_receptor, errores_iva, errores_total, errores_referencia, facturas_sin_error, total_emisores, total_receptores, lista_facturas_aprobadas):
        self.fecha = fecha
        self.total_facturas = total_facturas
        self.errores_nit_emisor = errores_nit_emisor
        self.errores_nit_receptor = errores_nit_receptor
        self.errores_iva = errores_iva
        self.errores_total = errores_total
        self.errores_referencia = errores_referencia
        self.facturas_sin_error = facturas_sin_error
        self.total_emisores = total_emisores
        self.total_receptores = total_receptores
        self.lista_facturas_aprobadas = lista_facturas_aprobadas
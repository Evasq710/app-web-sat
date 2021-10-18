class DTE:
    def __init__(self, lugar, dia, mes, year, hora, referencia, nit_emisor, nit_receptor, valor, iva, total):
        self.lugar = lugar
        self.dia = dia
        self.mes = mes
        self.year = year
        self.hora = hora
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.error_referencia_doble = False
        self.error_nit_emisor = False
        self.error_nit_receptor = False
        self.error_iva = False
        self.error_total = False
        self.validar_nit_emisor()
        self.validar_nit_receptor()
    
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
            except:
                self.error_nit_emisor = True
        elif modulo2 == 10:
            if nit_inverso[0] != "K":
                self.error_nit_emisor = True
        else:
            self.error_nit_emisor = True
    
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
            except:
                self.error_nit_receptor = True
        elif modulo2 == 10:
            if nit_inverso[0] != "K":
                self.error_nit_receptor = True
        else:
            self.error_nit_receptor = True

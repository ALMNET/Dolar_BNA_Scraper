import re
from datetime import date, timedelta, datetime
# from openpyxl import Workbook, load_workbook
# from colorama import Fore
# from bs4 import BeautifulSoup
import requests 

##########################################################################################
################################## FUNCIONES AUXILIARES ##################################
##########################################################################################

def extractor_datos(texto):
    """Extrae texto hasta que consigue el primer ; y devuelve el texto extraido.
    Util para separar datos de un texto separado por ;

    :param texto: Texto a verificar
    :type a: str
    :return: Texto extraido
    :rtype: str
    """
    textoExtraido = texto[:texto.find(";")]
    texto = texto[texto.find(";") + 1:]
    return textoExtraido, texto


def remove_html_tags(text):
    """Elimina etiquetas html de un texto.

    :param texto: Texto a filtrar
    :type a: str
    :return: Texto extraido sin etiquetas html
    :rtype: str
    """
    html_pattern = re.compile('<.*?>')
    clean_text = re.sub(html_pattern, '', text)
    return clean_text

##########################################################################################
################################## PARAMETROS INICIALES ##################################
##########################################################################################

urlDatosBNA = "https://www.bna.com.ar/Personas"


##########################################################################################
################################### OBTENCION DE DATOS ###################################
##########################################################################################

result = requests.get(urlDatosBNA)
htmlBase = result.text

fecha_referencia = date.today().strftime('%Y-%m-%d')

# Buscamos posiciones donde se ubican los datos de interes usando texto de referencia "USA"
posicionInicio = htmlBase.find("U.S.A")
posicionFin = htmlBase[posicionInicio:].find("</tr>")

# Filtramos solo datos de interes (viene con etiquetas html) y eliminamos el resto
datosBase = htmlBase[posicionInicio:(posicionInicio + posicionFin)]

# Barremos nuevamente texto que no nos interesa, filtramos USA y arrancamos desde dolar compra
posicionInicio = datosBase.find("<td>")
datosBase = datosBase[posicionInicio:]

# Eliminacion de espacios
datosBase = re.sub(r"\s+", "", datosBase)

# Separacion de datos con comas
datosBase = re.sub(r"</td><td>", ";", datosBase)

# Eliminación de etiquetas html
datosBase = remove_html_tags(datosBase)

# Impresion de datos base
# print(datosBase)

# Segmentacion de datos
dolarCompra, datosBase = extractor_datos(datosBase)
dolarVenta, datosBase = extractor_datos(datosBase)


# Salida de datos
print("Dolar Compra: " + dolarCompra)
print("Dolar Venta: " + dolarVenta)
import re
from datetime import date, timedelta, datetime
import mysql.connector
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

# Conversion de comas a puntos para pasar a flotante
datosBase = re.sub(r",", ".", datosBase)

# Impresion de datos base
# print(datosBase)

# Segmentacion de datos
dolarCompra, datosBase = extractor_datos(datosBase)
dolarVenta, datosBase = extractor_datos(datosBase)

# Conversion a flotante
dolarCompra = float(dolarCompra)
dolarVenta = float(dolarVenta)

# Salida de datos
print("Dolar Compra: " + str(dolarCompra))
print("Dolar Venta: " + str(dolarVenta))

##########################################################################################
################################ INSERTANDO DATOS EN LA DB ###############################
##########################################################################################

# Datos conexion
connection = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="ALMNet-387SQL",
    database="General"
)

# Create a cursor object
cursor = connection.cursor()

# Prepare SQL query to INSERT a record into the table
sql = """
INSERT INTO `General`.Pruebas 
(Fecha_Recepcion, Fecha_Creacion, Origen, Dolar_Venta, Dolar_Compra, Noticia_Relevante1, Noticia_Relevante2, Noticia_Relevante3) 
VALUES (now(), now(), 'Banco Nacion', {dolarVenta}, {dolarCompra}, '', '', '');""".format(dolarVenta = dolarVenta, dolarCompra = dolarCompra)


#values = ("value1", "value2", "value3")


# Execute the SQL query
cursor.execute(sql)

# Commit your changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Data inserted successfully!")
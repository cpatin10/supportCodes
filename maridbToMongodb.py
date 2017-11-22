#!/usr/bin/python
import pymysql
import pymongo
from pymongo import MongoClient
import random
import datetime
from datetime import datetime

"""Parámetros para la configuración de la conexión con MariaDB"""
sqlConfig = {
    'host': '192.168.10.75',
    'port': 3306,
    'user': 'semillero',
    'passwd': 'passw0rd!',
    'db': 'store'
    } 

"""Genera un número aleatorio entre 1 y un valor dado"""
def generarAleatorio(maximo):
    aleatorio = random.randrange(1, maximo)
    return aleatorio

"""Genera una fecha aleatoria para Septiembre del 2013. La fecha es de tipo dat en python"""
def generarFecha():
    dia = generarAleatorio(30)
    """if dia < 10:
        dia = "0" + str(dia)
    fecha = "2013-09-" + str(dia) + "T01:00:00+01:00" """
    fecha = '201309'+str(dia)
    fecha = datetime.strptime(fecha, "%Y%m%d")
    return fecha

"""Calcula un subtotal a partir de un precio y una cantidad dada"""
def calcularSubTotal(precio, cantidad):
    subTotal = precio * cantidad
    return subTotal

"""Cuenta el número de registros dentro de una tabla, para la base de datos MariaDB indicada por el cursor dado"""
def contarRegistros(cursor, tabla):
    query = ("SELECT COUNT(*) FROM " + tabla + ";")
    cursor.execute(query)
    contador = cursor.fetchone()
    return int(contador[0])

"""Escoge un cliente al azar de la tabla customer de la base de datos en MariaDB y retorna su id"""
def seleccionarCliente(cursor, valmax):
    posicion = generarAleatorio(valmax) - 1
    # https://www.w3schools.com/php/php_mysql_select_limit.asp
    query = ("SELECT customer_id FROM customers LIMIT %s, 1;")
    cursor.execute(query, (posicion))
    cliente = cursor.fetchone()
    return cliente[0]

"""Escoge un producto al azar de la tabla products de la base de datos en MariaDB y retorna su id y precio"""
def seleccionarProducto(cursor, valmax):
    posicion = generarAleatorio(valmax) - 1
    # https://www.w3schools.com/php/php_mysql_select_limit.asp
    query = ("SELECT product_id, product_price FROM products LIMIT %s, 1;")
    cursor.execute(query, (posicion))
    producto = cursor.fetchone()
    return producto[0], producto[1]

"""Introduce los datos de la orden (id y fecha) dentro del diccionario dado"""
def datosOrden(jsonDict, ordenId):
    jsonDict["order_id"] = ordenId
    jsonDict["order_date"] = generarFecha()

"""Introduce los datos de un cliente (id) escogido al azar dentro del diccionario dado"""
def datosCustomer(jsonDict, cursor, totClientes):
    customerId = seleccionarCliente(cursor, totClientes)
    jsonDict["customer_id"] = customerId

"""Introduce los datos de cada producto (id, cantidad, precio, subtotal) escogidos aleatoreamente perteneciente a una lista de compras de tamaño aleatorio entre 1 y 5"""
def datosProductos(jsonDict, cursor, totProductos):
    total = generarAleatorio(5)
    products = []
    for i in range(0, total):
        subDict = dict()
        productID, precio = seleccionarProducto(cursor, totProductos)
        cantidad = generarAleatorio(5)
        subDict["product_id"] = productID
        subDict["item_quantity"] = cantidad
        subDict["product_price"] = precio
        subDict["sub_total"] = calcularSubTotal(precio, cantidad)
        products.append(subDict)
    jsonDict["products"] = products

#for debugging purposes 
"""Imprime el contenido de un diccionario dado"""
def printDictionary(dictionary):
    for keys,values in dictionary.items():
        print(keys)
        print(values)

"""Generador de ficheros json, para la creación de una base de datos en MongoDB a partir de una base de datos en MariaDB"""
def main():
    try:
        #Conexión a MariaDB
        sqlConnection = pymysql.connect(**sqlConfig)
        cursor = sqlConnection.cursor()
        #Conexión a MongoDB
        mongoClient = pymongo.MongoClient("192.168.10.75", 27017) 
        mongodb = mongoClient["mongoHadoop"]
        mongodb.authenticate("hadoop", "hadoop.mongo")
        #Cálculo del total de clientes y productos en la base de datos de MariaDB
        totClientes = contarRegistros(cursor, "customers")
        totProductos = contarRegistros(cursor, "products")
        #Creación de los 2000 documentos a ingresar en MongoDB
        for ordenID in range(1, 2000 + 1):
            #Se crea un diccionario para poder crear el documento en MongoDB
            jsonDict = dict()
            #Llenado del diccionario
            datosOrden(jsonDict, ordenID)
            datosCustomer(jsonDict, cursor, totClientes)
            datosProductos(jsonDict, cursor, totProductos)
            #print(jsonDict)            
            #Inserción del diccionario en MongoDB
            mongodb.mobileOrders.insert(jsonDict)
        #Cierre de conexiones
        mongoClient.close()
        cursor.close()
        sqlConnection.close()
    except pymongo.errors.OperationFailure as err:
        print("Pymongo operationFailure: " + err)
    except Exception as err:
        print("Error: " + err)

if __name__ == "__main__":
    main()

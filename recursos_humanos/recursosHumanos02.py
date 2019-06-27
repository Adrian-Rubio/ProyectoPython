# -*- coding: utf-8 -*-

import re

def leerFichero(nombreFichero):
    ficheros = open(nombreFichero, 'rt')
    lineas = ficheros.readlines()
    ficheros.close()
    return lineas

def dniIncorrecto(dni):
    patron = "^[0-9]{8}[a-zA-Z]$"
    return re.match(patron, dni) is None

def nombreApellidoIncorrecto(nombre):
    patron = "^[a-zA-ZÁÉÍÓÚÑáéíóúñ ]+$"
    return re.match(patron, nombre) is None

def obtenerDatos(linea):
    errores = ""

    campos = linea.rstrip().split(":")
    if len(campos) == 4:
        if nombreApellidoIncorrecto(campos[0]):
            errores += "\tEl nombre tiene caracteres no alfabéticos\n"

        if nombreApellidoIncorrecto(campos[1]):
            errores += "\tEl apellido tiene caracteres no alfabéticos\n"

        if dniIncorrecto(campos[2]):
            errores += "\tEl dni no tiene el formato adecuado\n"

        if not campos[3].isdigit():
            errores += "\tEl cuarto campo (edad) tiene que ser entero\n"
        else:
            campos[3] = int(campos[3])
    else:
        errores += "\tTiene que haber exactamente cuatro campos en el registro!\n"

    if len(errores) > 0:
        raise ValueError(errores)
    else:
        return campos

def imprimirRegistros(diccionario):
    print("Datos:")
    for it in diccionario.values():
        print(it[0], it[1], it[2], it[3], sep='\t')
    print()

def printInfo(datos):
    info = "Nombre: {0}, Apellido: {1}, Dni: {2}, Edad: {3}". \
        format(datos[0], datos[1], datos[2], datos[3])
    print(info)

def buscarPersonasConEdad(edad):
    return [ p for p in diccionario.values() if p[3] == edad ]

lineas = leerFichero('datos_mal.txt')

diccionario = {}
for l in lineas:
    try:
        l = l.rstrip()
        datos = obtenerDatos(l)
        dni = datos[2]
        diccionario[dni.upper()] = datos
    except ValueError as errores:
        print("Errores en el registro '{0}':\n{1}".format(l, errores))
imprimirRegistros(diccionario)
from pprint import pprint as pp
pp(diccionario.values())


print("Teclea dni para obtener empleado de la persona")
while True:
    dni = input("dni?: ")
    if dni == '':
        break;

    if dniIncorrecto(dni):
        print("dni no tiene el formato adecuado.")
        continue

    dni = dni.upper()
    if dni in diccionario:
        datos = diccionario[dni]
        printInfo(datos)
    else:
        print("No existe persona con ese dni")
print()




print("Teclea edad para buscar personas con esa edad")
while True:
    print()
    edad = input("edad?: ")
    if edad == '':
        break;
    else:
        try:
            edad = int(edad)
        except ValueError as e:
            print("{0} no es un entero!".format(edad))
            print( e)
            continue

    encontradas = buscarPersonasConEdad(edad)
    if (len(encontradas) == 0):
        print("No hay personas con edad igual a {0}".format(edad))
    else:
        print("Personas con edad igual a {0}:".format(edad))
        for p in encontradas:
            printInfo(p)
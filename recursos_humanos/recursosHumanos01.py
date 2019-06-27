# -*- coding: utf-8 -*-


def leerFichero(nombreFichero):
  ficheros = open(nombreFichero, 'rt')
  lineas = ficheros.readlines()
  ficheros.close()
  return lineas


def obtenerDatos(linea):
  campos = linea.rstrip().split(":")
  campos[3] = int(campos[3])
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

lineas = leerFichero('datos_bien.txt')

diccionario = {}
for l in lineas:
  datos = obtenerDatos(l)
  dni = datos[2]
  diccionario[dni.upper()] = datos

imprimirRegistros(diccionario)


print("Teclea dni para obtener empleado de la persona")
while True:
  dni = input("dni?: ")
  if dni == '':
    break

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

  edad = int(edad)

  encontradas = buscarPersonasConEdad(edad)
  if (len(encontradas) == 0):
    print("No hay personas con edad igual a {0}".format(edad))
  else:
    print("Personas con edad igual a {0}:".format(edad))
    for p in encontradas:
      printInfo(p)
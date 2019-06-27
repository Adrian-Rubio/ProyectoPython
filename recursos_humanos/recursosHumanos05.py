# -*- coding: utf-8 -*-

import re


class DniError(Exception):
  def __init__(self, dni):
    self.__dni = dni

  def __str__(self):
    return "DniError: " + dni


class Empleado:
  def __init__(self, nombre, apellido, dni, edad):
    self.__nombre = nombre
    self.__apellido = apellido
    self.__dni = dni
    self.__edad = edad

  def __str__(self):
    return "Empleado - {} {}, {}, {}".format(
      self.__nombre, self.__apellido, self.__dni, self.__edad)

  def __hash__(self):
    return hash(self.__dni)

  def __eq__(self, other):
    if not isinstance(other, Empleado): return False
    return self.__dni == other.dni()

  def nombre(self):
    return self.__nombre

  def apellido(self):
    return self.__apellido

  def dni(self):
    return self.__dni

  def edad(self):
    return self.__edad


class BaseDatos:
  def __init__(self, fichero, separador=':'):
    self.__fichero = fichero
    self.__separador = separador

  def __dniIncorrecto(self, dni):
    patron = "^[0-9]{8}[a-zA-Z]$"
    return re.match(patron, dni) is None

  def __obtenerEmpleado(self, l):
    def nombreApellidoIncorrecto(nombre):
      patron = "^[a-zA-ZÁÉÍÓÚÑáéíóúñ ]+$"
      return re.match(patron, nombre) is None

    errores = ""

    campos = l.rstrip().split(self.__separador)
    if len(campos) == 4:
      if nombreApellidoIncorrecto(campos[0]):
        errores += "\tEl nombre tiene caracteres no alfabéticos\n"

      if nombreApellidoIncorrecto(campos[1]):
        errores += "\tEl apellido tiene caracteres no alfabéticos\n"

      if self.__dniIncorrecto(campos[2]):
        errores += "\tEl dni no tiene el formato adecuado\n"

      if not campos[3].isdigit():
        errores += "\tEl cuarto campo (edad) tiene que ser entero\n"
      else:
        campos[3] = int( campos[3] )
    else:
      errores += "\tTiene que haber cuatro campos en el registro!\n"

    if len(errores) > 0:
      raise ValueError(errores)
    else:
      return Empleado(campos[0], campos[1], campos[2], campos[3])

  def buscarPorEdad(self, edad):
    return self.buscarEmpleados(lambda emp: edad == emp.edad())

  def buscarPorDni(self, dni):
    empleados = self.buscarEmpleados(lambda emp: dni == emp.dni())
    if len(empleados) == 0:
      raise DniError(dni)
    else:
      assert len(empleados) == 1
      return empleados.pop()

  def buscarEmpleados(self, criterio):
    resultado = []
    with open(self.__fichero) as f:
      for linea in f:
        try:
          empleado = self.__obtenerEmpleado(linea)
          if criterio(empleado):
            resultado.append(empleado)
        except ValueError:
          pass
    return resultado

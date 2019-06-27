# -*- coding: utf-8 -*-

import re


class DniError(Exception):
    def __init__(self, dni):
        self._dni = dni

    def __str__(self):
        return "DniError: " + self._dni


class Empleado:
    def __init__(self, nombre, apellido, dni, edad):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__edad = edad

    def __str__(self):
        return "Empleado - {} {}, {}, {}".format(self.__nombre, self.__apellido, self.__dni, self.__edad)

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


class DniHelper:
    @staticmethod
    def dniIncorrecto(dni):
        patron = "^[0-9]{8}[a-zA-Z]$"
        return re.match(patron, dni) is None


class Cache():
    def __init__(self, max=2):
        self.__max = max
        self.__tamanyo = 0
        self.__cache = []

    def encuentra(self, dni):
        if DniHelper.dniIncorrecto(dni) : raise ValueError("Dni en formato incorrecto: " + dni)

        for emp in self.__cache:
            if emp.dni() == dni:
                return emp
        else:
            return None

    def insertar(self, empleado: Empleado):
        if empleado in self.__cache: return

        if self.__tamanyo < self.__max:
            self.__tamanyo += 1
        else:
            self.__cache.pop(0)
        self.__cache.append(empleado)

    def contenido(self):
        return self.__cache


class BaseDatos():
    def __init__(self, fichero, separador=':', maxCache = 2):
        self.__fichero = fichero
        self.__separador = separador
        self.__cache = Cache(maxCache)


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

            if DniHelper.dniIncorrecto(campos[2]):
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
        empleado = self.__cache.encuentra(dni)
        if empleado == None:
            empleados = self.buscarEmpleados(lambda emp: dni == emp.dni())
            if len(empleados) == 0:
                raise DniError(dni)
            else:
                assert len(empleados) == 1
                empleado = empleados.pop()
                self.__cache.insertar(empleado)
                return empleado
        else:
            return empleado

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

    def cache(self):
        return self.__cache.contenido()

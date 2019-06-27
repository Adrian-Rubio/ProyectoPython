from recursosHumanos04 import BaseDatos, Empleado, DniError


bd = BaseDatos(fichero="datos_bien2.txt", separador="@")
assert bd.size() == 5

bd = BaseDatos(fichero="datos_mal.txt")
assert bd.size() == 6

assert bd.buscarPorDni("51354176G") == Empleado('Vega', 'Aguado', '51354176G', 25)
assert bd.buscarPorDni("89307676B") == Empleado('Lucas', 'Moreno', '89307676B', 4)
try:
    bd.buscarPorDni("99307676B")
    assert False
except DniError:
    pass

e0 = Empleado('Marta', 'Madero', '89307676B', 44)
e1 = Empleado('José', 'Madero', '89307655B', 44)
emp = bd.buscarPorEdad(44)
assert len(emp) == 2

if e0 == emp[0]:
    assert e1 == emp[1]
elif e0 == emp[1]:
    assert e1 == emp[0]
else:
    assert False

assert str((e0)) == "Empleado - Marta Madero, 89307676B, 44"
assert e0.nombre() == "Marta"
assert e0.apellido() == "Madero"
assert e0.dni() == "89307676B"
assert e0.edad() == 44
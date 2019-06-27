from recursosHumanos05 import BaseDatos, Empleado, DniError


bd = BaseDatos(fichero="datos_mal.txt")

assert bd.buscarPorDni("51354176G") == Empleado('Vega', 'Aguado', '51354176G', 25)
assert bd.buscarPorDni("89307676B") == Empleado('Marta', 'Madero', '89307676B', 44)
try:
  bd.buscarPorDni("99307676B")
  assert False
except DniError:
  pass

emp = bd.buscarPorEdad(44)
assert len(emp) == 2

e0 = Empleado('Marta', 'Madero', '89307676B', 44)
e1 = Empleado('José', 'Madero', '89307655B', 44)
if e0 == emp[0]:
  assert e1 == emp[1]
elif e0 == emp[1]:
  assert e1 == emp[0]
else:
  assert False

emps = bd.buscarEmpleados(lambda emp: 'Hugo' == emp.nombre())
assert len(emps) == 1

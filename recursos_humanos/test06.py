from recursosHumanos06 import BaseDatos, Empleado, DniError


bd = BaseDatos("datos_mal.txt")
assert bd.cache() == []

e0 = Empleado('Vega', 'Aguado', '51354176G', 25)
assert bd.buscarPorDni("51354176G") == e0
assert bd.cache() == [ e0 ]

e1 = Empleado('Marta', 'Madero', '89307676B', 44)
assert bd.buscarPorDni("89307676B") == e1
assert bd.cache() ==  [e0, e1 ]

assert bd.buscarPorDni("51354176G") == e0
assert bd.cache() ==  [e0, e1 ]


try:
  bd.buscarPorDni("99997676B")
  assert False
except DniError:
  assert bd.cache() == [e0, e1]


e2 = Empleado('Hugo', 'Lobo', '31440200Y', 50)
assert bd.buscarPorDni("31440200Y")  == e2
assert bd.cache() == [e1, e2]

e3 = Empleado('José', 'Madero', '89307655B', 44)
assert bd.buscarPorDni("89307655B") == e3
assert bd.cache() == [e2, e3]
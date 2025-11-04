from rab import Marca, Aeronave

# Guarda uma matricula, a classe Marca valida a matrícula
planador_marca = Marca("ptppc")

# Realiza consultas
planador = Aeronave(planador_marca)
print(planador.classe)

# A mátricula pode ser dada diretamente como str para a consulta
aviao = Aeronave(Marca("pp-adb"))
outro_aviao = Aeronave(Marca("PPCAH"))
helicoptero = Aeronave("PT-HJB")
print(aviao.fabricante)
print(outro_aviao.fabricante)
print(helicoptero.fabricante)

# Cache é automaticamente utilizado para evitar buscar a mesma aeronaves
print(Aeronave("PPADB").fabricante)

# Não buscar do cache
planador = Aeronave(planador_marca,fromcache=False)
print(str(planador.assentos))

# Não usar o cache e não guardar o resultado consulta no cache
atr = Aeronave("Pratr",usecache=False)
print(atr.operador_nome)
print(atr.operador_cadastro)
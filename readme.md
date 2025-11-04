CARD ID `1633197553057006848`

***[Proposta Original](proposta.md)***

# Registro Aeronáutico Brasileiro

Esta ferramenta faz consultas de informações sobre uma aeronave no registro aeronáutico brasileiro dado sua matrícula.

- **A mátricula precisa ser de uma aeronave registrada no Brasil.**
- **Reservas de marcas não estão inclusas.**
- **A consulta é realizada de forma síncrona.**

## Dependências

Esta ferramenta utiliza o `parsel` para extrair as informações, instale via `pip install parsel`

## Utilização
Apenas o arquivo [`rab.py`](src/rab.py) é necessário
```py
from anac import Marca, Aeronave

# Guarda uma matricula, a classe Marca valida a matrícula
planador_marca = Marca("ptppc")


# Realiza consultas
planador = Aeronave(planador_marca)
print(planador.classe)
```

#### A mátricula pode ser dada diretamente como str para a consulta
```py
aviao = Aeronave(Marca("pp-adb"))
outro_aviao = Aeronave(Marca("PPCAH"))
helicoptero = Aeronave("PT-HJB")
print(aviao.fabricante)
print(outro_aviao.fabricante)
print(helicoptero.fabricante)
```

### Um cache é automaticamente hidratado e utilizado se a aeronave já foi consultada
```py
print(Aeronave("PPADB").fabricante)
```

#### Não buscar do cache
```py
planador = Aeronave(planador_marca,fromcache=False)
print(str(planador.assentos))
```

#### Não usar o cache e não guardar o resultado consulta no cache
```py
atr = Aeronave("Pratr",usecache=False)
print(atr.operador_nome)
print(atr.operador_cadastro)
```

---

> Projeto de finalidade acadêmica associado ao Curso Superior Tecnológico de Inteligência Artificial na FATEC Rio Claro
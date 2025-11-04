import re
from datetime import date
from urllib.request import urlopen
from parsel import Selector

extremidade_rab = "https://aeronaves.anac.gov.br/aeronaves/cons_rab_print.asp?nf="

class Marca:
    class INVALIDA(ValueError):
        pass
    class DESCONHECIDA(LookupError):
        pass
    regex = r'^(?:PP|PR|PS|PT|PU)(?!(?:SOS|XXX|PAN|TTT|VFR|IFR|VMC|IMC)$)[A-PR-Z][A-VXYZ][A-Z]$'
    def __init__(self,mat:str):
        self._reg = str(mat).strip().upper().replace('-','').replace(' ','')
        if not re.match(Marca.regex,self._reg):
            raise Marca.INVALIDA(f'A marca "{self._reg}" não pode ser válida no Brasil.')
    def __str__(self) -> str:
        return self._reg

class Aeronave:
    _cache = {}
    def __init__(self,marca:Marca|str,fromcache=True,usecache=True) -> None:

        if type(marca) == str:
            marca_sanit = Marca(marca)
        elif type(marca) == Marca:
            marca_sanit = marca
        else:
            raise RuntimeError

        cachehit = Aeronave._cache.get(marca_sanit._reg)
        if cachehit!=None and fromcache and usecache:
            self.__dict__.update(cachehit.__dict__)
            return
        
        try:
            resposta = urlopen(f'{extremidade_rab}{marca_sanit}')
        except:
            raise Marca.DESCONHECIDA
        
        if resposta.getcode() != 200:
            raise Marca.DESCONHECIDA
        
        html_relatorio = resposta.read().decode('iso-8859-1')
        
        sel = Selector(html_relatorio)
        
        self.marca                :str   = f'{str(marca_sanit)[:2]}-{str(marca_sanit)[2:]}'
        self.proprietario_nome    :str   = str(sel.xpath("//span[contains(text(), 'Proprietário')]/following-sibling::text()").get()).strip()
        self.proprietario_cadastro:str   = str(sel.xpath("(//span[contains(text(), 'CPF/CGC')]/following-sibling::text())[1]").get()).strip()
        self.operador_nome        :str   = str(sel.xpath("//span[contains(text(), 'Operador')]/following-sibling::text()").get()).strip()
        self.operador_cadastro    :str   = str(sel.xpath("(//span[contains(text(), 'CPF/CGC')]/following-sibling::text())[2]").get()).strip()
        self.fabricante           :str   = str(sel.xpath("//span[contains(text(), 'Fabricante')]/following-sibling::text()").get()).strip()
        self.ano                  :int   = int(str(sel.xpath("//span[contains(text(), 'Ano de Fabricação')]/following-sibling::text()").get()))
        self.modelo               :str   = str(sel.xpath("//span[contains(text(), 'Modelo')]/following-sibling::text()").get()).strip()
        self.numero_de_serie      :str   = str(sel.xpath("//span[contains(text(), 'Número de Série')]/following-sibling::text()").get()).strip()
        self.icao                 :str   = str(sel.xpath("//span[contains(text(), 'Tipo ICAO')]/following-sibling::text()").get()).strip()
        self.habilitacao          :str   = str(sel.xpath("//span[contains(text(), 'Tipo de Habilitação para Pilotos')]/following-sibling::text()").get()).strip()
        self.classe               :str   = str(sel.xpath("//span[contains(text(), 'Classe da Aeronave')]/following-sibling::text()").get()).strip()
        self.peso_maximo          :float = float(str(sel.xpath("//span[contains(text(), 'Peso Máximo de Decolagem')]/following-sibling::text()").get()).split('-')[0])
        self.passageiros          :int   = int(str(sel.xpath("//span[contains(text(), 'Número Máximo de Passageiros')]/following-sibling::text()").get()))
        self.regras_de_voo        :str   = str(sel.xpath("//span[contains(text(), 'Tipo de voo autorizado')]/following-sibling::text()").get()).strip()
        self.assentos             :int   = int(str(sel.xpath("//span[contains(text(), 'Número de Assentos')]/following-sibling::text()").get()))
        self.tripulacao           :int   = self.assentos - self.passageiros
        self.categoria            :str   = str(sel.xpath("//span[contains(text(), 'Categoria de Registro')]/following-sibling::text()").get()).strip()
        self.matricula            :int   = int(str(sel.xpath("//span[contains(text(), 'Número da Matrícula')]/following-sibling::text()").get()))
        self.gravame              :str   = str(sel.xpath("//span[contains(text(), 'Gravame')]/following-sibling::text()").get()).strip()
        self.situacao             :str   = str(sel.xpath("//span[contains(text(), 'Situação de Aeronavegabiidade')]/following-sibling::text()").get()).strip()

        validade_cva = str(sel.xpath("//span[contains(text(), 'Data de Validade do CVA')]/following-sibling::text()").get())
        validade_cva_datas = validade_cva.split('/')

        if len(validade_cva_datas)==3:
            self.validade_cva :date  = date(int(validade_cva_datas[2]),int(validade_cva_datas[1]),int(validade_cva_datas[0]))
        
        if usecache:
            Aeronave._cache[marca_sanit._reg] = self

if __name__ == "__main__":
    cah = Aeronave(Marca("PtCaH"))
    print(cah.assentos)
    print(cah.fabricante)
    ppc = Aeronave(Marca("PT-PPC"))
    print(ppc.fabricante)
    print(ppc.modelo)
    print(ppc.tripulacao)
    print(ppc.regras_de_voo)
    test = Aeronave(Marca("PT-PPC"))
    print(test.marca)
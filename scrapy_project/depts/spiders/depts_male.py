import scrapy


class DeptsMaleSpider(scrapy.Spider):
    name = 'depts_male'
    
    with open("lista_deputados.txt") as file:
       start_urls = [line.strip() for line in file]
    
    def start_request(self):
        request = scrapy.Request(url= self.start_urls, callback= self.parse)
        yield request
        
    def parse(self, response):
        data = dict()
        
        data["nome"] = response.css('.informacoes-deputado li:nth-child(1)::text').get()[1:].upper()
        data["genero"] = "M"
        data["data_nascimento"] = response.css('#identificacao li:nth-child(5)::text').get()[1:]
        data["presenca_plenario"] = response.css('.list-table__item:nth-child(1) .list-table__definition-description:nth-child(2)::text').get()[39:-40]
        data["ausencia_plenario"] = response.css('.list-table__item:nth-child(1) .list-table__definition-description:nth-child(6)::text').get()[39:-40]
        data["ausencia_justificada_plenario"] = response.css('.list-table__item:nth-child(1) .list-table__definition-description:nth-child(4)::text').get()[39:-40]
        data["presenca_comissao"] = response.css('.list-table__item+ .list-table__item .list-table__definition-description:nth-child(2)::text').get()[39:-44]
        data["ausencia_comissao"] = response.css('.list-table__item+ .list-table__item .list-table__definition-description:nth-child(6)::text').get()[39:-44]
        data["ausencia_justificada_comissao"] = response.css('.list-table__item+ .list-table__item .list-table__definition-description:nth-child(4)::text').get()[39:-44]

        gasto_total_par = response.css('.gasto__col:nth-child(1) tr:nth-child(1)  td:nth-child(2)::text').get()
        gasto_total_par = gasto_total_par.replace(".","")
        data["gasto_total_par"] = gasto_total_par.replace(",",".")
        #gasto_mes_par
        for x in response.css('#gastomensalcotaparlamentar > tbody > tr'):
            mes = x.css('td::text').get()
            valor = x.css('td:nth-child(2)::text').get()
            valor = valor.replace(".","")
            valor = valor.replace(",",".")
            key = "gasto_" + mes.lower() + "_par"
            data[key] = valor
        
        gasto_total_gab = response.css('.gasto+ .gasto .gasto__col:nth-child(1) tr:nth-child(1)  td:nth-child(2)::text').get()
        gasto_total_gab = gasto_total_gab.replace(".","")
        data["gasto_total_gab"] = gasto_total_gab.replace(",",".")
        #gasto_mes_gab
        for x in response.css('#gastomensalverbagabinete > tbody > tr'):
            mes = x.css('td::text').get()
            valor = x.css('td:nth-child(2)::text').get()
            valor = valor.replace(".","")
            valor = valor.replace(",",".")
            key = "gasto_" + mes.lower() + "_gab"
            data[key] = valor

        yield data

import re
from urllib import request
from urllib.error import HTTPError
from datetime import date
from bs4 import BeautifulSoup


class Scrap:
    def __init__(self):
        self.selic_address = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'
        self.ibov_address = 'https://br.advfn.com/bolsa-de-valores/bovespa/ibovespa-IBOV/historico'
        self.ipca_address = 'http://www.indiceseindicadores.com.br/ipca/'

    def selic_info(self):
        data = date.today()
        this_year = data.strftime("%Y")
        last_year = str(int(this_year) - 1)

        html_doc = request.urlopen(self.selic_address)
        soup = BeautifulSoup(html_doc, 'html.parser')
        tabela = soup.find_all("td", class_="centralizado")

        #        tabela_dict = {i.string: tabela[x+1].string
        #                       for x, i in enumerate(tabela)
        #                       if last_year in i.string or this_year in i.string}

        tabela_dict = ([i.string, tabela[x + 1].string]
                       for x, i in enumerate(tabela)
                       if last_year in i.string or this_year in i.string)

        return tabela_dict

    def ibov_info(self):
        try:
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                              'AppleWebKit/537.11 (KHTML, like Gecko) '
                              'Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                # 'Accept-Encoding': 'none',
                # 'Accept-Language': 'en-US,en;q=0.8',
                # 'Connection': 'keep-alive'
            }
            req = request.Request(self.ibov_address, headers=hdr)
            html_doc = request.urlopen(req)
            soup = BeautifulSoup(html_doc, 'html.parser')
            tabela_hdr = soup.find_all(
                "th",
                class_=re.compile("Column(1|2|10).?(ColumnLast)? (String|Numeric)"))
            column1 = soup.find_all("td", class_="String Column1")
            column1.insert(0, tabela_hdr[0])
            column2 = soup.find_all("td", class_="Numeric Column2")
            column2.insert(0, tabela_hdr[1])
            column3 = soup.find_all("td", class_="Numeric Column10 ColumnLast")
            column3.insert(0, tabela_hdr[2])

            # head_dict = {col1.string: [col2.string, col3.string]
            #             for col1, col2, col3 in zip(column1, column2, column3)}

            head_dict = ([col1.string, [col2.string, col3.string]]
                         for col1, col2, col3 in zip(column1, column2, column3))

            return head_dict
        except HTTPError:
            return ['http error']

    def ipca_info(self):
        html_doc = request.urlopen(self.ipca_address)
        soup = BeautifulSoup(html_doc, 'html.parser')

        tabela_bd = soup.find("tbody")

        ano = re.compile(r'<strong>\b(?P<ano>[0-9]{4})\b</strong>')
        get_ano = re.findall(ano, str(tabela_bd))

        # taxas = re.compile(r'<(strong|b)>\b(?P<indice>[0-9]{,2},[0-9]{2})\b</(strong|b)>')
        taxas = re.compile(
            r'<td style="text-align: right; width: [0-9.]{3,}px; height: [0-9.]{2,}px;">'
            r'(<span style="font-size: 10pt;">)?(<(strong|b)>)?\b(?P<indice>[0-9]{,2},[0-9]{2})\b'
            r'(</(strong|b)>)?(</span>)?</td>')

        get_tx = re.findall(taxas, str(tabela_bd))
        get_tx = [i[3] for i in get_tx]
        # get_tx = [i for i in get_tx if float(i) > 0.85]

        # tx_ano_dict = {ano: tx for ano, tx in zip(get_ano[:10], get_tx[:10])}
        tx_ano_dict = ([ano, tx] for ano, tx in zip(get_ano[:10], get_tx[:10]))
        # print(get_ano[:10])
        # print(get_tx[:10])

        return tx_ano_dict

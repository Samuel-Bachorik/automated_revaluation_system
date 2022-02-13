from get_prices import Price_Scraper

price_scraper = Price_Scraper()

class Process:
    def __init__(self):
        self.remove_trash           = price_scraper.remove_trash
        self.get_price_heureka      = price_scraper.get_price_heureka
        self.get_price_alza         = price_scraper.get_price_alza
        self.get_price_gigastore    = price_scraper.get_price_gigastore
        self.get_price_datacomp     = price_scraper.get_price_datacomp
        self.get_price_axdata       = price_scraper.get_price_axdata
        self.get_price_tvojpc       = price_scraper.get_price_tvojpc
        self.get_price_zdomu        = price_scraper.get_price_zdomu
        self.get_price_prva         = price_scraper.get_price_prva
        self.get_price_dmcomp       = price_scraper.get_price_dmcomp
        self.get_price_extremecomp  = price_scraper.get_price_extremecomp
        self.get_price_hejsk        = price_scraper.get_price_hejsk
        self.get_price_andreashop   = price_scraper.get_price_andreashop
        self.get_price_mobilonline  = price_scraper.get_price_mobilonline
        self.get_price_mobilecare   = price_scraper.get_price_mobilecare
        self.get_price_danimani     = price_scraper.get_price_danimani
        self.get_price_mobilpc      = price_scraper.get_price_mobilpc
        self.get_price_lacnenakupy  = price_scraper.get_price_lacnenakupy
        self.get_price_datart       = price_scraper.get_price_datart
        self.get_price_pricemarket  = price_scraper.get_price_pricemarket

    def process(self,sheet, start_stop):
        errors = []
        supplier_database = ["gigastore", "datacomp", "axdata", "tvojpc", "zdomu", "prva", "dmcomp", "extremepcshop", "hej", "andreashop", "mobilonline",
                             "mobilecare", "danimani", "mobilpc", "lacne-nakupy", "datart", "pricemarket"]

        supplier_database_f = [self.get_price_gigastore, self.get_price_datacomp, self.get_price_axdata, self.get_price_tvojpc,
                               self.get_price_zdomu, self.get_price_prva, self.get_price_dmcomp, self.get_price_extremecomp, self.get_price_hejsk,
                               self.get_price_andreashop, self.get_price_mobilonline, self.get_price_mobilecare, self.get_price_danimani, self.get_price_mobilpc,
                               self.get_price_lacnenakupy, self.get_price_datart, self.get_price_pricemarket]


        for i in range(start_stop[0], start_stop[1]):
            margin_in_percent = 2.7

            supplier_price_err = False
            product_margin_err = False
            lowest_price_err = False

            for j in range(len(supplier_database)):
                if supplier_database[j] in sheet[i][1]:
                    price_supplier = supplier_database_f[j](sheet[i][1])
                    break

            price_heureka = self.get_price_heureka(sheet[i][2])
            price_alza = float(sheet[i][0])

            if price_supplier == "UNAVAILABLE":
                errors.append("\033[1m" + '\033[91m' + "Product " + str(i + 2) + " is unavailable" + "\033[0m")

                continue

            if price_heureka == False or price_supplier == False :
                errors.append("\033[1m" + '\033[91m' + "Product " + str(
                    i + 2) + " dissapeared from supplier database" + "\033[0m")

                continue

            price_supplier = self.remove_trash(price_supplier)

            #price_heureka = self.remove_trash(price_heureka)
            #price_alza = self.remove_trash(price_alza)

            if price_alza < price_supplier:
                supplier_price_err = True

            #if price_heureka < price_alza:
             #   lowest_price_err = True

            if (abs(price_alza - price_supplier) / price_supplier) * 100.0 < margin_in_percent:
                product_margin_err = True

            error = "\033[1m" + '\033[91m' + "At product " + str(i + 2) + " - " + "\033[0m"

            if supplier_price_err: error += " Price of supplier is higher ||| "
            #if lowest_price_err: error += " Lower price exist ||| "
            if product_margin_err: error += " Margin is low"

            if supplier_price_err or lowest_price_err or product_margin_err:
                errors.append(error)

        return errors
        
        
        import requests
from bs4 import BeautifulSoup


class Price_Scraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

    def get_price_alza(self, url):

        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("span", {"class": "price_withVat"}).get_text()

        return price

    def get_price_heureka(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            price = r.text.split("\"minPrice\":")[1].split(",")[0]

        except:
            return False

        return price

    """ DODAVATELIA """

    def get_price_gigastore(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("span", {"id": "product-detail-price-value"}).get_text()

            if "," in price and "." in price:
                price = price.replace(',', '')

        except:
            return False

        return price

    def get_price_prva(self, url):
        try:
            r = requests.get(url, headers= self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("span", {"class": "price price-default"}).get_text()

        except:
            return False

        try:
            s = soup.find("a", {"class": "link-spedition-days"}).get_text()

            "(Nie je skladom)"
            "Na objednávku"

            if "Do 24 hodín" in s or "Do 48 hodín" in s or "Do 72 hodín" in s:
                return price

            else:
                return "UNAVAILABLE"

        except:
            return False

    def get_price_tvojpc(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("span", {"class": "woocommerce-Price-amount amount"}).get_text()

        except:
            return False

        try:
            soup.find("p", {"class": "stock out-of-stock"}).get_text()

            return "UNAVAILABLE"

        except:
            return price

    def get_price_axdata(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            price = soup.find("span", {"itemprop": "price"}).get_text()

        except:
            return False

        try:
            soup.find("span", {"class": "product-available"}).get_text()

        except:
            return "UNAVAILABLE"

        return price

    def get_price_datacomp(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "prc wvat abs"}).get_text()

        except:
            return False

        try:
            soup.find("span", {"class": "avail_ico avail_ok"}).get_text()

        except:
            return "UNAVAILABLE"

        return price.replace('Â', '').replace('', '').replace('â', '').replace('¬', '').replace(' ', '')

    def get_price_dmcomp(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("strong", {"class": "price sub-left-position"}).get_text()

        except:
            return False

        try:
            s = soup.find("span", {"class": "strong"}).get_text().replace('Â', '').replace('', '').replace('â', '').replace('¬', '').replace(' ', '').replace('€', '').replace(' ', '').replace(' ','').replace(',', '.')

            if "Vypredané" in s:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_zdomu(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"itemprop": "price"}).get_text()

        except:
            return False

        try:

            x = \
                r_text.split("<span class=\"control-label\">Kód: </span>")[0].split(
                    "<div class=\"product-information\">")[
                    1].split("TEXT")

            if "nie je skladom" in x:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_extremecomp(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"class": "cenabezdph"}).get_text().replace('Â', '').replace('', '').replace('â','').replace('¬', '').replace(' ', '').replace('€', '').replace(' ', '').replace(' ', '').replace(',', '.').replace("bezDPH", "")
            price = float(price) * 1.2
            price = str(price)

        except:
            return False

        try:
            soup.find("p", {"class": "skladom"}).get_text()

        except:
            return "UNAVAILABLE"

        return price

    def get_price_hejsk(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"id": "real_price"}).get_text()
        except:
            return False

        try:
            soup.find("span", {"class": "not-available"}).get_text()

            return "UNAVAILABLE"

        except:
            try:
                soup.find("span", {"class": "available supplier"}).get_text()
                return "UNAVAILABLE"

            except:
                try:
                    soup.find("span", {"class": "date-available"}).get_text()
                    return "UNAVAILABLE"

                except:
                    return price

    def get_price_andreashop(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "value"}).get_text()

        except:
            return False

        try:
            soup.find("div", {"class": "dostupnost stav-1 tooltip tooltip"}).get_text()


        except:
            return "UNAVAILABLE"

        return price

    def get_price_mobilonline(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "ProductNormal_page_price__3djvm"})
            children = price.findChildren()
            price = children[1].text


        except:
            return False

        try:
            soup.find("div", {"class": "Availability_available__1BM2E"}).get_text()
            return price

        except:
            return "UNAVAILABLE"


    def get_price_mobilecare(self, url):
        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"class": "woocommerce-Price-amount amount"}).get_text()

            if "," in price and "." in price:
                price = price.replace(',', '')

        except:
            return False

        try:
            soup.find("button", {"name": "add-to-cart"}).get_text()

        except:
            return "UNAVAILABLE"

        return price


    def get_price_danimani(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = float((soup.find("li", {"class": "taxprice"}, "li").get_text().replace('€', '').replace(' ','').replace(' ', '').replace(',', '.')).replace("BezDPH:", "")) * 1.2
            price = str(price)

        except:
            return False

        try:
            soup.find("li", {"class": "stav-skladu vypredane"}).get_text()
            return "UNAVAILABLE"

        except:

            return price

    def get_price_mobilpc(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            id = url.split("p-")[1].split(".xhtml")[0]
            price = soup.find("span", {"id": "PriceWithVAT" + id}).get_text()

        except:
            return False

        try:
            soup.find("div", {"data-txt": "Vo vlastnom sklade"}).get_text()

        except:

            return "UNAVAILABLE"

        return price

    def get_price_lacnenakupy(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")

            price = soup.find(class_="price price-primary text-danger").get_text()

        except:
            return False

        try:
            a = soup.find("div", {"id": "productStatus"}).get_text()

            if "Skladom" in a:
                return price

            if "Na objednávku" or "Momentálne nedostupné" or "Dočasne vypredané" or "Nedostupné" or "dodávateľa" in a:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_datart(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")

            price = soup.find("div", {"class": "price-wrap"}).get_text()

        except:
            return False

        try:
            a = soup.find("span", {"class": "product-availability-state"}).get_text()
            if "Posledný kus k odoslaniu" in a or "Ihneď k odoslaniu?" in a:
                return price

            if "U dodávateľa" in a or "Očakávame do" in a or "Nie je skladom" in a or "K vyzdvihnutiu na predajni" in a:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_pricemarket(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"itemprop": "price"}).get_text()

        except:
            return False

        try:
            s = soup.find("span", {"id": "product-availability"}).get_text().replace(' ', '').replace(' ', '').replace(
                ',', '.').replace("", "").replace("", "")

            "Dodanie1-5pracovnýchdní"
            "Ľutujeme.aletentoproduktjemomentálnevypredaný.Kontaktujtenásprosímohľadomdostupnostitohtoproduktu."
            "Naobjednávku."

            if "Dodanie" in s:
                return price

            if "Ľutujeme" in s or "vypredaný" in s or "Naobjednávku" in s or "Nedostupné":
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def remove_trash(self, price):
        number = float(price.replace('€', '').replace(' ', '').replace(' ', '').replace(',', '.'))

        return number

from __future__ import print_function
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def get_sheet(ID, JSON):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = JSON

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,scopes = SCOPES
    )

    SAMPLE_SPREADSHEET_ID = ID
    SAMPLE_RANGE_NAME = 'Linky!A2:C511'

    creds = credentials

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            pass

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('Žiadne dáta.')
            return


    except HttpError as err:
        print(err)
    print("Google sheets ready...")


    return values
from google_sheets import get_sheet
import time
import math
from run_workers import _run_workers

def print_errors(errors):
    for i in errors:
        for x in i:
            print(x)

if __name__ == '__main__':

    ID = '114oIOb8Ml45ET3aziBiaBlOl0TpbtLMT8-fkj6xGTTM'
    JSON_KLUC = "eshop-sheet-c38c9c8a59ed.json"
    sheets = get_sheet(ID, JSON_KLUC)
    processes_count = 30
    odd_residue = len(sheets) - (processes_count * (math.floor(len(sheets) / processes_count)))
    start_time = time.time()

    if odd_residue != 0:
        print("Processing an odd number of products...")
        sheets0 = sheets[0:len(sheets)-odd_residue]

        errors =_run_workers(processes_count=processes_count, sheets=sheets0)

        errors0 = _run_workers(processes_count=1, sheets=sheets, odd_residue= odd_residue)

        for k in errors0:
            errors.append(k)

        print_errors(errors)

        print("\n\n--This task took %s seconds--" % (time.time() - start_time))

    else:
        print("Processing an even number of products")
        errors = _run_workers(processes_count=processes_count, sheets=sheets)

        print_errors(errors)
        print("\n\n--This task took %s seconds--" % (time.time() - start_time)),
        ,
        
        
        
        try:
            soup.find("span", {"class": "product-available"}).get_text()

        except:
            return "UNAVAILABLE"

        return price

    def get_price_datacomp(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "prc wvat abs"}).get_text()

        except:
            return False

        try:
            soup.find("span", {"class": "avail_ico avail_ok"}).get_text()

        except:
            return "UNAVAILABLE"

        return price.replace('Â', '').replace('', '').replace('â', '').replace('¬', '').replace(' ', '')

    def get_price_dmcomp(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("strong", {"class": "price sub-left-position"}).get_text()

        except:
            return False

        try:
            s = soup.find("span", {"class": "strong"}).get_text().replace('Â', '').replace('', '').replace('â', '').replace('¬', '').replace(' ', '').replace('€', '').replace(' ', '').replace(' ','').replace(',', '.')

            if "Vypredané" in s:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_zdomu(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"itemprop": "price"}).get_text()

        except:
            return False

        try:

            x = \
                r_text.split("<span class=\"control-label\">Kód: </span>")[0].split(
                    "<div class=\"product-information\">")[
                    1].split("TEXT")

            if "nie je skladom" in x:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_extremecomp(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"class": "cenabezdph"}).get_text().replace('Â', '').replace('', '').replace('â','').replace('¬', '').replace(' ', '').replace('€', '').replace(' ', '').replace(' ', '').replace(',', '.').replace("bezDPH", "")
            price = float(price) * 1.2
            price = str(price)

        except:
            return False

        try:
            soup.find("p", {"class": "skladom"}).get_text()

        except:
            return "UNAVAILABLE"

        return price

    def get_price_hejsk(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"id": "real_price"}).get_text()
        except:
            return False

        try:
            soup.find("span", {"class": "not-available"}).get_text()

            return "UNAVAILABLE"

        except:
            try:
                soup.find("span", {"class": "available supplier"}).get_text()
                return "UNAVAILABLE"

            except:
                try:
                    soup.find("span", {"class": "date-available"}).get_text()
                    return "UNAVAILABLE"

                except:
                    return price

    def get_price_andreashop(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "value"}).get_text()

        except:
            return False

        try:
            soup.find("div", {"class": "dostupnost stav-1 tooltip tooltip"}).get_text()


        except:
            return "UNAVAILABLE"

        return price

    def get_price_mobilonline(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("div", {"class": "ProductNormal_page_price__3djvm"})
            children = price.findChildren()
            price = children[1].text


        except:
            return False

        try:
            soup.find("div", {"class": "Availability_available__1BM2E"}).get_text()
            return price

        except:
            return "UNAVAILABLE"


    def get_price_mobilecare(self, url):
        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"class": "woocommerce-Price-amount amount"}).get_text()

            if "," in price and "." in price:
                price = price.replace(',', '')

        except:
            return False

        try:
            soup.find("button", {"name": "add-to-cart"}).get_text()

        except:
            return "UNAVAILABLE"

        return price


    def get_price_danimani(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text

            soup = BeautifulSoup(r_text, "html.parser")
            price = float((soup.find("li", {"class": "taxprice"}, "li").get_text().replace('€', '').replace(' ','').replace(' ', '').replace(',', '.')).replace("BezDPH:", "")) * 1.2
            price = str(price)

        except:
            return False

        try:
            soup.find("li", {"class": "stav-skladu vypredane"}).get_text()
            return "UNAVAILABLE"

        except:

            return price

    def get_price_mobilpc(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            id = url.split("p-")[1].split(".xhtml")[0]
            price = soup.find("span", {"id": "PriceWithVAT" + id}).get_text()

        except:
            return False

        try:
            soup.find("div", {"data-txt": "Vo vlastnom sklade"}).get_text()

        except:

            return "UNAVAILABLE"

        return price

    def get_price_lacnenakupy(self, url):

        try:
            r = requests.get(url, headers=self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")

            price = soup.find(class_="price price-primary text-danger").get_text()

        except:
            return False

        try:
            a = soup.find("div", {"id": "productStatus"}).get_text()

            if "Skladom" in a:
                return price

            if "Na objednávku" or "Momentálne nedostupné" or "Dočasne vypredané" or "Nedostupné" or "dodávateľa" in a:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_datart(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")

            price = soup.find("div", {"class": "price-wrap"}).get_text()

        except:
            return False

        try:
            a = soup.find("span", {"class": "product-availability-state"}).get_text()
            if "Posledný kus k odoslaniu" in a or "Ihneď k odoslaniu?" in a:
                return price

            if "U dodávateľa" in a or "Očakávame do" in a or "Nie je skladom" in a or "K vyzdvihnutiu na predajni" in a:
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def get_price_pricemarket(self, url):

        try:
            r = requests.get(url, headers= self.headers)
            r_text = r.text
            soup = BeautifulSoup(r_text, "html.parser")
            price = soup.find("span", {"itemprop": "price"}).get_text()

        except:
            return False

        try:
            s = soup.find("span", {"id": "product-availability"}).get_text().replace(' ', '').replace(' ', '').replace(
                ',', '.').replace("", "").replace("", "")

            "Dodanie1-5pracovnýchdní"
            "Ľutujeme.aletentoproduktjemomentálnevypredaný.Kontaktujtenásprosímohľadomdostupnostitohtoproduktu."
            "Naobjednávku."

            if "Dodanie" in s:
                return price

            if "Ľutujeme" in s or "vypredaný" in s or "Naobjednávku" in s or "Nedostupné":
                return "UNAVAILABLE"

        except:
            return "UNAVAILABLE"

        return price

    def remove_trash(self, price):
        number = float(price.replace('€', '').replace(' ', '').replace(' ', '').replace(',', '.'))

        return number

from __future__ import print_function
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def get_sheet(ID, JSON):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = JSON

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,scopes = SCOPES
    )

    SAMPLE_SPREADSHEET_ID = ID
    SAMPLE_RANGE_NAME = 'Linky!A2:C511'

    creds = credentials

    if not creds or not creds.valid:

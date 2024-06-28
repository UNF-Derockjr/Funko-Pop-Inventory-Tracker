from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import random
import requests
import json
import xml.etree.ElementTree as ET

colorama_init()
colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]


APP_ID = 'DerrickK-FunkoPop-SBX-54d5919c2-c227714c'

def get_sold_items(search_term, category_id, condition_id, entries_per_page):
    url = 'https://svcs.sandbox.ebay.com/services/search/FindingService/v1'
    params = {
        'OPERATION-NAME': 'findCompletedItems',
        'SERVICE-VERSION': '1.7.0',
        'SECURITY-APPNAME': APP_ID,
        'RESPONSE-DATA-FORMAT': 'XML',
        'REST-PAYLOAD': '',
        'keywords': search_term,
        'categoryId': category_id,
        'itemFilter(0).name': 'Condition',
        'itemFilter(0).value': condition_id,
        'itemFilter(1).name': 'FreeShippingOnly',
        'itemFilter(1).value': 'true',
        'itemFilter(2).name': 'SoldItemsOnly',
        'itemFilter(2).value': 'true',
        'sortOrder': 'PricePlusShippingLowest',
        'paginationInput.entriesPerPage': entries_per_page,
        'paginationInput.pageNumber': 1
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.findall('.//{http://www.ebay.com/marketplace/search/v1/services}item'):
            title = item.find('{http://www.ebay.com/marketplace/search/v1/services}title').text
            current_price = item.find('.//{http://www.ebay.com/marketplace/search/v1/services}currentPrice').text
            print(f"Item: {title}, Sold Price: ${current_price}")
    else:
        print(f"Error: {response.status_code}, {response.text}")



class FunkoPop:
  def __init__(self, name, number):
    self.name = name
    self.number = number

funkoPops = []#[FunkoPop("Asta", 1)]
def InputFunkoPop():
    name = input("Funko Pop Name: ")
    number = input("Funko Pop Number: ")
    pop = FunkoPop(name, number)
    funkoPops.append(pop)
    prevail = input("Continue? y/n")
    match prevail:
        case "y" | "Y":
            InputFunkoPop()
        case "n" | "N":
            ShowMenu()
        case _:
            ShowMenu()

def ShowAllFunkoPops():
    print(f'{"Name":<15} {"Number":<10}')
    for pop in funkoPops:
        color = random.choice(colors)
        print(color + f"{pop.name:<15} {pop.number:10}")
    print(Style.RESET_ALL)
    prevail = input("Back to menu? y")
    match prevail:
        case "y" | "Y":
            ShowMenu()

def ShowMenu():
    print("\033[2J\033[H", end="", flush=True)
    print("1. Enter Funko Pop", end="\n\r")
    print("2. Show All Funko Pops", end="\n\r")
    print("0. Exit", end="\n\r")
    option = input("Option: ")
    print("\033[2J\033[H", end="", flush=True)
    match option:
        case "0":
            exit()
        case "1":
            InputFunkoPop()
        case "2":
            ShowAllFunkoPops()
        case "3":
            get_sold_items("batman", "88988", "1000", 2)
        case _:
            ShowMenu()

ShowMenu()
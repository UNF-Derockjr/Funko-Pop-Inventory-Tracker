from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import random

colorama_init()
colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]

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
        case _:
            ShowMenu()

ShowMenu()
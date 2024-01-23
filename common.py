from colorama import Fore, Style, init


def b(text: str):
    return Fore.BLUE + text + Style.RESET_ALL
def g(text: str):
    return Fore.GREEN + text + Style.RESET_ALL
def p(text: str):
    return Fore.MAGENTA + text + Style.RESET_ALL
def o(text: str):
    return Fore.ORANGE + text + Style.RESET_ALL
def c(text: str):
    return Fore.CYAN + text + Style.RESET_ALL
def y(text: str):
    return Fore.YELLOW + text + Style.RESET_ALL


def pocketcalc(hour:str):
    
    match hour:
        case "00" | "01" | "02" | "03" | "04" | "22" | "23":
            return "night"
        case "05" | "06" | "07" | "08" | "09" | "10" | "11":
            return "morning"
        case "12" | "13" | "14" | "15" | "16":
            return "day"
        case "17" | "18" | "19" | "20" | "21":
            return "evening"
        case _:
            return "campsite"

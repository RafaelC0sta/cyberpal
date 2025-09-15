import os
import time
from modules.teste import testar 
from modules.Fscanner.filescanner import filescan

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(""" ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗  █████╗ ██╗     
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██║     
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██████╔╝███████║██║     
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═══╝ ██╔══██║██║     
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║     ██║  ██║███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝\n""")
        
        print("Welcome to Cyberpal\n[1] - FScanner\n[2] - Logparser\n[0] - Sair\n")
        op = int(input("Choose the option: "))

        match(op):
            case 1:
              path = str(input("Insert the file path: "))
              filescan(path)
              time.sleep(10)
            case 2:
                #logparser
                pass 

            case 0:
                print("Thanks for using Cyberpal")
                break

            case _:
                print("Invalid Option")


if __name__ == "__main__":
    main()

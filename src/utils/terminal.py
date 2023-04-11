RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
YELLOW = "\033[33m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
class CustomPrint:
    @classmethod
    def error(cls,error, message=''):
        print(f'{RED} {error} {RESET} {message}')
    
    @classmethod
    def success(cls,success, message=''):
        print(f'{GREEN} {success} {RESET} {message}')
    
    @classmethod
    def warning(self,warning,message=''):
        print(f'{YELLOW} {warning} {RESET} {message}')
    @classmethod
    def clear_terminal(cls):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

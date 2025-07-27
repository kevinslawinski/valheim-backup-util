import os
import time

from services.config_service import ConfigService
from services.file_service import FileService

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_header():
    title = 'Valheim Backup Utility'
    border = '-' * len(title)
    print(f"{border}\n{title}\n{border}")
    
def menu_options():
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Read current config')
    print('(4) Regenerate config')

def prompt_for_choice():
    choice = input('Choose an option (1-4, 0 to exit): ')
    return choice

def print_config():
    config = ConfigService().load_config()
    print('\nCurrent configuration:\n')
    print(f'  World Name: {config.get("world_file_name")}')
    print(f'  Valheim Save Location: {config.get("local_path")}')
    print(f'  Repo Path: {config.get("repo_path")}')
    
def prompt_new_config():
    print('\nNew configuration:\n')
    world_file_name = input('  Name of the Valheim world: ')
    local_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')
    repo_path = input('  Path to Valheim remote repository: ')
    config = {
      'world_file_name': world_file_name,
      'local_path': local_path,
      'repo_path': repo_path
    }
    ConfigService().save_config(config)
    return config

def run():
    while True:
        menu_header()
        print('Loading config file...')
        config_service = ConfigService()
        config_service.load_config()
        time.sleep(1)
        clear_screen()
        menu_header()
        menu_options()

        choice = prompt_for_choice()
        
        if choice == '1':
            FileService.sync_files('upload')
        elif choice == '2':
            FileService.sync_files('download')
        elif choice == '3':
            print_config()
            input('\nPress Enter to return to the main menu...')
            clear_screen()
        elif choice == '4':
            prompt_new_config()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Not an option. Try again.')
        time.sleep(0.5)
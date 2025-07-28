import os
import time

from services.config_service import ConfigService
from services.file_service import FileService

def run():
    while True:
        menu_header()
        
        get_config()
        time.sleep(1)
        
        # Display main menu
        clear_screen()
        menu_header()
        menu_options()

        choice = prompt_menu_choice()
        if choice == '1':
            confirm = input(f'END of session upload? Confirm: (y/n) ')
            if confirm.lower() == 'y':
                FileService.sync_files('upload')
            else:
                print('Nothing uploaded.')
        elif choice == '2':
            confirm = input(f'START of session download? Confirm: (y/n) ')
            if confirm.lower() == 'y':
                FileService.sync_files('download')
            else:
                print('Nothing downloaded.')
        elif choice == '3':
            print_config()
        elif choice == '4':
            prompt_new_config()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Not an option. Try again.')
        
        input('\nPress Enter to continue...')
        clear_screen()
        time.sleep(0.5)

def menu_header():
    title = 'Valheim Backup Utility'
    border = '-' * len(title)
    print(f"{border}\n{title}\n{border}")
    
def menu_options():
    print('  (1) Upload world files to git repository')
    print('  (2) Download world files from git repository')
    print('  (3) Read current config')
    print('  (4) Regenerate config')

def get_config():
    print('Loading config file...')
    try:
        return ConfigService().get()
    except PermissionError:
        print('You\'re on your own with this one...')
        return None
    except Exception:
        print('Generating new config file...')
        return prompt_new_config()

def print_config():
    config = get_config()
    print(f"""Current configuration:
          
        World Name: {config.get("world_file_name")}
        Valheim Save Location: {config.get("local_path")}
        Repo Path: {config.get("repo_path")}""")
    
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
    ConfigService().save(config)
    print('\nConfiguration saved successfully!')
    return config

def prompt_menu_choice():
    choice = input('Choose an option (1-4, 0 to exit): ')
    return choice

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

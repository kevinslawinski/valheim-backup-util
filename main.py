import json
import os
import shutil
import time

# file name of user configuration
USER_CONFIG = 'config.json'

class ConfigManager: 
  @staticmethod
  def save_config(config):
    with open(USER_CONFIG, 'w') as config_file:
      json.dump(config, config_file, indent=2)

  @staticmethod
  def print_config(config):
    print('\nCurrent configuration:\n')
    print(f'  World Name: {config.get("world_file_name")}')
    print(f'  Valheim Save Location: {config.get("local_path")}')
    print(f'  Repo Path: {config.get("repo_path")}')
    
  @staticmethod
  def generate_config():
    print('\nNew configuration:\n')
    world_file_name = input('  Name of the Valheim world: ')
    local_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')
    repo_path = input('  Path to Valiheim remote repository: ')
    config = {
      'world_file_name': world_file_name,
      'local_path': local_path,
      'repo_path': repo_path
    }
    ConfigManager.save_config(config)
    return config

  @staticmethod
  def load_config():
    print('Loading config file...')
    if not os.path.exists(USER_CONFIG):
      print('Config file not found.')
      return ConfigManager.generate_config()
    with open(USER_CONFIG, 'r') as config:
      return json.load(config)

def copy_files(src, dst, files):
  for file in files:
    src_file = os.path.join(src, file)
    dst_file = os.path.join(dst, file)
    try:
      shutil.copy2(src_file, dst_file)
      print(f'Copied file: {file}')
    except FileNotFoundError:
      print(f'File not found: {src_file}')
    except Exception as e:
      print(f'Error copying file {src_file}: {e}')

def sync_files(action):
  config = load_config()
  world_file = config.get('world_file_name')
  local_path = config.get('local_path')
  repo_path = config.get('repo_path')
  files = [f'{world_file}.db', f'{world_file}.fwl']
  if action == 'upload':
    copy_files(local_path, repo_path, files)
  elif action == 'download':
    copy_files(repo_path, local_path, files)
  print('Navigating to main menu...')

def upload_files():
  sync_files('upload')

def download_files():
  sync_files('download')

def main_menu():
  while True:
    print('\n\n----------------------')
    print('Valheim Backup Utility')
    print('----------------------')
    config = load_config()
    time.sleep(0.7)
    print('\n----------------------')
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Read current config')
    print('(4) Regenerate config')
    
    choice = input('Choose an option (1-3, 0 to exit): ')
    
    if choice == '1':
      upload_files()
    elif choice == '2':
      download_files()
    elif choice == '3':
      print_config(config)
    elif choice == '4':
      generate_config()
    elif choice == '0':
      print('Goodbye!')
      break
    else:
      print('Not an option. Try again.')
    time.sleep(2)

if __name__ == '__main__':
  main_menu()
    
# os.system('git pull')
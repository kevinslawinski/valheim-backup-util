import json
import os
import shutil
import time

# file name of user configuration
USER_CONFIG = 'config.json'
 
def save_config(config):
  with open(USER_CONFIG, 'w') as config_file:
    json.dump(config, config_file, indent=2)
    
def generate_config():
  print('Generating new config...\n')
  world_file_name = input('Name of the Valheim world: ')
  local_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')
  repo_path = input('Local path to Valiheim remote repository: ')
  config = {
    'world_file_name': world_file_name,
    'local_path': local_path,
    'repo_path': repo_path
  }
  save_config(config)
  return config

def load_config(USER_CONFIG):
  print('Loading config file...')
  if not os.path.exists(USER_CONFIG):
    print('Config file not found')
    return generate_config()
  with open(USER_CONFIG, 'r') as config:
    print('Config file loaded successfully. Navigating to main menu...')
    return json.load(config)

def upload_files():
  with open(USER_CONFIG, 'r') as c:
    config = json.load(c)
    world_file = config.get('world_file_name')
    local_path = config.get('local_path')
    repo_path = config.get('repo_path')
    for item in os.listdir(local_path):
      if world_file in item:
        db_file = f'{world_file}.db'
        fwl_file = f'{world_file}.fwl'
        shutil.copy2(os.path.join(local_path, db_file), os.path.join(repo_path, db_file))
        shutil.copy2(os.path.join(local_path, fwl_file), os.path.join(repo_path, fwl_file))
        return True
      else:
        print(f'Could not find .db or .fwl file matching specified world name "{world_file}".')

def download_files():
  with open(USER_CONFIG, 'r') as c:
    config = json.load(c)
    world_file = config.get('world_file_name')
    local_path = config.get('local_path')
    repo_path = config.get('repo_path')
    for item in os.listdir(repo_path):
      if world_file in item:
        db_file = f'{world_file}.db'
        fwl_file = f'{world_file}.fwl'
        shutil.copy2(os.path.join(repo_path, db_file), os.path.join(local_path, db_file))
        shutil.copy2(os.path.join(repo_path, fwl_file), os.path.join(local_path, fwl_file))
        print('World files downloaded successfully. Navigating to main menu...')
        return True
      else:
        print(f'Could not find .db or .fwl file matching specified world name "{world_file}".')

def main():
  while True:
    print('\n\n----------------------')
    print('Valheim Backup Utility')
    print('----------------------')
    load_config(USER_CONFIG)
    time.sleep(2)
    print('\n----------------------')
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Regenerate config')
    
    choice = input('Choose an option (1-3, 0 to exit): ')
    
    if choice == '1':
      upload_files()
      time.sleep(2)
    elif choice == '2':
      download_files()
      time.sleep(2)
    elif choice == '3':
      generate_config()
      time.sleep(2)
    elif choice == '0':
      print('Goodbye!')
      break
    else:
      print('Not an option. Try again.')

main()
    
# os.system('git pull')
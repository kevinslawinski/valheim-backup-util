import json
import os
import shutil


USER_CONFIG = 'config.json'

def load_config(USER_CONFIG):
  if not os.path.exists(USER_CONFIG):
    print('Config file not found')
    return None
  with open(USER_CONFIG, 'r') as config:
    return json.load(config)
  
def save_config(config):
  with open(USER_CONFIG, 'w') as config_file:
    json.dump(config, config_file, indent=2)
    
def prompt_for_config():
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

def copy_files():
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
    

def main():
  config = load_config(USER_CONFIG)
  if not config:
    config = prompt_for_config()
  result = copy_files()
  if not result:
    print('Something went wrong')
  else:
    print('Files copied!')
  
main()
    
# os.system('git pull')
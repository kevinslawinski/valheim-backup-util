import json
import os

class ConfigManager:
  USER_CONFIG = 'config.json'
    
  def save_config(self, config):
    with open(self.USER_CONFIG, 'w') as config_file:
      json.dump(config, config_file, indent=2)

  def print_config(self):
    config = self.load_config()
    print('\nCurrent configuration:\n')
    print(f'  World Name: {config.get("world_file_name")}')
    print(f'  Valheim Save Location: {config.get("local_path")}')
    print(f'  Repo Path: {config.get("repo_path")}')

  def generate_config(self):
    print('\nNew configuration:\n')
    world_file_name = input('  Name of the Valheim world: ')
    local_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')
    repo_path = input('  Path to Valiheim remote repository: ')
    config = {
      'world_file_name': world_file_name,
      'local_path': local_path,
      'repo_path': repo_path
    }
    self.save_config(config)
    return config

  def load_config(self):
    print('Loading config file...')
    if not os.path.exists(self.USER_CONFIG):
      print('Config file not found.')
      return self.generate_config()
    
    with open(self.USER_CONFIG, 'r') as config:
      return json.load(config)
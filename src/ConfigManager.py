import json
import os

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
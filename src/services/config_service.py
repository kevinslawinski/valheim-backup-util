import json
import logging
import os

class ConfigService:
  USER_CONFIG = 'config.json'
    
  def save_config(self, config):
    try:
      with open(self.USER_CONFIG, 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, indent=2, ensure_ascii=False)
    except PermissionError as e:
      logging.error(f"Permission denied when saving config: {e}")
      raise
    except Exception as e:
      logging.error(f"Unexpected error when saving config: {e}")
      raise

  def load_config(self):
    if not os.path.exists(self.USER_CONFIG):
      logging.error('Config file not found.')
      new_config = self.generate_config()
      return new_config
    # Check if the config path is a directory
    if os.path.isdir(self.USER_CONFIG):
      raise ValueError('Config path is a directory, not a file.')
    try:
      with open(self.USER_CONFIG, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
        # Validation logic
        required_fields = {'world_file_name', 'local_path', 'repo_path'}
        config_keys = set(config.keys())
        # Check for missing fields
        missing = required_fields - config_keys
        if missing:
          raise ValueError(f"Config missing required fields: {missing}")
        # Check for extra fields
        extra = config_keys - required_fields
        if extra:
          raise ValueError(f"Config has unexpected fields: {extra}")
        # Check for empty or null values
        for field in required_fields:
          if config[field] is None or config[field] == '':
            raise ValueError(f"Config field '{field}' is empty or null.")
        return config
    except json.JSONDecodeError as e:
      logging.error(f"Config file is not valid JSON: {e}")
      raise
    except PermissionError as e:
      logging.error(f"Permission denied when loading config: {e}")
      raise
    except Exception as e:
      logging.error(f"Unexpected error when loading config: {e}")
      raise
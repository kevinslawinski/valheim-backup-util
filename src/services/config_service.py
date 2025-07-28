import json
import logging
import os

class ConfigService:
    USER_CONFIG = 'config.json'

    @classmethod
    def save(cls, config):
        """
        Save the provided configuration dictionary to the config file.
        Args:
            config (dict): The configuration data to save.
        Raises:
            PermissionError: If the file cannot be written due to permissions.
            Exception: For any other unexpected errors during save.
        """
        try:
            with open(cls.USER_CONFIG, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, indent=2, ensure_ascii=False)
        except PermissionError as e:
            logging.warning("Permission denied when saving config: %s", e)
            raise
        except Exception as e:
            logging.warning("Unexpected error when saving config: %s", e)
            raise

    @classmethod
    def get(cls):
        """
        Load and validate the configuration from the config file.
        Returns:
            dict: The loaded configuration data.
        Raises:
            FileNotFoundError: If the config file does not exist.
            ValueError: If the config file is a directory, missing required fields, has extra fields, or contains empty/null values.
            json.JSONDecodeError: If the config file is not valid JSON.
            PermissionError: If the file cannot be read due to permissions.
            Exception: For any other unexpected errors during load.
        """
        # Check if the config file exists
        if not os.path.exists(cls.USER_CONFIG):
            message = f"Config file '{cls.USER_CONFIG}' does not exist."
            logging.error(message)
            raise FileNotFoundError(message)
        
        # Check if the config path is a directory
        if os.path.isdir(cls.USER_CONFIG):
            raise ValueError('Config path is a directory, not a file.')
        
        try:
            with open(cls.USER_CONFIG, 'r', encoding='utf-8') as config_file:
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
            logging.error("Config file is not valid JSON: %s", e)
            raise
        except PermissionError as e:
            logging.error("Permission denied when loading config: %s", e)
            raise
        except Exception as e:
            logging.error("Unexpected error when loading config: %s", e)
            raise
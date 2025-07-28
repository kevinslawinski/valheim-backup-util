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
        Notes:
            Logs a warning if saving fails due to permissions or other errors.
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
        Notes:
            Logs errors for missing file, directory path, missing/extra/empty fields, invalid JSON, and permission issues.
            Validates required fields ('world_file_name', 'local_path', 'repo_path') and checks for empty/null values.
        """
        # Check if the config file exists
        if not os.path.exists(cls.USER_CONFIG):
            message = f"Config file '{cls.USER_CONFIG}' does not exist."
            logging.error(message)
            raise FileNotFoundError(message)
        
        # Check if the config path is a directory
        if os.path.isdir(cls.USER_CONFIG):
            message = f"Config path '{cls.USER_CONFIG}' is a directory, not a file."
            logging.error(message)
            raise ValueError(message)
        
        try:
            with open(cls.USER_CONFIG, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                # Validation logic
                required_fields = {'world_file_name', 'local_path', 'repo_path'}
                config_keys = set(config.keys())
                # Check for missing fields
                missing = required_fields - config_keys
                if missing:
                    message = f"Config is missing required fields: {missing}"
                    logging.error(message)
                    raise ValueError(message)
                # Check for extra fields
                extra = config_keys - required_fields
                if extra:
                    message = f"Config has unexpected fields: {extra}"
                    logging.error(message)
                    raise ValueError(message)
                # Check for empty or null values
                for field in required_fields:
                    if config[field] is None or config[field] == '':
                        message = f"Config field '{field}' is empty or null."
                        logging.error(message)
                        raise ValueError(message)
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
import unittest
import json
import os
from unittest import mock
from unittest.mock import mock_open, patch

# Import the ConfigManager class from your module
from src.ConfigManager import ConfigManager

# Define a temporary file path for testing
# TEST_CONFIG_FILE = 'test_config.json'





# TESTS PASS BUT THEY ARE OVERWRITING THE ACTUAL CONFIG FILE





class TestConfigManager(unittest.TestCase):

    def setUp(self):
        # Create a sample config file for testing
        self.sample_config = {
            'world_file_name': 'TestWorld',
            'local_path': 'C:\\Users\\TestUser\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local',
            'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
        }
        self.temp_config_file = 'temp_config.json'
        with open(self.temp_config_file, 'w') as f:
            json.dump(self.sample_config, f)

    def tearDown(self):
        # Remove the temporary config file after each test
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)

    def test_save_config(self):
        config_manager = ConfigManager()
        test_config = {
            'world_file_name': 'TestWorld',
            'local_path': 'C:\\Users\\TestUser\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local',
            'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
        }
        config_manager.save_config(test_config)

        # Check if the saved config file exists
        self.assertTrue(os.path.exists(config_manager.USER_CONFIG))

        # Check if the saved config matches the original
        with open(config_manager.USER_CONFIG, 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config, test_config)

    @patch('builtins.input', side_effect=['TestWorld', 'C:\\Users\\TestUser\\ValheimRepo'])
    @patch('os.getenv', return_value='C:\\Users\\TestUser')
    def test_generate_config(self, mock_input, mock_getenv):
        config_manager = ConfigManager()
        generated_config = config_manager.generate_config()

        # Check if the generated config matches the expected format
        self.assertEqual(generated_config['world_file_name'], 'TestWorld')
        self.assertEqual(generated_config['repo_path'], 'C:\\Users\\TestUser\\ValheimRepo')

        # Verify that the config is saved correctly to the file
        saved_config = config_manager.load_config()
        self.assertEqual(saved_config['world_file_name'], 'TestWorld')
        self.assertEqual(saved_config['repo_path'], 'C:\\Users\\TestUser\\ValheimRepo')

    @patch('src.ConfigManager.ConfigManager.USER_CONFIG', 'temp_config.json')
    def test_load_config_existing(self):
        config_manager = ConfigManager()

        # Load the configuration
        loaded_config = config_manager.load_config()

        # Check if the loaded config matches the sample config
        self.assertEqual(loaded_config, self.sample_config)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_missing_file(self, mock_open, mock_exists):
        # Set up the mock open to read the temporary config file
        mock_open.return_value.read.return_value = json.dumps({
            'world_file_name': 'NewWorld',
            'local_path': 'D:\\ValheimBackups',
            'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
        })

        config_manager = ConfigManager()

        # Patch the generate_config method to bypass user input
        def mock_generate_config(self):
            return {
                'world_file_name': 'NewWorld',
                'local_path': 'D:\\ValheimBackups',
                'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
            }

        with patch.object(ConfigManager, 'generate_config', mock_generate_config):
            loaded_config = config_manager.load_config()

        # Check if the loaded config matches the mock data
        self.assertEqual(loaded_config['world_file_name'], 'NewWorld')
        self.assertEqual(loaded_config['local_path'], 'D:\\ValheimBackups')
        self.assertEqual(loaded_config['repo_path'], 'C:\\Users\\TestUser\\ValheimRepo')

    @patch('src.ConfigManager.ConfigManager.USER_CONFIG', 'temp_config.json')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', mock_open(read_data=json.dumps({
        'world_file_name': 'TestWorld',
        'local_path': 'C:\\Users\\TestUser\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local',
        'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
    })))
    @patch('builtins.input', side_effect=['TestWorld', 'C:\\Users\\TestUser\\ValheimRepo'])
    def test_print_config(self, mock_input, mock_exists):
        config_manager = ConfigManager()
        with patch('builtins.print') as mocked_print:
            config_manager.print_config()

            # Check if print function was called with the correct output
            expected_output = [
                f'  World Name: TestWorld',
                f'  Valheim Save Location: C:\\Users\\TestUser\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local',
                f'  Repo Path: C:\\Users\\TestUser\\ValheimRepo'
            ]
            mocked_print.assert_any_call('\nCurrent configuration:\n')
            for expected_line in expected_output:
                mocked_print.assert_any_call(expected_line)


if __name__ == '__main__':
    unittest.main()
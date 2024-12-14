import json
import sys
from json import JSONDecodeError
from pathlib import Path

from md_launcher.components.launcher.model.configuration_model import ConfigurationModel
from md_launcher.components.md_common_python.py_common.logging import HoornLogger

if __name__ == "__main__":
	module_separator = "LAUNCHER"
	high_level_logger: HoornLogger = HoornLogger(separator_root=module_separator)

	args = sys.argv[1:]

	if len(args) < 1:
		high_level_logger.critical("A path to the configuration json file is required.")
		exit(1)

	configuration_file = args[0]

	try:
		configuration_path = Path(configuration_file)
	except FileNotFoundError:
		high_level_logger.critical(f"Configuration file '{configuration_file}' not found.")
		exit(1)
	except Exception as e:
		high_level_logger.critical(f"An error occurred while trying to access the configuration file: {str(e)}")
		exit(1)

	try:
		with open(configuration_path, 'r') as f:
			config_model: ConfigurationModel = ConfigurationModel(**json.load(f))
	except JSONDecodeError:
		high_level_logger.critical(f"Invalid JSON format in the configuration file '{configuration_file}'.")
		exit(1)
	except Exception as e:
		high_level_logger.critical(f"An error occurred while trying to parse the configuration file: {str(e)}")
		exit(1)

import json
import os
import sys

from json import JSONDecodeError
from pathlib import Path

from md_launcher.components.launcher.config_validation import ConfigValidation
from md_launcher.components.launcher.launch_util import LaunchUtil
from md_launcher.components.launcher.model.raw_configuration_model import RawConfigurationModel
from md_launcher.components.md_common_python.py_common.logging import HoornLogger, DefaultHoornLogOutput, \
	FileHoornLogOutput, LogType


def get_log_dir(application_name: str):
	"""Gets the log directory.

	Returns:
	  The log directory.
	"""

	try:
		user_config_dir = os.path.expanduser("~")
	except Exception as e:
		raise e

	dir = os.path.join(user_config_dir, "AppData", "Local")
	log_dir = os.path.join(dir, application_name, "logs", "Launcher")
	return log_dir

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
			config_model: RawConfigurationModel = RawConfigurationModel(**json.load(f))
	except JSONDecodeError:
		high_level_logger.critical(f"Invalid JSON format in the configuration file '{configuration_file}'.")
		exit(1)
	except Exception as e:
		high_level_logger.critical(f"An error occurred while trying to parse the configuration file: {str(e)}")
		exit(1)

	validated_config = ConfigValidation(config_model, high_level_logger).validate_configuration()

	log_dir = Path(get_log_dir(validated_config.project_name))
	root_separator = validated_config.project_name
	real_logger = HoornLogger(separator_root=root_separator, outputs=[DefaultHoornLogOutput(), FileHoornLogOutput(log_dir, max_logs_to_keep=5)], min_level=LogType.DEBUG if validated_config.debug_mode else LogType.INFO)

	real_logger.info("Successfully started the launcher.", separator="Launcher")

	launch_util: LaunchUtil = LaunchUtil(validated_config, real_logger)
	launch_util.launch()

	real_logger.info("Successfully launched application.", separator="Launcher")


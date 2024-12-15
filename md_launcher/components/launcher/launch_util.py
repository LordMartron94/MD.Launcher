import time
from pathlib import Path

from md_launcher.components.launcher.model.configuration_model import ConfigurationModel
from md_launcher.components.md_common_python.py_common.command_handling import CommandHelper
from md_launcher.components.md_common_python.py_common.logging import HoornLogger

SUPPORTED_TYPES = ["Python", "Exe"]


class LaunchUtil:
	"""
	This class handles the actual launching of the application.
	"""

	def __init__(self, configuration: ConfigurationModel, logger: HoornLogger, separator: str = "Launcher"):
		self._configuration: ConfigurationModel = configuration
		self._logger = logger
		self._separator = separator
		self._command_helper = CommandHelper(self._logger, self._separator + ".Command")
		self._sequence_sleep = 1

	def launch(self):
		self._launch_router()
		time.sleep(self._sequence_sleep)  # Middleman needs some time to launch
		self._launch_components()
		self._logger.info("Launched Router successfully", separator=self._separator)

	def _launch_router(self):
		self._command_helper.open_application(exe=self._configuration.router_binary, args=[self._configuration.project_name], new_window=True)

	def _launch_components(self):
		for component in self._configuration.components:
			file_path = self._configuration.project_root.joinpath(component.file_path)
			file_path = Path(str(file_path).replace("${sanitized_project_name}", self._configuration.sanitized_project_name))
			arguments = component.args
			arguments = [arg.replace("${project_name}", f"{self._configuration.project_name}") for arg in arguments]

			if component.type == "Exe":
				self._command_helper.open_application(exe=file_path, args=arguments)
			elif component.type == "Python":
				venv_path: Path = self._configuration.python_venv_path

				if venv_path is None:
					self._logger.error(f"Cannot launch Python component {component.file_path} because Python Virtual Environment path is not set.", separator=self._separator)
					continue
				if not venv_path.exists():
					self._logger.error(f"Cannot launch Python component {component.file_path} because Python Virtual Environment executable does not exist at {venv_exe}.", separator=self._separator)
					continue

				self._command_helper.open_application(exe=venv_path, args=[f"{file_path}"] + arguments, new_window=not self._configuration.components_launch_in_background)

			time.sleep(self._sequence_sleep)

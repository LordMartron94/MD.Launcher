import time

from md_launcher.components.launcher.model.configuration_model import ConfigurationModel
from md_launcher.components.md_common_python.py_common.command_handling import CommandHelper
from md_launcher.components.md_common_python.py_common.logging import HoornLogger


class LaunchUtil:
	"""
	This class handles the actual launching of the application.
	"""

	def __init__(self, configuration: ConfigurationModel, logger: HoornLogger, separator: str = "Launcher"):
		self._configuration = configuration
		self._logger = logger
		self._separator = separator
		self._command_helper = CommandHelper(self._logger, self._separator + ".Command")

	def launch(self):
		self._launch_router()
		time.sleep(1)  # Middleman needs some time to launch
		self._logger.info("Launched Router successfully", separator=self._separator)

	def _launch_router(self):
		self._command_helper.open_application(exe=self._configuration.router_binary, args=[self._configuration.project_name])

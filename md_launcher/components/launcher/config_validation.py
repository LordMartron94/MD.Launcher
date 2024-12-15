from pathlib import Path

from md_launcher.components.launcher.model.configuration_model import ConfigurationModel
from md_launcher.components.launcher.model.raw_configuration_model import RawConfigurationModel
from md_launcher.components.md_common_python.py_common.logging import HoornLogger
from md_launcher.components.launcher.constants import PROJECT_ROOT


class ConfigValidation:
	def __init__(self, configuration: RawConfigurationModel, logger: HoornLogger):
		self._configuration = configuration
		self._logger = logger

	def validate_configuration(self) -> ConfigurationModel:
		root: Path = PROJECT_ROOT

		self._logger.info(f"Using dynamically constructed project root: '{root}' for configuration validation.")

		if not root.exists():
			self._logger.error(f"Project root '{root}' does not exist.\nMake sure that you follow the correct project structure!")
			exit(1)

		router_binary = root.joinpath("router").joinpath("router.exe")
		if not router_binary.exists():
			self._logger.error(f"Router binary '{router_binary}' does not exist.")
			exit(1)

		venv_exe = root.joinpath("venv", "Scripts", "python.exe")
		config_model = ConfigurationModel(**self._configuration.model_dump(), router_binary=router_binary, python_venv_path=venv_exe, project_root=root)

		if config_model.python_venv_path is not None:
			if not config_model.python_venv_path.exists():
				self._logger.error(f"Python Virtual Environment path '{config_model.python_venv_path}' does not exist.")
				exit(1)

		return config_model


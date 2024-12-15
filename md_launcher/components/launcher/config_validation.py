from md_launcher.components.launcher.model.configuration_model import ConfigurationModel
from md_launcher.components.launcher.model.raw_configuration_model import RawConfigurationModel
from md_launcher.components.md_common_python.py_common.logging import HoornLogger


class ConfigValidation:
	def __init__(self, configuration: RawConfigurationModel, logger: HoornLogger):
		self._configuration = configuration
		self._logger = logger

	def validate_configuration(self) -> ConfigurationModel:
		router_binary = self._configuration.project_root.joinpath("router").joinpath("router.exe")
		if not router_binary.exists():
			self._logger.error(f"Router binary '{router_binary}' does not exist.")
			exit(1)

		config_model = ConfigurationModel(**self._configuration.model_dump(), router_binary=router_binary)

		if config_model.python_venv_path is not None:
			if not config_model.python_venv_path.exists():
				self._logger.error(f"Python Virtual Environment path '{config_model.python_venv_path}' does not exist.")
				exit(1)

		return config_model


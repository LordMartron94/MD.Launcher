from pathlib import Path
from typing import List, Optional

import pydantic
from pydantic import Field

from md_launcher.components.launcher.model.component_model import ComponentModel


class RawConfigurationModel(pydantic.BaseModel):
	project_name: str
	sanitized_project_name: str
	components: List[ComponentModel] = Field(default_factory=list)
	debug_mode: bool = Field(default=False)
	components_launch_in_background: bool = Field(default=False)
	venv_override: str = Field(default=None)

	@pydantic.field_validator("project_name", mode="before")
	@classmethod
	def validate_project_name(cls, value: str) -> str:
		if value == "":
			raise ValueError("Project name cannot be empty.")
		return value

	@pydantic.field_validator("sanitized_project_name", mode="before")
	@classmethod
	def validate_project_name(cls, value: str) -> str:
		if value == "":
			raise ValueError("Sanitized Project name cannot be empty.")
		return value

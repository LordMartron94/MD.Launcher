from pathlib import Path
from typing import List, Optional

import pydantic
from pydantic import Field

from md_launcher.components.launcher.model.component_model import ComponentModel


class RawConfigurationModel(pydantic.BaseModel):
	project_root: Path
	project_name: str
	components: List[ComponentModel] = Field(default_factory=list)
	python_venv_path: Optional[Path] = Field(default=None)
	debug_mode: bool = Field(default=False)
	components_launch_in_background: bool = Field(default=False)

	@pydantic.field_validator("project_root", mode="before")
	@classmethod
	def validate_project_root(cls, value: str) -> Path:
		if value == "":
			raise ValueError("Project root cannot be empty.")

		value = Path(value)

		if not value.exists():
			raise ValueError("Project root does not exist.")
		if not value.is_dir():
			raise ValueError("Project root must be a valid directory.")
		return value

	@pydantic.field_validator("project_name", mode="before")
	@classmethod
	def validate_project_name(cls, value: str) -> str:
		if value == "":
			raise ValueError("Project name cannot be empty.")
		return value

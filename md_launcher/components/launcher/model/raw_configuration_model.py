from pathlib import Path

import pydantic


class RawConfigurationModel(pydantic.BaseModel):
	project_root: Path
	project_name: str

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

from pathlib import Path
from typing import List, Optional

import pydantic

from md_launcher.components.launcher.model.component_model import ComponentModel


class ConfigurationModel(pydantic.BaseModel):
	project_root: Path
	project_name: str
	router_binary: Path
	components: List[ComponentModel]
	python_venv_path: Optional[Path]
	debug_mode: bool
	components_launch_in_background: bool

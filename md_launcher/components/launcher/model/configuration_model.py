from pathlib import Path
from typing import List

import pydantic


class ConfigurationModel(pydantic.BaseModel):
	project_root: Path
	project_name: str
	router_binary: Path
	component_launchers: List[Path]

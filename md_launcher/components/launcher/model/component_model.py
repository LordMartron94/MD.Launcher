from pathlib import Path
from typing import List

import pydantic


class ComponentModel(pydantic.BaseModel):
	file_path: Path
	args: List[str]
	type: str


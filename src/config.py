from dotenv import dotenv_values
from typing import Dict
from pathlib import Path

async def get_config(mode: str) -> Dict:
    file_path = Path(__file__)
    root_path = file_path.parents[1]
    if 'sim' in mode:
        env_path = root_path / "sim.env"
    else:
        env_path = root_path / ".env"
    print(f"Loading config from {env_path}")
    config = {**dotenv_values(dotenv_path=env_path)}
    return config

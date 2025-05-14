"""
    Default Configurations

"""
from pathlib import Path

# Saved root directory by root items
project_root = Path(__file__).parent  
while not (project_root / "requirements.txt").exists() and not (project_root / "run,py").exists():
    project_root = project_root.parent 
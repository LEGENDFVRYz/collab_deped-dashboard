from pathlib import Path

## getting the main root folder of the project
def find_project_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / ".gitignore").exists() or (parent / "run.py").exists():
            return parent
    raise FileNotFoundError("Could not find the project root")
    
project_root = find_project_root()
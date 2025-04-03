# from pathlib import Path

# # Find the root directory by looking for a specific marker file
# project_root = Path(__file__).parent  # Get current directory of the script
# while not (project_root / "requirements.txt").exists() and not (project_root / "run,py").exists():
#     project_root = project_root.parent 
    
# # Export project_root for other modules
# __all__ = ["project_root"]
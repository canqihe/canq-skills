#!/usr/bin/env python3
"""
Setup script for ModelScope Image Generation skill
Creates virtual environment and installs dependencies
"""

import subprocess
import sys
from pathlib import Path


def main():
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / ".venv"
    requirements = skill_dir / "requirements.txt"

    print(f"Skill directory: {skill_dir}")

    # Create virtual environment
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    # Get pip path
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"

    # Install requirements
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", str(requirements)], check=True)

    print("✅ Setup complete!")


if __name__ == "__main__":
    main()

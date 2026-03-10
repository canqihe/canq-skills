#!/bin/bash
# Wrapper script that loads environment variables from user's shell config

# Detect user's shell and source the appropriate config
if [ -n "$ZSH_VERSION" ]; then
    source ~/.zshrc 2>/dev/null || true
elif [ -n "$BASH_VERSION" ]; then
    source ~/.bashrc 2>/dev/null || source ~/.bash_profile 2>/dev/null || true
fi

# Run the Python script with all arguments passed through
python3 ~/.claude/skills/nano-banana-pro/scripts/generate_image.py "$@"

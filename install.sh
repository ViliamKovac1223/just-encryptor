#!/bin/bash

# install dependencies
pip install pycryptodome

# check if "$HOME/.local/bin" is in the "$PATH" if no then add it to the "$PATH"
if [ "$(echo "$PATH" | grep -c "\./local/bin")" -lt 1 ]; then
  [ -d "$HOME/.local/bin" ] || mkdir -p "$HOME/.local/bin" # create "$HOME/.local/bin" if doesn't exist
  echo "PATH=\"$HOME/.local/bin:$PATH\"" >> "$HOME/.bashrc"
  [ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc"
fi

chmod +x jenc.py
[ -f "$HOME/.local/bin/jenc" ] || ln -s "$(pwd)/jenc.py" "$HOME/.local/bin/jenc"

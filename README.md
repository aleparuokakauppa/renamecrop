# Renamecrop

## Description
Resize and name images in bulk through a GUI
Created with:
- [PySimpleGUI](https://github.com/PySimpleGUI)
- [Wand](https://github.com/emcconville/wand)
- [Pil](https://github.com/python-pillow/Pillow)

## Usage
Two ways:
Manual or Windows executable

### Manual
Install dependencies:

`pip install PySimpleGUI Wand Pillow`

Run the script:

`python main.py`

### Executable
The binary was built on Windows 11 amd64 with Pyinstaller.

Sha256: `68c7090076dcb29d2b5023971942c184a3aee9662f43696da463e802432ec98e  main.exe`

Manual installation is preferred, since the binary is mainly for my own convenience.

- Download and run the .exe file on a amd64-system

If this doesn't work -> Manual installation

## Goal
- Create a working and simple to use GUI image resizer + renamer
- Application is reasonably performant
- A Windows installer for use by non-developers

## Roadmap
- A preview for the RGB selector

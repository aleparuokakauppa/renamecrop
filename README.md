# Renamecrop

## Note
Since PySimpleGUI has switched to a paid model, this project will no longer be maintained.

## Description
Resize and name images in bulk through a GUI
Created with:
- [PySimpleGUI](https://github.com/PySimpleGUI)
- [Wand](https://github.com/emcconville/wand)
- [Pil](https://github.com/python-pillow/Pillow)

## Screenshot
![Screenshot](https://github.com/aleparuokakauppa/renamecrop/blob/main/screenshots/Renamecrop.jpeg?raw=true)

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

Sha256: `669e16c6ea9787cdd6dba89fe0c7b84b8e993d1d256089d9d95ec673881e2ec6  main.exe`

Manual installation is preferred, since the binary is mainly for my own convenience.

- Download and run the .exe file on a amd64-system

If this doesn't work -> Manual installation

## Goal
- Create a working and simple to use GUI image resizer + renamer
- Application is reasonably performant
- A Windows installation for use by non-developers

## Roadmap
- Fix the ugly UI
- A preview for the RGB selector
- Semantic corrections as they come up
- A proper installer for multi-platform, not a single .exe

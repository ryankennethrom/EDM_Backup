#!/bin/bash

python -m pip install -r requirements.txt
python -m PyInstaller --onefile BackupSettings.py
python -m PyInstaller --onefile BackupX.py

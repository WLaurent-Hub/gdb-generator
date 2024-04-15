@echo off

rem Configuration du code page en UTF-8
chcp 65001 > nul

rem # Chemin vers le fichier propy.bat
set PROPY_BAT_PATH="C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat"

rem Définir la région 
rem Pour afficher la liste des régions disponibles, remplacer REGION_NAME par "-help"
set REGION_NAME="ALL"

rem Exécute le script main.py avec region_name comme argument
%PROPY_BAT_PATH% "main.py" %REGION_NAME% 


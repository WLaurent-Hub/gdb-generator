# Générateur de Géodatabase par Région

Ce script Python permet de générer une géodatabase par région contenant différentes couches géographiques à partir de données sources, en utilisant les librairies arcpy et arcgis.

## Fonctionnalités

Le script génère une géodatabase (fichier `.gdb`) contenant les couches suivantes pour chaque région spécifiée :
- Une feature représentant les rivières de la région.
- Une feature représentant les routes de la région.
- Une feature des départements de la région.

## Installation

Avant d'exécuter le script, assurez-vous de suivre ces étapes d'installation :

1. **Installer Python** :
    - Assurez-vous d'avoir Python installé sur votre système. Vous pouvez le télécharger depuis [python.org](https://www.python.org/downloads/) et suivre les instructions d'installation.

2. **Installer ArcGis Pro Desktop** :
    - Assurez-vous d'avoir une licence ArcGis Pro sur votre système. Vous pouvez le télécharger depuis [arcgis.org](https://pro.arcgis.com/fr/pro-app/latest/get-started/get-started.htm) et suivre les instructions d'installation:

3. **Configurer le fichier `exec.bat`** :
    - Ouvrez le fichier `exec.bat` dans un éditeur de texte (**e.g** : VS Code, notepad++, sublime text).
    - Recherchez la variable `PROPY_BAT_PATH` contenant le chemin vers `propy.bat`.
    ```batch
    set "PROPY_BAT_PATH=C:\chemin\vers\propy.bat"
    ```
    - Remplacez `C:\chemin\vers\propy.bat` par le chemin correct vers votre fichier `propy.bat`.
    - Rechercher la variable `REGION_NAME` contenant le nom de la région à spécifier.
    ```batch
    set REGION_NAME="region_à_spécifier"
    ```
    - Remplacer `"region_à_spécifier"` par une région disponible
    - Pour afficher la liste des régions disponibles, remplacer REGION_NAME par "-help"
    ```batch
    set REGION_NAME="-help"
    ```
4. **Executer le fichier `exec.bat`**: 
    - Double-clique sur ce fichier pour lancer l'exécution du script

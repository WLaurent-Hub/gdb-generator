import arcpy
import os
import re 

class Geoprocessing():
    
    WORKSPACE = os.getcwd() 
    
    REGION = os.path.join(WORKSPACE, "data", "REGION.shp")
    RIVIERE = os.path.join(WORKSPACE, "data", "riviere", "riviere.shp")
    ROUTES = os.path.join(WORKSPACE, "data", "route", "route.shp")
    DEPARTEMENTS = os.path.join(WORKSPACE, "data", "DEPARTEMENT.shp")
    
    def __init__(self, region_name):
        self.region_name = re.sub(r"'", "''", region_name)

        
    def create_geodatabase(self):
        """
            Fonction pour créer une géodatabase en fonction du nom de région fourni.
            Si le nom de région n'est pas "ALL", cela crée une géodatabase avec le nom de la région.
            Si le nom de région est "ALL", cela crée une géodatabase nommée "ALL.gdb".
            Renvoie True si la création de la géodatabase est réussie, sinon False.
        """
        
        try:
            
            if self.region_name != "ALL":
                
                query = f"NOM_REG = '{self.region_name}'"
                arcpy.MakeFeatureLayer_management(self.REGION, "test_layer")
                arcpy.SelectLayerByAttribute_management("test_layer", "NEW_SELECTION", query)
                
                count = int(arcpy.GetCount_management("test_layer").getOutput(0))
                
                # Vérifie si au moins une entité est sélectionnée
                if count > 0:
                    arcpy.CreateFileGDB_management(self.WORKSPACE, f'{self.region_name}.gdb')
                    print(f'Géodatabase {self.region_name}.gdb créée avec succès.')
                else:
                    print("Aucune région trouvée. Veuillez définir un nom de region valide.")
                    return False
            else:
                arcpy.CreateFileGDB_management(self.WORKSPACE, "ALL.gdb")
                print("Géodatabase ALL.gdb créée avec succès.")
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
            return False
        except Exception as e:
            print(e.args[0])
            return False
        return True
            
    def select_by_attribute(self):
        """
            Exécute une sélection par attribut basée sur la valeur de self.region_name.
            Utilise arcpy pour créer une couche d'entités et sélectionner par attribut.
        """
        
        try:
            if self.region_name == "ALL":
                query = None
            else:
                query = f"NOM_REG = '{self.region_name}'"
                
            # Génère une couche temporaire de la région spécifiée 
            arcpy.MakeFeatureLayer_management(self.REGION, "region_layer")
            arcpy.SelectLayerByAttribute_management("region_layer", "NEW_SELECTION", query)
            
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
        except Exception as e:
            print(e.args[0])

    def select_and_copy(self, shapefile, layer_name):
        """
            Fonction qui sélectionne et copie des entités en fonction de conditions spécifiques.

            Paramètres :
            - self : L'instance de l'objet.
            - shapefile : Le shapefile avec lequel travailler.
            - layer_name : Le nom de la couche à créer.
        """
        
        try:
            # Nettoye et formate le nom de la région
            clean_region_name = re.sub(r'[^\w\s]', '', self.region_name).replace(' ', '_')

            if not clean_region_name:
                print("Le nom de la région est invalide. Impossible de copier les entités.")
                return
            
            arcpy.MakeFeatureLayer_management(shapefile, layer_name)

            if shapefile == self.DEPARTEMENTS:
                # Jointure attributaire de la couche région_layer si le fichier est celui des départements
                arcpy.AddJoin_management(layer_name, "INSEE_REG", "region_layer", "INSEE_REG")
            
            if self.region_name != "ALL":
                if shapefile == self.DEPARTEMENTS:
                    # Sélection attributaire de la région spécifiée si ce n'est pas "ALL"
                    where_clause = f"NOM_REG = '{self.region_name}'"
                    arcpy.SelectLayerByAttribute_management(layer_name, "NEW_SELECTION", where_clause)
                else:
                    # Sélection spatial par intersection de la région si ce n'est pas "ALL"
                    arcpy.SelectLayerByLocation_management(layer_name, "INTERSECT", "region_layer")
            
            output_name = f"{clean_region_name}_{layer_name}"
            output_path = os.path.join(self.WORKSPACE, f"{self.region_name}.gdb", output_name)

            arcpy.CopyFeatures_management(layer_name, output_path)

        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
        except Exception as e:
            print(e.args[0])

    
    def select_by_location(self):
        """
            Fonction qui sélectionne et copie des entités en fonction de conditions spécifiques.
        """
        
        try:
            self.select_and_copy(self.RIVIERE, "rivieres")
            self.select_and_copy(self.ROUTES, "routes")
            self.select_and_copy(self.DEPARTEMENTS, "departements")
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
        except Exception as e:
            print(e.args[0])
            
def main():
    """
        Fonction principale du script. 
        Elle vérifie les arguments de la ligne de commande pour déterminer l'opération à effectuer. 
        Si le nombre d'arguments est inférieur à 2, elle fournit des instructions sur l'utilisation du script. 
        Si le premier argument est '-help', elle liste les régions disponibles. 
        Sinon, elle traite la région spécifiée en créant une géodatabase et en effectuant 
        des opérations de sélection d'attributs et d'emplacement à l'aide de la classe Geoprocessing.
    """
    
    if len(sys.argv) < 2:
        print("Utilisation :\n")
        print("   <propy_bat_path> main.py <region_name>")
        print("   - Pour exécuter le script avec une région spécifique.\n")
        print("   <propy_bat_path> main.py -help")
        print("   - Pour afficher les régions disponibles.")
        return
    
    if sys.argv[1] == "-help":
        print("Régions disponibles :")
        print("   - Occitanie")
        print("   - Centre-Val de Loire")
        print("   - Normandie")
        print("   - Nouvelle-Aquitaine")
        print("   - Grand Est")
        print("   - Provence-Alpes-Côte d'Azur")
        print("   - Auvergne-Rhône-Alpes")
        print("   - Bourgogne-Franche-Comté")
        print("   - Pays de la Loire")
        print("   - Hauts-de-France")
        print("   - Bretagne")
        print("   - Corse")
        print("   - Île-de-France")
        print("   - Guadeloupe")
        print("   - Martinique")
        print("   - Mayotte")
        print("   - La Réunion")
        print("   - Guyane")
        return
    
    region_name = sys.argv[1]
    gp = Geoprocessing(region_name)
    
    if gp.create_geodatabase():
        gp.select_by_attribute()
        gp.select_by_location()

if __name__ == '__main__':
    main()
    


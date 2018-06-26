# Architecture avec Terraform  

## Résumé et objectif de ce projet  

Ce projet à pour objectif de recenser de manière synthétique comment manipuler Terraform en entreprise pour déployer et répliquer aisément une architecture sur AWS.  

## Structure de base de Terraform    

### Fichier main.tf (basique)  
Créez un dossier et un fichier main.tf . Ce fichier est nécessaire pour recenser toutes les ressources à déployer, toutes les déclarations se feront ici.

Exemple de fichier main.tf
```
provider "aws" {  
  region = "<Region>" # Region == eu-west-1 ou une variable ${var.region}  
}  
```

### Fichier variables.tf  

Additionnellement, un second fichier peut être utilisé pour recenser et déclarer toutes les variables utilisés dans main.tf. Ce fichier s'appelle variables.tf . Les types de variables doivent être déclarées: string, map,list.  

Voici ce que ça donne:  
```
variable "variable_string" {
 description = "Description de la variable"
 type = "string" 
 default = "this is the default value"
}
variable "variable_list" {  
 description = "Description de la variable"  
 type = "list"  
 default = ["item1","item2"]  
}
variable "variable_map" {
 description = "Description de la variable"
 type = "map"
 default {
   "ireland" = "eu-west-1",
   "francfort" = "eu-east-1"
 }
}
```
Ces variables pourront être référencées sur dans le fichier main.tf par interpolation:  
```
 "${var.variable_string}" 

 "${var.variable_list}" 
 "${var.variable_list[0]}" 

 "${lookup(var.variable_map,ireland)}" 
```
### Gestion environnements  

Les environnements peuvent être gérés facilement la stack par la créations de sous-dossiers. A l'intérieur de ces sous-dossiers, deux fichiers nécessaires:  
 * terraform.tfvars:  
  Contient les valeurs des variables pour l'environnement souhaité.

 * state.tf:  
  Contient les données nécessaires pour stocker l'état des ressources sur AWS pour ensuite les comparer avec le fichier terraform en local pour trouver les éventuelles différences.  
  Exemple de contenu :  
  ```
  terraform {  
    backend "s3" {  
      bucket     = "<NomBucket>"  
      key        = "NomFichierTFSTATE"  
      dynamodb_table = "<NomTable>"  
      region     = "<Region>"  
    }  
  }  
  ```
En addition de ces nouveaux fichiers, des liens symboliques doivent être en place vers les fichiers main.tf et variable.tf précédement définis. Ces fichiers sont à la racine de la stack.  
De plus, les profiles AWS (pour aws cli) doivent être configurés (dans le fichier credentials de aws-cli) et le nom du profil de l'environnement doit être exporté sous la variable "AWS_PROFILE".  
L'utilisation de la DynamoDB Table permet de référencer quel utilisateur a démarré une édition des ressources pour cette stacks et empêche toute édition concurrente (Lock). Une fois l'édition terminée, la table est éditée à nouveau et le "state lock" est libéré, ce qui permet aux autres utilisateurs à lancer des éditions sur cette stack.  
Il est fortement recommandé de mettre comme dynamodb_table la même table pour toutes les stacks de cet environnement.   


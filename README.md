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

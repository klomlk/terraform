##Initialisation du backend sur Terraform 
Dans le dossier contenant l'environnement à modifier (par exemple dev), créer un fichier state.tf.
Ce fichier contiendra les données relatives à l'utilisation du bucket S3 où sera stocké l'état distant de l'architecture.

Voici ce que contiendra le fichier:

terraform {
  backend "s3" {
    bucket = "<Nom_Bucket>"
    key = "<Nom_Fichier_distant>"
    lock_table = "<Nom_Table_DynamoDB>"
    region = "<Region_AWS>" 
  }
}


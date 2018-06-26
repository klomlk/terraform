# Quelques retours d'expériences  
## Utilisation de conditions  
### Count:  
L'utilisation du paramètre count est possible sur toutes les ressources Terraform. 
Ce paramètre permet de définir le nombre de ressources identiques qui seront déployées. 
Pour notre cas, nous détournons son usage primaire pour différencier les environnements:  
```
variable "prod" {}  

prod=0 #Nous sommes en Dev  

resource "aws_security_group" "SG-Prod" { 
  count = "${var.prod}"  
  description = "Security Group d'environnement de Prod"  
}  
``` 
Dans l'exemple ci-dessus, le security group SG-Prod ne sera pas déployé en Dev, mais le sera si la variable "prod" est à 1.  

### Ternaire:
Les ternaires permettent d'ajouter plus de complexité dans les évaluations de conditions en effectuant 
deux tâches différentes suivant la valeur d'une variable analysée. 
```
  sg = ["${data.terraform_remote_state.BSG.BSG_AdminWindows_id}","${aws_security_group.SG-RDJ.id}","${var.prod == 1 ? "${join("", data.terraform_remote_state.DFS.*.SG-DFS_SHARED.id)}" : "${aws_security_group.SG-RDJ.id}" }"]  
``` 
Dans l'exemple ci-dessus, nous avons un ternaire débutant par "${ var.prod == 1 ... }" qui évalue la valeur de la variable prod. Si elle est à 1, nous sommes en Prod, à 0 nous sommes en Développement.  
Ensuite sont définies les actions:  
```
... ? "${join("", data.terraform_remote_state.DFS.*.SG-DFS_SHARED.id)}" : "${aws_security_group.SG-RDJ.id}" }"
```  
Après le point d'interrogation, deux possibilités sont offertes: `? TRUEVAL : FALSEVAL`. Si l'évaluation précédente est vrai, alors l'action à gauche du ':' est exécutée, sinon ce sera celle de droite.   

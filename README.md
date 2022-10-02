# pakman
Une exéprience d'apprentissage par supervision basée sur le célèbre jeu pacman par des étudiants d'Architcture Logiciels à l'ESGI


# Mouvement des fantômes

Pour chacun des fantômes, on associe une valeur alpha \in [0;1] tel que si le pacman est dans une direction d1,d2, et que 
le fantôme a la possibilité de se déplacer dans deux menant vers le pacman, alors il choisit une direction verticale avec une probabilité
\alpha.
# Définitions des états

La grille du jeu 1 est composée de 60x60 cases et sur chacune d'entre elles il existe 6 possibilités :  un mur, rien, une gomme,
un fantôme, une gomme avec un fantôme. Si nous composions une qtable avec l'ensemble des états possibles, nous aurions alors 3600⁶
soit quelque chose de l'ordre de 2^21 possibilités.
Pour éviter une exploision du temps de calcul, nous allons définir un ensemble de radars avec une portée limitée à une case (droite/gauche, haut-bas)
pour chacun des éléments qui composent le jeu. 

# Discussions

* Pour le radar fantome:
 -> une variable [0,1,...8] =[N, S, NE, SE, NW, SW, E, W] qui indique la direction du fantôme par rapport au pacman
 -> une variable pour la distance [0,1,2]=["1", "2", "SE3"] qui indique la distance entre le pacman et le fantôme
* 
LITReview est une application permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres / articles à la demande.

L’application permet de : 

1 - Demander des critiques de livres ou d’articles, en créant un ticket.
2 - Publier des critiques de livres ou d’articles.



Installation et exécution de l'application :

1 - Cloner le dépôt du projet à l'aide de la commande $ git clone https://github.com/isw120/P9 (vous pouvez également télécharger le code en temps qu'archive zip)

2 - Rendez-vous depuis un terminal à la racine du répertoire P9-master avec la commande $ cd P9-master/LITReview

3 - Créer un environnement virtuel pour le projet avec $ python -m venv env sous windows ou $ python3 -m venv env sous macos ou linux.

4 - Activez l'environnement virtuel avec $ env\Scripts\activate sous windows ou $ source env/bin/activate sous macos ou linux.

5 - Installez les dépendances du projet avec la commande $ pip install -r requirements.txt

6 - Créer et alimenter la base de données avec la commande $ python manage.py migrate et la commande $ python manage.py migrate LITReview

7 - Démarrer le serveur avec $ python manage.py runserver





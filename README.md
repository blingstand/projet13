# Projet 13 : Projet final 
*********************

Ce projet a été créé pour répondre aux exigence du projet 13 de la formation Openclassroom parcours Python. Il s'agit de mettre en oeuvre toutes mes compétences pour répondre aux besoins d'une association que je souhaite aider. Dans mon cas le [centre spa](https://www.spa24bergerac.org/) de ma ville.

Ma démarche a consisté à aller à la rencontre de ce centre et de me renseigner sur la manière dont il travaille. Lors de la présentation j'ai remarqué quelques points sur lesquels je pouvais faire gagner du temps au secrétariat en automatisant certaines tâches dans leur journée. A savoir : 
* mettre en évidence le travail à faire dans la journée, 
* donner rapidement accès à des données, 
* automatiser l'envoi de mail suite à une modification de la base.

L'appication que je propose à cette association traite du suivi de la stérilisation suite à une adoption. Légalement une personne doit stériliser l'animal qu'elle acquiert. Dans certain cas cette stérilisation doit avoir lieue après l'adoption. Cela nécessite un suivi qui peut être chronophage. Mon application veut limiter ce temps à effectuer du suivi en limitant l'action humaine a des tâches complexes et en la libérant des tâches répétitives. 

Développé avec Python 3.8, Django 3.1.1
Hébergé sur [Heroku](https://www.heroku.com/)

# Table des matières
(utilisateur)
1. [Installation](#installation(linux))
2. [Configuration](#configuration)
3. [Utilisation du site](#utilisation)
(développers)
4. [Détail des applications](#applications)
5. [Tests](#tests)
************************************************

## Installation(linux)

Ouvrez le terminal puis tapez
    
    $ mkdir new_file
    $ cd new_file
    $ git init
    $ git clone https://github.com/blingstand/projet13.git
    $ virtualenv env -p votre_version_de_python
    $ source votre_version_de_python/bin/activate
    $ pip install -r requirements.txt
************************************************

## Configuration

Dans mon projet vous allez avoir besoin d'un super utilisateur. Pour l'exemple je vais créer un 
compte > admin/admin@mail.fr/mdpadmin (pseudo/mail/mot de passe).

Pour ce faire : 

        $ python manage.py createsuperuser
        Username: admin # pseudo souhaité et appuyez sur retour.
        Email address: admin@mail.fr # mail souhaité et appuyez sur retour
        Password: ******** # mot de passe souhaité et appuyez sur retour
        Password (again) : ******** # même mot de passe pour confirmer et appuyez sur retour
        Superuser created successfully. # preuve que tout va bien =)

************************************************

## Utilisation

Je suppose que vous avez installé et configuré mon projet. Vous pouvez désormais le lancer en faisant : 

    $ python manage.py runserver

le système répondra : 

    System check identified no issues (0 silenced).
    March 20, 2020 - 11:17:10 #ma date de rédaction du readme =) 
    Django version 3.0.3, using settings 'pureBeurre.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Rendez-vous à cette adresse pour utiliser le site en local : http://127.0.0.1:8000/
Afin d'utiliser le site il faut être connecté. Je vous rappelle que vous avez créé précédemment un superuser à cet effet. 

Je vous laisse ensuite explorer les fonctionnalités ...

************************************************
## Applications

En parcourant mon projet vous verrez plusieurs applications: 
1. [Core](https://github.com/blingstand/projet13/tree/master/core) > elle contient mes templates de base ainsi que les feuilles de styles de chaque page.
2. [Info](https://github.com/blingstand/projet13/tree/master/info) > elle contient tous ce que vous trouverez dans la partie information. A savoir la page à propos et l'index de l'app.
3. [Mail](https://github.com/blingstand/projet13/tree/master/mail) > elle contient tout ce qui a trait aux mails. A savoir le model pour mail, la préparation de mails auto, création, affichage, modification et suppression.
4. [MyDashboard](https://github.com/blingstand/projet13/tree/master/mydashboard) > elle contient tout ce qui a trait au tableau de bord. A savoir le graphique et les calculs nécessaire pour afficher les raccourcis vers les propriétaires contactés et à contacter.
5. [Sheet](https://github.com/blingstand/projet13/tree/master/sheet) > elle contient tout ce qui a trait aux fiches. A savoir les models pour animaux, admin, proprio et contact, mais aussi les formulaires et les pages HTML.
6. [Spa-Conf](https://github.com/blingstand/projet13/tree/master/spa-conf) > elle contient le settings et les réglages de l'app.
7. [User](https://github.com/blingstand/projet13/tree/master/user) > elle contient le nécessaire pour identifier les utilisateurs.

## Tests

<!-- J'ai organisé mes tests de la manière suivante. Ils sont tous regroupés dans le dossier [test](https://github.com/blingstand/projet8/tree/master/test). Vous trouverez à l'intérieur un test pour chaque application. Au debut du testxxx.py vous aurez les tests unitaires et ensuite les tests d'intégrations. Seuls les tests de validation se trouvent séparés car j'ai jugé qu'ils n'appartenait non pas à une seule mais à toutes les applications.

Remarque : django-nose est installé sur ce projet ce qui signifie que le niveau de couverture des tests sera consultable. J'ai volontairement laissé le dossier cover pour mon correcteur Openclassrooms.  -->

Pour lancer les tests, c'est très simple tapez : 

    $ python manage.py test #lance tous les tests (codés pour le moment)
    $ python manage.py test test.test_user #lance que les tests de l'app user  (codés pour le moment)
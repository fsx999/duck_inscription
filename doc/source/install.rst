============
Installation
============


Prérequis
---------

Il faut avoir fait l'install de django_apogee http://django-apogee.readthedocs.org/fr/latest/

Commandes
---------

#) Création du project et installation des librairies

    .. code-block:: bash

        cd ~/project
        git clone https://github.com/fsx999/duck_inscription.git
        cd duck_inscription
        source ~/.Envs/django_projet/bin/activate
        sudo apt-get install mercurial
        pip install -r requirement.txt
        pip install gunicorn


#) Configuration :

    .. code-block:: bash

        vim test_duck_inscription/local_settings.py


    ajout des variables de conf

    .. code-block:: python

        EMAIL_HOST = host.server.email
        EMAIL_USE_TLS = True # en cas de ssl, sinon False
        EMAIL_PORT = 2525 # port du serveur de mail
        EMAIL_HOST_USER = "utilisateur du compte"
        EMAIL_HOST_PASSWORD = "password"
        DEBUG = False # true si developpement
        ALLOWED_HOSTS =['inscription.mondomaine.fr'] # il faut ajoute le nom de domaine qui va être utiliser pour le site

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'ma_database',
                'USER': 'mon_utilisateur',
                'PASSWORD': 'mon_password',
                'HOST': 'url_base_de_donnee',
                'PORT': '',

            },
            'oracle': {  # Voir la configuration de django_apogee
                'ENGINE': 'django.db.backends.oracle',
                'NAME': 'nom_base_oracle',
                'USER': 'utilisateur_oracle',
                'PASSWORD': 'password',
                'HOST': 'host_oracle',
                'PORT': 'le_port',
            },
        }
        COMPOSANTE = '034'  # le code de la composante qui utilise l'application (code apogee)

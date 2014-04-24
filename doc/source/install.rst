============
Installation
============


Prérequis
---------

Il faut avoir fait l'install de django_apogee http://django-apogee.readthedocs.org/fr/latest/

Commandes
---------

#) Création du projet et installation des librairies

    .. code-block:: bash

        cd ~/projet
        git clone https://github.com/fsx999/duck_inscription.git
        cd duck_inscription
        source ~/.Envs/django_projet/bin/activate
        sudo apt-get install mercurial
        pip install -r requirement.txt
        pip install gunicorn
        sudo apt-get install supervisor nginx


#) Configuration :

    .. code-block:: bash

        vim test_duck_inscription/local_settings.py


    ajout des variables de conf

    .. code-block:: python

        # coding=utf-8
        EMAIL_HOST = 'host.server.email'
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

    application des migration

    .. code-block:: bash

        ./manage.py syncdb
        ./manage.py migrate

    initialisation de la base (différente de django_apogee)

    .. code-block:: bash

        ./manage.py initialisation_inscription
        ./manage.py shell_plus

    dans la console le code python suivant

    .. code-block:: python

         annee = SettingAnneeUni.objects.get(cod_anu=2014)  # changer par l'année en cours
         annee.inscription = True
         annee.save()


#) Configuration supervisor


    .. code-block:: bash

        mkdir ~/logs
        cd /etc/supervisor/conf.d
        sudo vim preins.conf


    Il faut remplasser tous les user par le bon user

    .. code-block:: bash

        [program:preins]
        command=/home/$user/.Envs/django_projet/bin/gunicorn -n gunicorn_preins -w 3 -t 30 -b unix:/tmp/gunicorn_preins.sock -p /tmp/gunicorn_preins.pid --log-level debug --error-logfile /home/$user/logs/error_gunicorn_preins.log --settings test_duck_inscription.settings test_duck_inscription.wsgi:application
        directory=/home/$user/projet/duck_inscription
        environment=PATH="/home/$user/.Envs/django_projet/bin"
        user=$user
        autostart=true
        autorestart=true
        redirect_stderr=true


    Ensuite il faut rajouter le chemin d'oracle dans le path (méthode a améliorer)

    .. code-block:: bash

        sudo vim /etc/init.d/supervisor

    ajouter au début du fichier juste après PATH=.....

    .. code-block:: bash

        export ORACLE_HOME=/opt/instantclient_11_2
        export LD_LIBRARY_PATH=:/opt/instantclient_11_2

    .. code-block:: bash

        sudo service supervisor restart

    configuration de nginx

    .. code-block:: bash
        mkdir ~/html
        mkdir ~/projet/static
        mkdir ~/projet/static_tel
        sudo vim /etc/nginx/sites-available/preins

    .. code-block:: bash

        upstream app_server {
            server unix:/tmp/gunicorn_preins.sock fail_timeout=0;
        }
        server {
            # pour https
            #ssl_certificate  wildcard-ssl.crt;
            #ssl_certificate_key  wildcard-ssl.key;

            #listen 443; # port 443 pour https, 80 pour http
            listen 80;
            server_name  localhost; #mettre le nom de domaine voulue

            #ssl  on;
            #ssl_session_timeout  5m;
            #ssl_protocols  SSLv3 TLSv1;
            #ssl_ciphers  ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv3:+EXP;
            #ssl_prefer_server_ciphers   on;

            root /home/$user/html;

            location /static/ {
                    # checks for static file, if not found proxy to app
                    autoindex on;
                    root /home/$user/projet/;
            }
            location /static_tel/ {
                    # checks for static file, if not found proxy to app
                    autoindex on;
                    root /home/$user/projet/;
            }
            location / {
                proxy_pass http://app_server;
                proxy_redirect     off;
                proxy_set_header   Host             $host;
                proxy_set_header   X-Real-IP        $remote_addr;
                proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Protocol "http"; # "https" si https
                #proxy_set_header X-Forwarded-Ssl on;
            }
        }


        ensuite

        .. code-block:: bash

            cd ../sites-enabled/
            sudo rm default
            sudo ln -s ../sites-available/preins preins
            sudo service nginx restart

        .. code-block:: bash

            source ~/.Envs/django_projet/bin/activate
            cd ~/projet/duck_inscription
            ./manage.py collectstatic




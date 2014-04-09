from distutils.core import setup

setup(name='duck_inscription', version='0.1', packages=['duck_inscription'], url='', license='',
      author='paul guichon', author_email='paul.guichon@iedparis8.net', description='',
      install_requires=['django',
                        'south',
                        'cx_Oracle',
                        'django_apogee',
                        'django-registration',
                        'django-simple-captcha',
                        'django-floppyforms',
                        'django_xworkflows',
                        'django-extra-views'])

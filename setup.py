from distutils.core import setup

setup(
    name='duck_inscription',
    version='0.1 beta',
    packages=['', 'duck_inscription', 'duck_inscription.urls', 'duck_inscription.admin', 'duck_inscription.forms',
              'duck_inscription.tests', 'duck_inscription.views', 'duck_inscription.adminx',
              'duck_inscription.adminx.html_string', 'duck_inscription.models', 'duck_inscription.managers',
              'duck_inscription.factories', 'duck_inscription.management', 'duck_inscription.management.commands',
              'duck_inscription.migrations', 'duck_inscription.templatetags'],
    url='https://github.com/fsx999/duck_inscription',
    license='MIT',
    author='paulguichon',
    author_email='paul.guichon@iedparis8.net',
    description=''
)

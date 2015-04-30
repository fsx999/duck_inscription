# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings
import django.utils.timezone
import django.core.validators
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        ('duck_utils', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_apogee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdresseIndividu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listed_number', models.CharField(max_length=15, verbose_name='Numero de tel\xe9phone :')),
                ('label_adr_1', models.CharField(max_length=32, verbose_name='Adresse :')),
                ('label_adr_2', models.CharField(max_length=32, null=True, verbose_name="Suite de l'adresse :", blank=True)),
                ('label_adr_3', models.CharField(max_length=32, null=True, verbose_name="Suite de l'adresse :", blank=True)),
                ('label_adr_etr', models.CharField(max_length=32, null=True, verbose_name='Code postal et ville \xe9trang\xe8re :', blank=True)),
                ('type', models.CharField(max_length=1, choices=[('1', 'OPI'), ('2', 'Fixe')])),
                ('code_pays', models.ForeignKey(verbose_name='Pays :', to='django_apogee.Pays')),
                ('com_bdi', models.ForeignKey(blank=True, to='django_apogee.ComBdi', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CentreGestionModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centre_gestion', models.CharField(max_length=3, verbose_name='')),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Centre de gestion',
                'verbose_name_plural': 'Centres de gestion',
            },
        ),
        migrations.CreateModel(
            name='CursusEtape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200, null=True, verbose_name='Label web')),
            ],
            options={
                'verbose_name': 'Cursus',
                'verbose_name_plural': 'Cursus',
            },
        ),
        migrations.CreateModel(
            name='DiplomeEtape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=120, null=True, verbose_name='Label web')),
                ('is_inscription_ouverte', models.BooleanField(default=True, verbose_name='ouverture campagne inscription')),
            ],
            options={
                'verbose_name': 'Dipl\xf4mes',
                'verbose_name_plural': 'Diplomes',
            },
        ),
        migrations.CreateModel(
            name='DossierInscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annee_premiere_inscription_p8', models.CharField(max_length=4, null=True, blank=True)),
                ('annee_premiere_inscription_enseignement_sup_fr', models.CharField(max_length=4, null=True)),
                ('annee_premiere_inscription_universite_fr', models.CharField(max_length=4, null=True, blank=True)),
                ('annee_bac', models.CharField(choices=[('1900', 1900), ('1901', 1901), ('1902', 1902), ('1903', 1903), ('1904', 1904), ('1905', 1905), ('1906', 1906), ('1907', 1907), ('1908', 1908), ('1909', 1909), ('1910', 1910), ('1911', 1911), ('1912', 1912), ('1913', 1913), ('1914', 1914), ('1915', 1915), ('1916', 1916), ('1917', 1917), ('1918', 1918), ('1919', 1919), ('1920', 1920), ('1921', 1921), ('1922', 1922), ('1923', 1923), ('1924', 1924), ('1925', 1925), ('1926', 1926), ('1927', 1927), ('1928', 1928), ('1929', 1929), ('1930', 1930), ('1931', 1931), ('1932', 1932), ('1933', 1933), ('1934', 1934), ('1935', 1935), ('1936', 1936), ('1937', 1937), ('1938', 1938), ('1939', 1939), ('1940', 1940), ('1941', 1941), ('1942', 1942), ('1943', 1943), ('1944', 1944), ('1945', 1945), ('1946', 1946), ('1947', 1947), ('1948', 1948), ('1949', 1949), ('1950', 1950), ('1951', 1951), ('1952', 1952), ('1953', 1953), ('1954', 1954), ('1955', 1955), ('1956', 1956), ('1957', 1957), ('1958', 1958), ('1959', 1959), ('1960', 1960), ('1961', 1961), ('1962', 1962), ('1963', 1963), ('1964', 1964), ('1965', 1965), ('1966', 1966), ('1967', 1967), ('1968', 1968), ('1969', 1969), ('1970', 1970), ('1971', 1971), ('1972', 1972), ('1973', 1973), ('1974', 1974), ('1975', 1975), ('1976', 1976), ('1977', 1977), ('1978', 1978), ('1979', 1979), ('1980', 1980), ('1981', 1981), ('1982', 1982), ('1983', 1983), ('1984', 1984), ('1985', 1985), ('1986', 1986), ('1987', 1987), ('1988', 1988), ('1989', 1989), ('1990', 1990), ('1991', 1991), ('1992', 1992), ('1993', 1993), ('1994', 1994), ('1995', 1995), ('1996', 1996), ('1997', 1997), ('1998', 1998), ('1999', 1999), ('2000', 2000), ('2001', 2001), ('2002', 2002), ('2003', 2003), ('2004', 2004), ('2005', 2005), ('2006', 2006), ('2007', 2007), ('2008', 2008), ('2009', 2009), ('2010', 2010), ('2011', 2011), ('2012', 2012), ('2013', 2013), ('2014', 2014), ('2015', 2015)], max_length=4, blank=True, help_text="Ann\xe9e d'obtention du baccalaur\xe9at ou \xe9quivalent", null=True, verbose_name="Ann\xe9e d'obtention")),
                ('annee_dernier_etablissement', models.CharField(max_length=4, null=True, blank=True)),
                ('annee_derniere_inscription_universite_hors_p8', models.CharField(max_length=4, null=True, blank=True)),
                ('annee_dernier_diplome', models.CharField(max_length=4, null=True)),
                ('autre_eta', models.NullBooleanField()),
                ('sportif_haut_niveau', models.BooleanField(default=False, verbose_name='sportif haut niveau')),
                ('etape', models.CharField(default='scolarite', max_length=20)),
                ('echelon', models.CharField(max_length=2, null=True, verbose_name='Echelon', blank=True)),
                ('num_boursier', models.CharField(max_length=13, null=True, verbose_name='N\xb0 de boursier', blank=True)),
                ('boursier_crous', models.NullBooleanField(default=None, verbose_name="Bousier du Crous de l'ann\xe9e pr\xe9c\xe9dente")),
                ('centre_payeur', models.CharField(blank=True, max_length=6, null=True, choices=[('LMDE', 'LMDE'), ('SMEREP', 'SMEREP')])),
                ('num_secu', models.CharField(max_length=15, null=True, blank=True)),
                ('affiliation_parent', models.ForeignKey(related_name='affiliation_parent_dossier', blank=True, to='django_apogee.RegimeParent', null=True)),
                ('autre_etablissement', models.ForeignKey(related_name='autre_etablissement', blank=True, to='django_apogee.Etablissement', null=True)),
                ('bac', models.ForeignKey(blank=True, to='django_apogee.BacOuxEqu', null=True)),
                ('cat_soc_autre_parent', models.ForeignKey(related_name='cat_soc_autre_parent', blank=True, to='django_apogee.CatSocPfl', null=True)),
                ('cat_soc_chef_famille', models.ForeignKey(related_name='cat_soc_chef_famille', to='django_apogee.CatSocPfl', null=True)),
                ('cat_soc_etu', models.ForeignKey(related_name='cat_soc_etu', to='django_apogee.CatSocPfl', null=True)),
                ('cat_travail', models.ForeignKey(blank=True, to='django_apogee.DomaineActPfl', null=True)),
                ('dernier_etablissement', models.ForeignKey(related_name='dernier_etablissement', to='django_apogee.Etablissement', null=True)),
                ('etablissement_annee_precedente', models.ForeignKey(related_name='etablissement_annee_precedente', to='django_apogee.Etablissement', null=True)),
                ('etablissement_bac', models.ForeignKey(related_name='etablissement_bac', to='django_apogee.Etablissement', null=True)),
                ('etablissement_dernier_diplome', models.ForeignKey(related_name='etablissement_dernier_diplome', to='django_apogee.Etablissement', null=True)),
            ],
            options={
                'verbose_name': "Dossier d'inscription",
                'verbose_name_plural': "Dossiers d'inscription",
            },
        ),
        migrations.CreateModel(
            name='Individu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', django_xworkflows.models.StateField(max_length=17, workflow=django_xworkflows.models._SerializedWorkflow(states=[b'first_connection', b'code_etu_manquant', b'individu', b'adresse', b'recap', b'accueil'], initial_state=b'first_connection', name=b'IndividuWorkflow'))),
                ('code_opi', models.IntegerField(unique=True, null=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Nom patronymique')),
                ('common_name', models.CharField(max_length=30, null=True, verbose_name="Nom d'\xe9poux", blank=True)),
                ('first_name1', models.CharField(max_length=30, verbose_name='Pr\xe9nom')),
                ('first_name2', models.CharField(max_length=30, null=True, verbose_name='Deuxi\xe8me pr\xe9nom', blank=True)),
                ('first_name3', models.CharField(max_length=30, null=True, verbose_name='Troisi\xe8me pr\xe9nom', blank=True)),
                ('student_code', models.IntegerField(default=None, null=True, verbose_name='Code \xe9tudiant', blank=True)),
                ('personal_email', models.EmailField(max_length=254, unique=True, null=True, verbose_name='Email')),
                ('personal_email_save', models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True)),
                ('date_registration_current_year', models.DateTimeField(auto_now_add=True)),
                ('sex', models.CharField(max_length=1, null=True, verbose_name='sexe', choices=[('M', 'Homme'), ('F', 'Femme')])),
                ('birthday', models.DateField(null=True, verbose_name='date de naissance')),
                ('town_birth', models.CharField(max_length=30, null=True, verbose_name='Ville naissance', blank=True)),
                ('valid_ine', models.CharField(default='O', max_length=1, null=None, verbose_name='Avez vous un num\xe9ro INE', choices=[('O', "J'ai un num\xe9ro INE"), ('N', "Je n'ai pas de num\xe9ro INE")])),
                ('ine', models.CharField(help_text='Obligatoire si vous en avez un', max_length=12, null=True, verbose_name='INE/BEA', blank=True)),
                ('annee_obtention', models.CharField(choices=[('1900', 1900), ('1901', 1901), ('1902', 1902), ('1903', 1903), ('1904', 1904), ('1905', 1905), ('1906', 1906), ('1907', 1907), ('1908', 1908), ('1909', 1909), ('1910', 1910), ('1911', 1911), ('1912', 1912), ('1913', 1913), ('1914', 1914), ('1915', 1915), ('1916', 1916), ('1917', 1917), ('1918', 1918), ('1919', 1919), ('1920', 1920), ('1921', 1921), ('1922', 1922), ('1923', 1923), ('1924', 1924), ('1925', 1925), ('1926', 1926), ('1927', 1927), ('1928', 1928), ('1929', 1929), ('1930', 1930), ('1931', 1931), ('1932', 1932), ('1933', 1933), ('1934', 1934), ('1935', 1935), ('1936', 1936), ('1937', 1937), ('1938', 1938), ('1939', 1939), ('1940', 1940), ('1941', 1941), ('1942', 1942), ('1943', 1943), ('1944', 1944), ('1945', 1945), ('1946', 1946), ('1947', 1947), ('1948', 1948), ('1949', 1949), ('1950', 1950), ('1951', 1951), ('1952', 1952), ('1953', 1953), ('1954', 1954), ('1955', 1955), ('1956', 1956), ('1957', 1957), ('1958', 1958), ('1959', 1959), ('1960', 1960), ('1961', 1961), ('1962', 1962), ('1963', 1963), ('1964', 1964), ('1965', 1965), ('1966', 1966), ('1967', 1967), ('1968', 1968), ('1969', 1969), ('1970', 1970), ('1971', 1971), ('1972', 1972), ('1973', 1973), ('1974', 1974), ('1975', 1975), ('1976', 1976), ('1977', 1977), ('1978', 1978), ('1979', 1979), ('1980', 1980), ('1981', 1981), ('1982', 1982), ('1983', 1983), ('1984', 1984), ('1985', 1985), ('1986', 1986), ('1987', 1987), ('1988', 1988), ('1989', 1989), ('1990', 1990), ('1991', 1991), ('1992', 1992), ('1993', 1993), ('1994', 1994), ('1995', 1995), ('1996', 1996), ('1997', 1997), ('1998', 1998), ('1999', 1999), ('2000', 2000), ('2001', 2001), ('2002', 2002), ('2003', 2003), ('2004', 2004), ('2005', 2005), ('2006', 2006), ('2007', 2007), ('2008', 2008), ('2009', 2009), ('2010', 2010), ('2011', 2011), ('2012', 2012), ('2013', 2013), ('2014', 2014), ('2015', 2015)], max_length=4, blank=True, help_text="Ann\xe9e d'obtention du baccalaur\xe9at ou \xe9quivalent", null=True, verbose_name="Ann\xe9e d'obtention")),
                ('opi_save', models.IntegerField(null=True, blank=True)),
                ('code_departement_birth', models.ForeignKey(verbose_name='D\xe9partement de naissance', blank=True, to='django_apogee.Departement', null=True)),
                ('code_pays_birth', models.ForeignKey(related_name='pays_naissance', default=None, verbose_name='Pays de naissance', to='django_apogee.Pays', null=True)),
                ('code_pays_nationality', models.ForeignKey(related_name='nationnalite', verbose_name='Nationnalit\xe9', to='django_apogee.Pays', null=True)),
                ('diplome_acces', models.ForeignKey(blank=True, to='django_apogee.BacOuxEqu', null=True)),
                ('family_status', models.ForeignKey(verbose_name='Status familial', to='django_apogee.SitFam', null=True)),
                ('situation_militaire', models.ForeignKey(verbose_name='Situation militaire', blank=True, to='django_apogee.SitMil', null=True)),
                ('type_handicap', models.ForeignKey(verbose_name='Handicap', blank=True, to='django_apogee.TypHandicap', null=True)),
                ('type_hebergement_annuel', models.ForeignKey(blank=True, to='django_apogee.TypHebergement', null=True)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(django_xworkflows.models.WorkflowEnabled, models.Model),
        ),
        migrations.CreateModel(
            name='IndividuTransitionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transition', models.CharField(max_length=255, verbose_name='transition', db_index=True)),
                ('from_state', models.CharField(max_length=255, verbose_name='from state', db_index=True)),
                ('to_state', models.CharField(max_length=255, verbose_name='to state', db_index=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='performed at', db_index=True)),
                ('individu', models.ForeignKey(related_name='etape_dossier', to='duck_inscription.Individu')),
            ],
        ),
        migrations.CreateModel(
            name='InscriptionUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('groups', models.ManyToManyField(related_query_name='user_inscription', related_name='user_inscription_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user_inscription', related_name='user_inscription_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'inscription_user',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ListeDiplomeAces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name="nom du diplome d'acces")),
            ],
            options={
                'db_table': 'pal_liste_diplome_aces',
                'verbose_name': "Liste des dipl\xf4mes d'acc\xe8s direct",
                'verbose_name_plural': "Liste des dipl\xf4mes d'acc\xe8s direct",
            },
        ),
        migrations.CreateModel(
            name='MoyenPaiementModel',
            fields=[
                ('type', models.CharField(max_length=3, serialize=False, verbose_name='type paiement', primary_key=True)),
                ('label', models.CharField(max_length=60, verbose_name='label')),
            ],
            options={
                'db_table': 'pal_moyen_paiement',
                'verbose_name': 'Moyen de paiement',
                'verbose_name_plural': 'Moyens de paiement',
            },
        ),
        migrations.CreateModel(
            name='NoteMasterModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moyenne_general', models.FloatField(null=True, blank=True)),
                ('note_memoire', models.FloatField(null=True, blank=True)),
                ('note_stage', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaiementAllModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nb_paiement_frais', models.IntegerField(default=1, verbose_name='Nombre de paiements pour les frais p\xe9dagogiques')),
                ('etape', models.CharField(default='droit_univ', max_length=20)),
                ('demi_annee', models.BooleanField(default=False)),
                ('moyen_paiement', models.ForeignKey(verbose_name='Votre moyen de paiement :', to='duck_inscription.MoyenPaiementModel', help_text='Veuillez choisir un moyen de paiement', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SettingAnneeUni',
            fields=[
                ('anneeuni_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_apogee.AnneeUni')),
                ('inscription', models.BooleanField(default=False)),
                ('transfert_pdf', models.FileField(null=True, upload_to='document_inscription', blank=True)),
                ('bourse_pdf', models.FileField(null=True, upload_to='document_inscription', blank=True)),
                ('pieces_pdf', models.FileField(null=True, upload_to='document_inscription', blank=True)),
                ('tarif_medical', models.FloatField(null=True, verbose_name='tarif medical', blank=True)),
                ('tarif_secu', models.FloatField(null=True, verbose_name='tarif secu', blank=True)),
            ],
            options={
                'verbose_name': 'Setting ann\xe9e universitaire',
                'verbose_name_plural': 'Settings ann\xe9e universitaire',
            },
            bases=('django_apogee.anneeuni',),
        ),
        migrations.CreateModel(
            name='SettingsEtape',
            fields=[
                ('etape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_apogee.Etape')),
                ('label', models.CharField(max_length=120, null=True, verbose_name='Label')),
                ('required_equivalence', models.BooleanField(default=True, verbose_name='Equivalence obligatoire')),
                ('is_inscription_ouverte', models.BooleanField(default=True, verbose_name='ouverture campagne inscription')),
                ('date_ouverture_equivalence', models.DateTimeField(null=True, blank=True)),
                ('date_fermeture_equivalence', models.DateTimeField(null=True, blank=True)),
                ('date_ouverture_candidature', models.DateTimeField(null=True, blank=True)),
                ('date_fermeture_candidature', models.DateTimeField(null=True, blank=True)),
                ('date_ouverture_inscription', models.DateTimeField(null=True, blank=True)),
                ('date_fermeture_inscription', models.DateTimeField(null=True, blank=True)),
                ('date_fermeture_reinscription', models.DateTimeField(null=True, blank=True)),
                ('label_formation', models.CharField(max_length=120, null=True, blank=True)),
                ('document_equivalence', models.FileField(upload_to='document_equivalence', null=True, verbose_name="Document d'\xe9quivalence", blank=True)),
                ('document_candidature', models.FileField(upload_to='document_candidature', null=True, verbose_name='Document de candidature', blank=True)),
                ('note_maste', models.BooleanField(default=False)),
                ('path_template_equivalence', models.CharField(max_length=1000, null=True, verbose_name='Path Template Equivalence', blank=True)),
                ('grille_de_equivalence', models.FileField(upload_to='grilles_evaluations', null=True, verbose_name='Grille evaluations', blank=True)),
                ('droit', models.FloatField(default=186, verbose_name='Droit')),
                ('frais', models.FloatField(default=1596, verbose_name='Frais')),
                ('nb_paiement', models.IntegerField(default=3, verbose_name='Nombre paiement')),
                ('demi_tarif', models.BooleanField(default=False, verbose_name='Demi tarif en cas de r\xe9ins')),
                ('semestre', models.BooleanField(default=False, verbose_name='Demie ann\xe9e')),
                ('limite_etu', models.IntegerField(null=True, verbose_name="Capacit\xe9 d'accueil", blank=True)),
                ('annee', models.ForeignKey(default=2014, to='duck_inscription.SettingAnneeUni')),
                ('cursus', models.ForeignKey(blank=True, to='duck_inscription.CursusEtape', null=True)),
                ('diplome', models.ForeignKey(blank=True, to='duck_inscription.DiplomeEtape', null=True)),
            ],
            options={
                'verbose_name': 'Settings Etape',
                'verbose_name_plural': 'Settings Etapes',
            },
            bases=('django_apogee.etape',),
        ),
        migrations.CreateModel(
            name='SettingsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etapes', models.ManyToManyField(related_name='etapes', to='duck_inscription.SettingsEtape')),
                ('property', models.ManyToManyField(to='duck_utils.Property', blank=True)),
                ('user', models.OneToOneField(related_name='setting_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StatModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equi_effectue', models.IntegerField(null=True)),
                ('equi_reception', models.IntegerField(null=True)),
                ('equi_refuse', models.IntegerField(null=True)),
                ('equi_traite', models.IntegerField(null=True)),
                ('candidature_effectue', models.IntegerField(null=True)),
                ('candidature_reception', models.IntegerField(null=True)),
                ('candidature_refuse', models.IntegerField(null=True)),
                ('candidature_accepte', models.IntegerField(null=True)),
                ('inscription_effectue', models.IntegerField(null=True)),
                ('inscription_reception', models.IntegerField(null=True)),
                ('inscription_incomplet', models.IntegerField(null=True)),
                ('inscription_complet', models.IntegerField(null=True)),
                ('inscription_opi', models.IntegerField(null=True)),
                ('inscription_attente', models.IntegerField(null=True)),
                ('cod_anu', models.ForeignKey(to='duck_inscription.SettingAnneeUni')),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
            options={
                'verbose_name': 'statistique',
                'verbose_name_plural': 'statistiques',
            },
        ),
        migrations.CreateModel(
            name='TypePaiementModel',
            fields=[
                ('type', models.CharField(max_length=5, serialize=False, verbose_name='type de frais', primary_key=True)),
                ('label', models.CharField(max_length=40, verbose_name='label')),
            ],
            options={
                'db_table': 'pal_type_paiement',
                'verbose_name': 'Type de paiement',
                'verbose_name_plural': 'Types de paiement',
            },
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('code_dossier', models.AutoField(serialize=False, verbose_name='code dossier', primary_key=True)),
                ('date', models.DateField(auto_now_add=True, verbose_name='La date du v\u0153ux')),
                ('valide', models.BooleanField(default=False)),
                ('is_reins', models.NullBooleanField(default=None)),
                ('is_auditeur', models.BooleanField(default=False)),
                ('date_validation', models.DateTimeField(null=True, blank=True)),
                ('state', django_xworkflows.models.StateField(max_length=25, workflow=django_xworkflows.models._SerializedWorkflow(states=[b'creation', b'ouverture_equivalence', b'liste_diplome', b'demande_equivalence', b'equivalence', b'liste_attente_equivalence', b'mis_liste_attente_equi', b'ouverture_candidature', b'note_master', b'candidature', b'liste_attente_candidature', b'mis_liste_attente_candi', b'ouverture_inscription', b'dossier_inscription', b'choix_ied_fp', b'droit_univ', b'inscription', b'liste_attente_inscription', b'auditeur', b'auditeur_traite'], initial_state=b'creation', name=b'WishWorkflow'))),
                ('suivi_dossier', django_xworkflows.models.StateField(max_length=21, workflow=django_xworkflows.models._SerializedWorkflow(states=[b'inactif', b'equivalence_reception', b'equivalence_complet', b'equivalence_incomplet', b'equivalence_traite', b'equivalence_refuse', b'candidature_reception', b'candidature_complet', b'candidature_incomplet', b'candidature_traite', b'candidature_refuse', b'inscription_reception', b'inscription_complet', b'inscription_incomplet', b'inscription_incom_r', b'inscription_traite', b'inscription_refuse', b'inscription_annule'], initial_state=b'inactif', name=b'SuiviDossierWorkflow'))),
                ('demi_annee', models.BooleanField(default=False, choices=[(True, '1'), (False, '0')])),
                ('is_ok', models.BooleanField(default=False)),
                ('date_liste_inscription', models.DateTimeField(null=True, blank=True)),
                ('annee', models.ForeignKey(db_column='annee', default=2014, to='duck_inscription.SettingAnneeUni')),
                ('centre_gestion', models.ForeignKey(blank=True, to='duck_inscription.CentreGestionModel', null=True)),
                ('diplome_acces', models.ForeignKey(related_name='diplome_acces', default=None, blank=True, to='duck_inscription.ListeDiplomeAces', null=True)),
                ('etape', models.ForeignKey(verbose_name='Etape', to='duck_inscription.SettingsEtape', null=True)),
                ('individu', models.ForeignKey(related_name='wishes', to='duck_inscription.Individu', null=True)),
            ],
            options={
                'verbose_name': 'Voeu',
                'verbose_name_plural': 'Voeux',
            },
            bases=(django_xworkflows.models.WorkflowEnabled, models.Model),
        ),
        migrations.CreateModel(
            name='WishParcourTransitionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transition', models.CharField(max_length=255, verbose_name='transition', db_index=True)),
                ('from_state', models.CharField(max_length=255, verbose_name='from state', db_index=True)),
                ('to_state', models.CharField(max_length=255, verbose_name='to state', db_index=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='performed at', db_index=True)),
                ('wish', models.ForeignKey(related_name='parcours_dossier', to='duck_inscription.Wish')),
            ],
        ),
        migrations.CreateModel(
            name='WishTransitionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transition', models.CharField(max_length=255, verbose_name='transition', db_index=True)),
                ('from_state', models.CharField(max_length=255, verbose_name='from state', db_index=True)),
                ('to_state', models.CharField(max_length=255, verbose_name='to state', db_index=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='performed at', db_index=True)),
                ('wish', models.ForeignKey(related_name='etape_dossier', to='duck_inscription.Wish')),
            ],
        ),
        migrations.AddField(
            model_name='paiementallmodel',
            name='wish',
            field=models.OneToOneField(to='duck_inscription.Wish'),
        ),
        migrations.AddField(
            model_name='notemastermodel',
            name='wish',
            field=models.OneToOneField(to='duck_inscription.Wish'),
        ),
        migrations.AddField(
            model_name='listediplomeaces',
            name='etape',
            field=models.ForeignKey(related_name='diplome_aces', to='duck_inscription.SettingsEtape', null=True),
        ),
        migrations.AddField(
            model_name='individu',
            name='user',
            field=models.OneToOneField(null=True, to='duck_inscription.InscriptionUser'),
        ),
        migrations.AddField(
            model_name='individu',
            name='year',
            field=models.ForeignKey(blank=True, to='django_apogee.AnneeUni', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='individu',
            field=models.OneToOneField(related_name='dossier_inscription', to='duck_inscription.Individu'),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='mention_bac',
            field=models.ForeignKey(to='django_apogee.MentionBac', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='non_affiliation',
            field=models.ForeignKey(related_name='non_affiliation_dossier', blank=True, to='django_apogee.MtfNonAflSso', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='premier_universite_fr',
            field=models.ForeignKey(related_name='premiere_universite_fr', default=None, blank=True, to='django_apogee.Etablissement', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='quotite_travail',
            field=models.ForeignKey(blank=True, to='django_apogee.QuotiteTra', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='sise_annee_precedente',
            field=models.ForeignKey(verbose_name='size_annee_precedente', to='django_apogee.SituationSise', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='situation_sociale',
            field=models.ForeignKey(related_name='situation_sociale_dossier', default='NO', blank=True, to='django_apogee.SitSociale', null=True),
        ),
        migrations.AddField(
            model_name='dossierinscription',
            name='type_dernier_diplome',
            field=models.ForeignKey(to='django_apogee.TypeDiplomeExt', null=True),
        ),
        migrations.AddField(
            model_name='adresseindividu',
            name='individu',
            field=models.ForeignKey(related_name='adresses', to='duck_inscription.Individu'),
        ),
    ]

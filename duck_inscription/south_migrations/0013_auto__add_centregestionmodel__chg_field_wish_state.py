# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CentreGestionModel'
        db.create_table(u'duck_inscription_centregestionmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centre_gestion', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'duck_inscription', ['CentreGestionModel'])


        # Changing field 'Wish.state'
        db.alter_column(u'duck_inscription_wish', 'state', self.gf(u'django_xworkflows.models.StateField')(max_length=25, workflow=__import__('xworkflows', globals(), locals()).base.WorkflowMeta('WishWorkflow', (), {'states': (('creation', 'creation'), ('ouverture_equivalence', 'ouverture_equivalence'), ('liste_diplome', 'liste_diplome'), ('demande_equivalence', 'demande_equivalence'), ('equivalence', 'equivalence'), ('liste_attente_equivalence', 'liste_attente_equivalence'), ('ouverture_candidature', 'ouverture_candidature'), ('note_master', 'note_master'), ('candidature', 'candidature'), ('liste_attente_candidature', 'liste_attente_candidature'), ('ouverture_inscription', 'ouverture_inscription'), ('dossier_inscription', 'dossier_inscription'), ('choix_ied_fp', 'choix_ied_fp')), 'initial_state': 'creation'})))

    def backwards(self, orm):
        # Deleting model 'CentreGestionModel'
        db.delete_table(u'duck_inscription_centregestionmodel')


        # Changing field 'Wish.state'
        db.alter_column(u'duck_inscription_wish', 'state', self.gf(u'django_xworkflows.models.StateField')(max_length=25, workflow=__import__('xworkflows', globals(), locals()).base.WorkflowMeta('WishWorkflow', (), {'states': (('creation', 'creation'), ('ouverture_equivalence', 'ouverture_equivalence'), ('liste_diplome', 'liste_diplome'), ('demande_equivalence', 'demande_equivalence'), ('equivalence', 'equivalence'), ('liste_attente_equivalence', 'liste_attente_equivalence'), ('ouverture_candidature', 'ouverture_candidature'), ('note_master', 'note_master'), ('candidature', 'candidature'), ('liste_attente_candidature', 'liste_attente_candidature'), ('ouverture_inscription', 'ouverture_inscription'), ('dossier_inscription', 'dossier_inscription')), 'initial_state': 'creation'})))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_apogee.anneeuni': {
            'Meta': {'ordering': "[u'-cod_anu']", 'object_name': 'AnneeUni', 'db_table': "u'ANNEE_UNI'"},
            'cod_anu': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True', 'db_column': "u'COD_ANU'"}),
            'eta_anu_iae': ('django.db.models.fields.CharField', [], {'default': "u'I'", 'max_length': '1', 'db_column': "u'ETA_ANU_IAE'"})
        },
        u'django_apogee.bacouxequ': {
            'Meta': {'object_name': 'BacOuxEqu', 'db_table': "u'BAC_OUX_EQU'"},
            'cod_bac': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True', 'db_column': "u'COD_BAC'"}),
            'cod_sis': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '1', 'to': u"orm['django_apogee.SituationSise']", 'null': 'True', 'db_column': "u'COD_SIS'"}),
            'cod_sis_bac': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_column': "u'COD_SIS_BAC'"}),
            'cod_tds': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_TDS'"}),
            'daa_deb_vld_bac': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_DEB_VLD_BAC'"}),
            'daa_fin_vld_bac': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_FIN_VLD_BAC'"}),
            'lib_bac': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "u'LIB_BAC'"}),
            'lic_bac': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_BAC'"}),
            'tem_deb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_DEB'"}),
            'tem_del': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_DEL'"}),
            'tem_en_sve_bac': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_BAC'"}),
            'tem_etb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_ETB'"}),
            'tem_mnb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_MNB'"}),
            'tem_nat_bac': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_NAT_BAC'"}),
            'tem_obt_tit_etb_sec': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_OBT_TIT_ETB_SEC'"}),
            'tem_type_equi': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '1', 'db_column': "u'TEM_TYPE_EQUI'"})
        },
        u'django_apogee.catsocpfl': {
            'Meta': {'object_name': 'CatSocPfl', 'db_table': "u'CAT_SOC_PFL'"},
            'cod_pcs': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_PCS'"}),
            'lib_pcs': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_PCS'"}),
            'lib_web_pcs': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_column': "u'LIB_WEB_PCS'"}),
            'tem_en_sve_pcs': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_PCS'"}),
            'tem_sai_qtr': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_SAI_QTR'"})
        },
        u'django_apogee.centregestion': {
            'Meta': {'object_name': 'CentreGestion', 'db_table': "u'CENTRE_GESTION'"},
            'cod_cge': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'COD_CGE'"}),
            'lib_cge': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "u'LIB_CGE'"})
        },
        u'django_apogee.combdi': {
            'Meta': {'ordering': "[u'lib_ach']", 'object_name': 'ComBdi', 'db_table': "u'COM_BDI_COPY'"},
            'cod_bdi': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_column': "u'COD_BDI'"}),
            'cod_com': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_column': "u'COD_COM'"}),
            'cod_fic_cbd': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'COD_FIC_CBD'"}),
            'eta_ptc_ach': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'ETA_PTC_ACH'"}),
            'eta_ptc_loc': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'ETA_PTC_LOC'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '13', 'primary_key': 'True'}),
            'lib_ach': ('django.db.models.fields.CharField', [], {'max_length': '26', 'db_column': "u'LIB_ACH'"}),
            'tem_en_sve_cbd': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'TEM_EN_SVE_CBD'"})
        },
        u'django_apogee.departement': {
            'Meta': {'ordering': "[u'lib_dep']", 'object_name': 'Departement', 'db_table': "u'DEPARTEMENT'"},
            'cod_acd': ('django.db.models.fields.IntegerField', [], {'db_column': "u'COD_ACD'"}),
            'cod_dep': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'COD_DEP'"}),
            'lib_dep': ('django.db.models.fields.CharField', [], {'max_length': '60', 'db_column': "u'LIB_DEP'"}),
            'lic_dep': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_DEP'"}),
            'tem_en_sve_dep': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_EN_SVE_DEP'"})
        },
        u'django_apogee.domaineactpfl': {
            'Meta': {'object_name': 'DomaineActPfl', 'db_table': "u'DOMAINE_ACT_PFL'"},
            'cod_dap': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_DAP'"}),
            'lib_web_dap': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'db_column': "u'LIB_WEB_DAP'"})
        },
        u'django_apogee.etablissement': {
            'Meta': {'ordering': "[u'lib_etb']", 'object_name': 'Etablissement', 'db_table': "u'ETABLISSEMENT'"},
            'cod_aff_dep_etb': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "u'COD_AFF_DEP_ETB'"}),
            'cod_aff_etb': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "u'COD_AFF_ETB'"}),
            'cod_dep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Departement']", 'db_column': "u'COD_DEP'"}),
            'cod_etb': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True', 'db_column': "u'COD_ETB'"}),
            'cod_pay_adr_etb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Pays']", 'null': 'True', 'db_column': "u'COD_PAY_ADR_ETB'"}),
            'cod_pos_adr_etb': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'db_column': "u'COD_POS_ADR_ETB'"}),
            'cod_tpe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.TypEtb']", 'db_column': "u'COD_TPE'"}),
            'lib_art_off_etb': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_column': "u'LIB_ART_OFF_ETB'"}),
            'lib_etb': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_ETB'"}),
            'lib_off_etb': ('django.db.models.fields.CharField', [], {'max_length': '60', 'db_column': "u'LIB_OFF_ETB'"}),
            'tem_aut_sis_etb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_AUT_SIS_ETB'"}),
            'tem_en_sve_etb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_ETB'"})
        },
        u'django_apogee.etape': {
            'Meta': {'object_name': 'Etape', 'db_table': "u'ETAPE'"},
            'cod_cur': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_CUR'"}),
            'cod_cyc': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_CYC'"}),
            'cod_etp': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "u'COD_ETP'"}),
            'lib_etp': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'db_column': "u'LIB_ETP'"})
        },
        u'django_apogee.mentionbac': {
            'Meta': {'object_name': 'MentionBac', 'db_table': "u'MENTION_NIV_BAC'"},
            'cod_mnb': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_MNB'"}),
            'lib_mnb': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_MNB'"}),
            'lic_mnb': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_MNB'"}),
            'tem_en_sve_mnb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_MNB'"})
        },
        u'django_apogee.mtfnonaflsso': {
            'Meta': {'object_name': 'MtfNonAflSso', 'db_table': "u'MTF_NON_AFL_SSO'"},
            'cod_mns': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_MNS'"}),
            'lib_mns': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "u'LIB_MNS'"}),
            'lic_mns': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'LIC_MNS'"}),
            'tem_del': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_DEL'"}),
            'tem_en_sve_mns': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_MNS'"})
        },
        u'django_apogee.pays': {
            'Meta': {'ordering': "[u'lic_pay']", 'object_name': 'Pays', 'db_table': "u'PAYS'"},
            'cod_pay': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'COD_PAY'"}),
            'cod_sis_pay': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'COD_SIS_PAY'"}),
            'lib_nat': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_NAT'"}),
            'lib_pay': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_PAY'"}),
            'lic_pay': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_PAY'"}),
            'tem_afl_dec_ind_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_AFL_DEC_IND_PAY'"}),
            'tem_del': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_DEL'"}),
            'tem_en_sve_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_EN_SVE_PAY'"}),
            'tem_ouv_drt_sso_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_OUV_DRT_SSO_PAY'"})
        },
        u'django_apogee.quotitetra': {
            'Meta': {'object_name': 'QuotiteTra', 'db_table': "u'QUOTITE_TRA'"},
            'cod_qtr': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_QTR'"}),
            'lib_qtr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_QTR'"}),
            'lib_web_qtr': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_column': "u'LIB_WEB_QTR'"}),
            'lic_qtr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIC_QTR'"}),
            'lim1_qtr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIM1_QTR'"}),
            'tem_cou_aut_reg_qtr': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_COU_AUT_REG_QTR'"}),
            'tem_en_sve_qtr': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_QTR'"})
        },
        u'django_apogee.regimeparent': {
            'Meta': {'object_name': 'RegimeParent', 'db_table': "u'REGIME_PARENT'"},
            'cod_rgp': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_RGP'"}),
            'lib_rgp': ('django.db.models.fields.CharField', [], {'max_length': '280', 'db_column': "u'LIB_RGP'"}),
            'ordre_tri_rgp': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'ORDRE_TRI_RGP'"})
        },
        u'django_apogee.sitfam': {
            'Meta': {'object_name': 'SitFam', 'db_table': "u'SIT_FAM'"},
            'cod_fam': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_FAM'"}),
            'cod_sis_fam': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_SIS_FAM'", 'blank': 'True'}),
            'lib_fam': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "u'LIB_FAM'"}),
            'lic_fam': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "u'LIC_FAM'"}),
            'tem_en_sve_fam': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_FAM'"})
        },
        u'django_apogee.sitmil': {
            'Meta': {'object_name': 'SitMil', 'db_table': "u'SIT_MIL'"},
            'cod_sim': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_SIM'"}),
            'lib_sim': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_SIM'"}),
            'lic_sim': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_SIM'"}),
            'tem_del_dip': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '1', 'db_column': "u'TEM_DEL_DIP'"}),
            'tem_en_sve_sim': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_SIM'"}),
            'tem_sai_dmm_lbt': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_SAI_DMM_LBT'"})
        },
        u'django_apogee.sitsociale': {
            'Meta': {'object_name': 'SitSociale', 'db_table': "u'SIT_SOCIALE'"},
            'cod_soc': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_SOC'"}),
            'lib_soc': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_column': "u'LIM1_SOC'"}),
            'lic_soc': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_column': "u'LIB_SOC'"}),
            'tem_del': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_DEL'"}),
            'tem_en_sve_soc': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_EN_SVE_SOC'"})
        },
        u'django_apogee.situationsise': {
            'Meta': {'object_name': 'SituationSise', 'db_table': "u'SITUATION_SISE'"},
            'cod_sis': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_SIS'"}),
            'lib_sis': ('django.db.models.fields.CharField', [], {'max_length': '130', 'db_column': "u'LIB_SIS'"}),
            'tem_en_sve_sis': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_SIS'"})
        },
        u'django_apogee.typediplomeext': {
            'Meta': {'object_name': 'TypeDiplomeExt', 'db_table': "u'TYP_DIPLOME_EXT'"},
            'cod_tde': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'COD_TDE'"}),
            'lib_tde': ('django.db.models.fields.CharField', [], {'max_length': '130', 'db_column': "u'LIB_TDE'"}),
            'lib_web_tde': ('django.db.models.fields.CharField', [], {'max_length': '130', 'db_column': "u'LIB_WEB_TDE'"}),
            'tem_en_sve_tde': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_TDE'"})
        },
        u'django_apogee.typetb': {
            'Meta': {'object_name': 'TypEtb', 'db_table': "u'TYP_ETB'"},
            'cod_sis_tpe': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'COD_SIS_TPE'"}),
            'cod_tpe': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_TPE'"}),
            'lib_tpe': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_TPE'"}),
            'lic_tpe': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_TPE'"}),
            'tem_det_tpe': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_DET_TPE'"}),
            'tem_en_sve_tpe': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_TPE'"}),
            'tem_ges_trf_tpe': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_GES_TRF_TPE'"}),
            'tem_prop_autre_etb': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '1', 'db_column': "u'TEM_PROP_AUTRE_ETB'"})
        },
        u'django_apogee.typhandicap': {
            'Meta': {'object_name': 'TypHandicap', 'db_table': "u'TYP_HANDICAP'"},
            'cod_thp': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "u'COD_THP'"}),
            'lib_thp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_THP'"}),
            'lic_thp': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_THP'"}),
            'tem_en_sve_thp': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_THP'"}),
            'tem_tie_tps': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_TIE_TPS'"})
        },
        u'django_apogee.typhebergement': {
            'Meta': {'object_name': 'TypHebergement', 'db_table': "u'TYP_HEBERGEMENT'"},
            'cod_thb': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True', 'db_column': "u'COD_THB'"}),
            'lib_thb': ('django.db.models.fields.CharField', [], {'max_length': '60', 'db_column': "u'LIB_THB'"}),
            'tem_en_sve_thb': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'db_column': "u'TEM_EN_SVE_THB'"})
        },
        u'duck_inscription.adresseindividu': {
            'Meta': {'object_name': 'AdresseIndividu'},
            'code_pays': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Pays']"}),
            'com_bdi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.ComBdi']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'adresses'", 'to': u"orm['duck_inscription.Individu']"}),
            'label_adr_1': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'label_adr_2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'label_adr_3': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'label_adr_etr': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'listed_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'duck_inscription.centregestionmodel': {
            'Meta': {'object_name': 'CentreGestionModel'},
            'centre_gestion': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'duck_inscription.cursusetape': {
            'Meta': {'object_name': 'CursusEtape'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        u'duck_inscription.diplomeetape': {
            'Meta': {'object_name': 'DiplomeEtape'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_inscription_ouverte': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'})
        },
        u'duck_inscription.dossierinscription': {
            'Meta': {'object_name': 'DossierInscription'},
            'affiliation_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'affiliation_parent_dossier'", 'null': 'True', 'to': u"orm['django_apogee.RegimeParent']"}),
            'annee_bac': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'annee_dernier_diplome': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'annee_dernier_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'annee_derniere_inscription_universite_hors_p8': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'annee_premiere_inscription_enseignement_sup_fr': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'annee_premiere_inscription_p8': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'annee_premiere_inscription_universite_fr': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'autre_eta': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'autre_etablissement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'autre_etablissement'", 'null': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'bac': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.BacOuxEqu']", 'null': 'True', 'blank': 'True'}),
            'boursier_crous': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'cat_soc_autre_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cat_soc_autre_parent'", 'null': 'True', 'to': u"orm['django_apogee.CatSocPfl']"}),
            'cat_soc_chef_famille': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cat_soc_chef_famille'", 'null': 'True', 'to': u"orm['django_apogee.CatSocPfl']"}),
            'cat_soc_etu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cat_soc_etu'", 'null': 'True', 'to': u"orm['django_apogee.CatSocPfl']"}),
            'cat_travail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.DomaineActPfl']", 'null': 'True', 'blank': 'True'}),
            'centre_payeur': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'dernier_etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'dernier_etablissement'", 'null': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'echelon': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'etablissement_annee_precedente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'etablissement_annee_precedente'", 'null': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'etablissement_bac': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'etablissement_bac'", 'null': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'etablissement_dernier_diplome': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'etablissement_dernier_diplome'", 'null': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'etape': ('django.db.models.fields.CharField', [], {'default': "u'scolarite'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individu': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'dossier_inscription'", 'unique': 'True', 'to': u"orm['duck_inscription.Individu']"}),
            'mention_bac': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.MentionBac']", 'null': 'True'}),
            'non_affiliation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'non_affiliation_dossier'", 'null': 'True', 'to': u"orm['django_apogee.MtfNonAflSso']"}),
            'num_boursier': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'num_secu': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'premier_universite_fr': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'premiere_universite_fr'", 'null': 'True', 'blank': 'True', 'to': u"orm['django_apogee.Etablissement']"}),
            'quotite_travail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.QuotiteTra']", 'null': 'True', 'blank': 'True'}),
            'sise_annee_precedente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.SituationSise']", 'null': 'True'}),
            'situation_sociale': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'NO'", 'related_name': "u'situation_sociale_dossier'", 'null': 'True', 'blank': 'True', 'to': u"orm['django_apogee.SitSociale']"}),
            'sportif_haut_niveau': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_dernier_diplome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.TypeDiplomeExt']", 'null': 'True'})
        },
        u'duck_inscription.individu': {
            'Meta': {'ordering': "[u'pk']", 'object_name': 'Individu'},
            'annee_obtention': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'code_departement_birth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Departement']", 'null': 'True', 'blank': 'True'}),
            'code_opi': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'code_pays_birth': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'pays_naissance'", 'null': 'True', 'to': u"orm['django_apogee.Pays']"}),
            'code_pays_nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'nationnalite'", 'null': 'True', 'to': u"orm['django_apogee.Pays']"}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'date_registration_current_year': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diplome_acces': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.BacOuxEqu']", 'null': 'True', 'blank': 'True'}),
            'family_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.SitFam']", 'null': 'True'}),
            'first_name1': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_name2': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'first_name3': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ine': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'opi_save': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'personal_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True'}),
            'personal_email_save': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'situation_militaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.SitMil']", 'null': 'True', 'blank': 'True'}),
            'state': (u'django_xworkflows.models.StateField', [], {'default': "u'first_connection'", 'max_length': '17', u'workflow': u"__import__('xworkflows', globals(), locals()).base.WorkflowMeta('IndividuWorkflow', (), {'states': (('first_connection', 'first_connection'), ('code_etu_manquant', 'code_etu_manquant'), ('individu', 'individu'), ('adresse', 'adresse'), ('recap', 'recap'), ('accueil', 'accueil')), 'initial_state': 'first_connection'})"}),
            'student_code': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'town_birth': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'type_handicap': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.TypHandicap']", 'null': 'True', 'blank': 'True'}),
            'type_hebergement_annuel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.TypHebergement']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'valid_ine': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'null': 'None'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.AnneeUni']", 'null': 'True', 'blank': 'True'})
        },
        'duck_inscription.listediplomeaces': {
            'Meta': {'object_name': 'ListeDiplomeAces', 'db_table': "u'pal_liste_diplome_aces'"},
            'etape': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'diplome_aces'", 'null': 'True', 'to': u"orm['duck_inscription.SettingsEtape']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'duck_inscription.notemastermodel': {
            'Meta': {'object_name': 'NoteMasterModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moyenne_general': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'note_memoire': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'note_stage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'wish': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['duck_inscription.Wish']", 'unique': 'True'})
        },
        u'duck_inscription.settinganneeuni': {
            'Meta': {'ordering': "[u'-cod_anu']", 'object_name': 'SettingAnneeUni', '_ormbases': [u'django_apogee.AnneeUni']},
            u'anneeuni_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_apogee.AnneeUni']", 'unique': 'True', 'primary_key': 'True'}),
            'inscription': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'duck_inscription.settingsetape': {
            'Meta': {'object_name': 'SettingsEtape', '_ormbases': [u'django_apogee.Etape']},
            'annee': ('django.db.models.fields.related.ForeignKey', [], {'default': '2014', 'to': u"orm['duck_inscription.SettingAnneeUni']"}),
            'cursus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duck_inscription.CursusEtape']", 'null': 'True', 'blank': 'True'}),
            'date_fermeture_candidature': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture_equivalence': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture_inscription': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture_reinscription': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture_candidature': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture_equivalence': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture_inscription': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'diplome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duck_inscription.DiplomeEtape']", 'null': 'True', 'blank': 'True'}),
            'document_candidature': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'document_equivalence': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'etape_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_apogee.Etape']", 'unique': 'True', 'primary_key': 'True'}),
            'grille_de_equivalence': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_inscription_ouverte': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'}),
            'label_formation': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'note_maste': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path_template_equivalence': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'required_equivalence': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'duck_inscription.settingsuser': {
            'Meta': {'object_name': 'SettingsUser'},
            'etapes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'etapes'", 'symmetrical': 'False', 'to': u"orm['duck_inscription.SettingsEtape']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'setting_user'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'duck_inscription.wish': {
            'Meta': {'object_name': 'Wish'},
            'annee': ('django.db.models.fields.related.ForeignKey', [], {'default': '2014', 'to': u"orm['duck_inscription.SettingAnneeUni']", 'db_column': "'annee'"}),
            'centre_gestion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.CentreGestion']", 'null': 'True', 'blank': 'True'}),
            'code_dossier': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_validation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'diplome_acces': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'diplome_acces'", 'null': 'True', 'blank': 'True', 'to': "orm['duck_inscription.ListeDiplomeAces']"}),
            'etape': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duck_inscription.SettingsEtape']", 'null': 'True'}),
            'individu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wishes'", 'null': 'True', 'to': u"orm['duck_inscription.Individu']"}),
            'is_reins': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'state': (u'django_xworkflows.models.StateField', [], {'default': "'creation'", 'max_length': '25', u'workflow': u"__import__('xworkflows', globals(), locals()).base.WorkflowMeta('WishWorkflow', (), {'states': (('creation', 'creation'), ('ouverture_equivalence', 'ouverture_equivalence'), ('liste_diplome', 'liste_diplome'), ('demande_equivalence', 'demande_equivalence'), ('equivalence', 'equivalence'), ('liste_attente_equivalence', 'liste_attente_equivalence'), ('ouverture_candidature', 'ouverture_candidature'), ('note_master', 'note_master'), ('candidature', 'candidature'), ('liste_attente_candidature', 'liste_attente_candidature'), ('ouverture_inscription', 'ouverture_inscription'), ('dossier_inscription', 'dossier_inscription'), ('choix_ied_fp', 'choix_ied_fp')), 'initial_state': 'creation'})"}),
            'suivi_dossier': (u'django_xworkflows.models.StateField', [], {'default': "'inactif'", 'max_length': '21', u'workflow': u"__import__('xworkflows', globals(), locals()).base.WorkflowMeta('SuiviDossierWorkflow', (), {'states': (('inactif', 'inactif'), ('equivalence_reception', 'equivalence_reception'), ('equivalence_complet', 'equivalence_complet'), ('equivalence_incomplet', 'equivalence_incomplet'), ('equivalence_traite', 'equivalence_traite'), ('equivalence_refuse', 'equivalence_refuse'), ('candidature_reception', 'candidature_reception'), ('candidature_complet', 'candidature_complet'), ('candidature_incomplet', 'candidature_incomplet'), ('candidature_traite', 'candidature_traite'), ('inscription_reception', 'inscription_reception'), ('inscription_complet', 'inscription_complet'), ('inscription_incomplet', 'inscription_incomplet'), ('inscription_traite', 'inscription_traite')), 'initial_state': 'inactif'})"}),
            'valide': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'duck_inscription.wishparcourtransitionlog': {
            'Meta': {'object_name': 'WishParcourTransitionLog'},
            'from_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'to_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'transition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'wish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parcours_dossier'", 'to': "orm['duck_inscription.Wish']"})
        },
        'duck_inscription.wishtransitionlog': {
            'Meta': {'object_name': 'WishTransitionLog'},
            'from_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'to_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'transition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'wish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'etape_dossier'", 'to': "orm['duck_inscription.Wish']"})
        }
    }

    complete_apps = ['duck_inscription']
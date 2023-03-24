# OSCAR

**Outil Servant à Comparer Automatiquement les Référentiels** (*Work in progress*)

## Objet

OSCAR est un projet d'outil en ligne de commande permettant de contrôler automatiquement l'alignement des référentiels
de structures et, à terme, de personnes, en contexte universitaire :

- Référentiels internes (LDAP...)
- Référentiels tiers : RNSR, AureHAL, Hceres, IdRef, ORCID...

Il s'agit de détecter tout écart entre les référentiels ne pouvant être synchronisés automatiquement afin d'en
  faciliter la correction par les services.

## Déploiement

Installation recommandée sous virtualenv. Nommez votre environnement à la fin de `venv/bin/activate` , sinon ce sera, par défaut, "development".

```shell
export ENV=staging
 ```
ou
```shell
export ENV=production
```
puis
```shell
source nom_du_virtualenv/bin/activate
```
Installez les dépendances :
```shell
 pip install -r requirements.txt
```
Des dépendances logicielles peuvent-être requises :
- Pour Selenium
```shell
apt-get install chromium-driver
```
- Pour python-ldap :
```shell
apt-get install build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind
```

Pour customiser les paramètres des modules, créez un fichier yml dédié à votre environnement. Par exemple, pour customiser les paramètres du module "Ldap" en environnement "production" :
```shell
cp mod_conf/ldap.yml mod_conf/production_ldap.yml
vim mod_conf/production_ldap.yml
```
La configuration de base (ici `mod_conf/ldap.yml`) sera alors ignorée.

## Validation de l'installation
Pour vérifier le bon fonctionnement
```shell
$ cd tests
$ pytest
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.9.2, pytest-7.2.1, pluggy-1.0.0
rootdir: /webhome/oscar/oscar, configfile: pytest.ini
collected 29 items                                                                                                                                                                                                

app/test_input_controller.py ....                                                                                                                                                                           [ 13%]
app/data/test_data_service.py ..                                                                                                                                                                            [ 20%]
app/data/test_entity_factory.py ...                                                                                                                                                                         [ 31%]
app/module_mgmt/module_factory_test.py ..                                                                                                                                                                   [ 37%]
app/module_mgmt/module_manager_test.py ....                                                                                                                                                                 [ 51%]
app/output/test_output_handler.py .                                                                                                                                                                         [ 55%]
modules/hal/test_hal_module.py .....                                                                                                                                                                        [ 72%]
modules/ldap/test_ldap_module.py .....                                                                                                                                                                      [ 89%]
modules/rnsr/test_rnsr_module.py ...                                                                                                                                                                        [100%]

=============================================================================================== 29 passed in 11.21s ===============================================================================================

```

## Utilisation

Déployé sur un serveur de l'université, OSCAR peut s'exécuter :

- En mode manuel, comme une application console, par les personnes ayant accès.
- En mode automatique, via une exécution périodique. Il enverra alors son rapport par mail sous forme de fichier de
  tableur.

### Mode manuel
```shell
python src/main.py --manual
```
```
$ python src/main.py --manual
→ Fichier d'initialisation découvert : mod_conf/hal.yml
      ＊ Module : hal initialisé avec succès
→ Fichier d'initialisation découvert : mod_conf/rnsr.yml
      ＊ Module : rnsr initialisé avec succès
→ Fichier d'initialisation découvert : mod_conf/production.ldap.yml
      ＊ Module : ldap initialisé avec succès
Initialisation : hal **  rnsr **  ldap
Initialisation 100.0% [=====================================================================================================================================================================>]   3/  3 eta [00:00]
A pour acronyme, R pour id rnsr, Q pour quitter =, valeur > A=LAMOP
⚙ Contrôle d'alignement d'entité : critère [acronym]=[LAMOP]
ldap
Initialisation 100.0% [=====================================================================================================================================================================>]   3/  3 eta [00:00]
Champ : Directeur-directrice
hal : None
rnsr : None
ldap : None
Champ : Adresse email Directeur-directrice
hal : None
rnsr : None
ldap : None
Champ : Nom
hal : Laboratoire de Médiévistique Occidentale de Paris
rnsr : Laboratoire de Médiévistique Occidentale de Paris 
ldap : Laboratoire de médiévistique occidentale de Paris
Champ : Acronym
hal : LAMOP
rnsr : LAMOP 
ldap : LAMOP
Champ : Adresse
hal : - Université Paris 1 Panthéon-Sorbonne - Centre Sorbonne - 17 rue de la Sorbonne 75005 Paris - CNRS LAMOP Campus Condorcet, Bat. Nord 14 rue des Humanités 93322 Aubervilliers cedex.
rnsr : Centre Sorbonne, 17 rue de la Sorbonne 75005 PARIS 
ldap : Sorbonne
17 RUE DE LA SORBONNE
75005 PARIS
France
Champ : Identifiant RNSR
hal : 199812917D
rnsr : 199812917D
ldap : None
Champ : Site web
hal : https://lamop.pantheonsorbonne.fr/
rnsr : None
ldap : http://lamop.univ-paris1.fr
Champ : Numéro
hal : UMR8589
rnsr : None
ldap : UMR 8589
A pour acronyme, R pour id rnsr, Q pour quitter =, valeur >
 
```

## Licence


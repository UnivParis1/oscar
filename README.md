# OSCAR

**Outil Servant à Comparer Automatiquement les Référentiels** (*Work in progress*)

## Objet

OSCAR est un projet d'outil en ligne de commande permettant de contrôler automatiquement l'alignement des référentiels
de structures et, à terme, de personnes, en contexte universitaire :

- Référentiels internes (LDAP...)
- Référentiels tiers : RNSR, AureHAL, Hceres, IdRef, ORCID...

Il s'agit de détecter tout écart entre les référentiels ne pouvant être synchronisés automatiquement afin d'en
  faciliter la correction par les services.

## Utilisation

Déployé sur un serveur de l'université, OSCAR peut s'exécuter :

- En mode manuel, comme une application console, par les personnes ayant accès.
- En mode automatique, via une exécution périodique. Il enverra alors son rapport par mail sous forme de fichier de
  tableur.

## Licence


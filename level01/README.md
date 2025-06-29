# level01

Le fichier passwd dans /etc contient les informations de base sur les comptes utilisateurs du système. 
Avant les mdp était stocké directement à cet endroit comme on peut le voir dans la [linuxdoc](https://www.linuxdoc.org/HOWTO/Security-HOWTO-6.html)


```bash
cat /etc/passwd
```
output:
```bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

john est une commande qui essaie de retrouver un mot de passe à partir de son hash par bruteforce ou dictionnaire.
J'install john-jumbo latest version et je met le mot de passe dans un fichier

```bash
./john file
```
output
```
Using default input encoding: UTF-8
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
Cracked 1 password hash (is in ./john.pot), use "--show"
No password hashes left to crack (see FAQ)
```

```bash
./john file --show
```
output:
```
?:abcdefg

1 password hash cracked, 0 left
```

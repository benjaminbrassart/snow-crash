# level00

Our target user is `flag00`. Let's start with some basic scouting commands:

```sh
# Inspect level00's home
ls -lA # nothing useful

# Inspect flag00's home
ls -lA "$(getent passwd flag00 | cut -d ':' -f 6)" # permission denied

# Find files that belong to level00
find / -user level00 2>/dev/null # nothing relevant

# Find files that are readable by level00
find / -readable 2>/dev/null # too many results

# Find files that belong to flag00
find / -user flag00 2>/dev/null # interesting...
```

With the last command, we get two files:

```
/usr/sbin/john
/rofs/usr/sbin/john
```

It contains the following string: `cdiiddwpgswtgt`.
We can try this as the password for `flag00`.

```
flag00@localhost's password: cdiiddwpgswtgt
Permission denied, please try again.
```

Unfortunately this is not the password.
Let's keep digging.

`cdiiddwpgswtgt` contains only lowercase letters, so it could be encrypted using a [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher). There are tools to brute-force this kind of encryption like [dcode.fr](https://www.dcode.fr/caesar-cipher). Commands like `tr` also allow this kind of decryption.

If we run the script `resources/bruteforce.py` with `cdiiddwpgswtgt` as argument, we get the following output:

```
 1 -> dejjeexqhtxuhu
 2 -> efkkffyriuyviv
 3 -> fgllggzsjvzwjw
 4 -> ghmmhhatkwaxkx
 5 -> hinniibulxbyly
 6 -> ijoojjcvmyczmz
 7 -> jkppkkdwnzdana
 8 -> klqqllexoaebob
 9 -> lmrrmmfypbfcpc
10 -> mnssnngzqcgdqd
11 -> nottoohardhere
12 -> opuuppibseifsf
13 -> pqvvqqjctfjgtg
14 -> qrwwrrkdugkhuh
15 -> rsxxsslevhlivi
16 -> styyttmfwimjwj
17 -> tuzzuungxjnkxk
18 -> uvaavvohykolyl
19 -> vwbbwwpizlpmzm
20 -> wxccxxqjamqnan
21 -> xyddyyrkbnrobo
22 -> yzeezzslcospcp
23 -> zaffaatmdptqdq
24 -> abggbbunequrer
25 -> bchhccvofrvsfs
```

One line stands out: `11 -> nottoohardhere`. We can try this as password.

```
flag00@localhost's password: nottoohardhere
Don't forget to launch getflag !
```

It worked! `getflag` prints `x24ti5gi3x0ol2eh4esiuxias`. That's (supposedly) our password for user `level01`.

```
level01@localhost's password: x24ti5gi3x0ol2eh4esiuxias
```

It also worked. Noice.

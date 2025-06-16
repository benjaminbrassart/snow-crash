# level01

Our target user is `flag01`. Let's start with some basic scouting commands:

```sh
# Inspect level01's home
ls -lA # nothing useful

# Inspect flag01's home
ls -lA "$(getent passwd flag01 | cut -d ':' -f 6)" # permission denied

# Find files that belong to level01
find / -user level01 2>/dev/null # nothing relevant

# Find files that are readable by level01
find / -readable 2>/dev/null # too many results

# Find files that belong to flag01
find / -user flag01 2>/dev/null # nothing
```

Nothing like the previous level. After looking a bit on the Internet, it appears that looking at the user database can be useful in security challenges.

```sh
cat /etc/passwd
```

This has a lot of users. We could try to `grep` what we want, but the `getent` is the preferred tool for interacting with the user database.

```sh
getent passwd flag01
```

This is the output:

```
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

The user database follows a specific format. Each line is an entry. Each entry's field is separated with a colon `:`. Here are the fields:

1. Username
2. Password, either:
    * An encrypted password
    * `x` if the password is in `/etc/shadow`
    * An asterisk `*` if the account is disabled
3. UID
4. Primary GID
5. Gecos ([Wikipedia](https://en.wikipedia.org/wiki/Gecos_field))
6. Home directory
7. Shell

The entry for `flag01` contains an encrypted password. According to the [Linux documentation](https://www.linuxdoc.org/HOWTO/Security-HOWTO-6.html), passwords are encrypted using a one-way DES algorithm. It also mentions [John the Ripper](https://www.openwall.com/john/doc/OPTIONS.shtml) (chapter [6.9 "Crack" and "John the Ripper"](https://www.linuxdoc.org/HOWTO/Security-HOWTO-6.html#crack)).

After pulling `/etc/passwd` from the target:

```sh
john passwd
john passwd --show
```

The last command outputs this:

```
flag01:abcdefg:3001:3001::/home/flag/flag01:/bin/bash

1 password hash cracked, 0 left
```

`abcdefg` appears to be is the password for `flag01`. Let's try.

```
flag01@localhost's password: abcdef
Don't forget to launch getflag !
```

Awesome. `getflag` prints `f2av5il02puano7naaf6adaaf`. As for the previous level, this is the password for the next level.

```
level02@localhost's password: f2av5il02puano7naaf6adaaf
```

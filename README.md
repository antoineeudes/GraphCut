# Installation
```
brew install socat
brew install xquartz
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"
```

In another terminal, run : 
```
open -a Xquartz
```

Go to XQuartz Preferences > Security and check on `Allow connections from network clients`

Run :
```
ifconfig en0
```

the result should look like : 

```
en0: 
…
inet XXX.XXX.X.XXX netmask 0xffffff00 broadcast 192.168.199.255
…
```

Then run 
```
docker run --rm -it \
   -e DISPLAY=XXX.XXX.X.XXX:0 \
   --workdir=/code \
   --volume="/path/to/this/repo:/code" \
   --volume="/etc/group:/etc/group:ro" \
   --volume="/etc/passwd:/etc/passwd:ro" \
   --volume="/etc/shadow:/etc/shadow:ro" \
   --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
   graphcut:latest /bin/bash
```

# Usage
In the container, run

```
python mincut_init.py
```

Here you go!


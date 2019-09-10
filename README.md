This is a little plugin for [qutebrowser](https://github.com/qutebrowser/qutebrowser)

It adds a `shell-send` command to qutebrowser that sends currently selected text to a shell process  
It will execute `x-terminal-emulator-exe "<args> ; $SHELL"`  

# HOWTO

`lib.py` file is intended to be imported to `config.py` file of qutebrowser's `basedir`/config folder

Example config.py:

```
# user's config

from importlib.machinery import SourceFileLoader
from os import path

SourceFileLoader('send-shell-plugin', path.expanduser('~/devel/qutebrowser-send-shell/lib.py')).load_module()
```


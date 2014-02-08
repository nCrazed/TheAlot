TheAlot
=======

Lightweight python IRC Bot

Requirements:

* [python3.3](http://python.org/download/releases/3.3.3/) (not tested with older version)
* [virtualenv](http://www.virtualenv.org) (optional)
* [irc](https://pypi.python.org/pypi/irc)
* [sqlalchemy](http://www.sqlalchemy.org/)

Installation
------------

1. Install and source the virtualenv:
```bash
virtualenv3 VENV
source VENV/bin/activate
```

2. Install the package
```bash
pip install thealot
```

Configuration
-------------

1. Copy the default config file:
```bash
cp VENV/lib/python<VERSION>/site-packages/thealot/config.json .
```

2. Edit configuration to fit your needs:

### server
> IRC server address that bot should connect to

### port
> Port that the bot should use to connect to the server

### channel
> IRC channel that the bot should join after connecting to the server

### nickname
> Nickname that the bot should attempt to use (if it's taken and underscore is appended until available nickname is found.

### prefix
> Prefix to be used to invoke bot commands

### database
> Database URL string acceptable by [sqlalchemy.create_engine()](http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlalchemy.create_engine) to be used by the bot and plugins.

### plugins
> a comma separated list of plugin module names to be loaded when bot is started.
> Example: To run the [AlotPlugin](https://github.com/nCrazed/AlotPlugin) install `thealot-alot` package with:
```bash
pip install thealot-alot
```
and enable the plugin in the config:
```json
"plgins" : [
    "alot"
]
```

## Running

1. Source the virtualenv:
```bash
source VENV/bin/activate
```

2. Instantiate and run the bot:
```python
from thealot import TheAlot

if __name__ == "__main__":
    bot = TheAlot()
    bor.start()
```

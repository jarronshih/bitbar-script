# 1point3acres profile
The main program is `1p3a.py`. It supports auto sign-on and auto day question.

## Getting start
- Install dependency from `Pipfile.lock`
- Setup cookies in `local_settings.py`
- Run `1p3a.py`


## Detail setup
### Install env
I use pipenv to setup env.

```bash
brew install pipenv
pipenv install
```


### Configure cookie
Create file `local_settings.py` and add `username` and `raw_cookies` inside.

```python
# local_settings.py
username = 'username'
raw_cookies = '''
<copy cookie from browser after login>
'''
```


### Configure the refresh time
The refresh time is in the filename of the plugin, following this format: `{name}.{time}.{ext}`

```bash
ln -s <folder>/1point3acres/run.sh 1p3a.24h.sh
```

### Ensure you have execution rights
Ensure the plugin is executable by running `chmod +x 1p3a.24h.sh`.

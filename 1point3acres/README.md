

## Configure the cred
Create file `local_settings.py` and add `username` and `raw_cookies` inside.

```python
username = 'boo'
raw_cookies = '''
copy from browser after login
'''
```


## Configure the refresh time
The refresh time is in the filename of the plugin, following this format: `{name}.{time}.{ext}`

```bash
ln -s <folder>/1point3acres/1p3a.py 1p3a.24h.py
```

## Ensure you have execution rights
Ensure the plugin is executable by running `chmod +x 1p3a.24h.py`.

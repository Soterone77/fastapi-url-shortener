# FastAPI URL Shortener

## Develop

### Setup:

Right click 'url-shortener'  -> Mark directory as -> Sources Root

### Run

Go to the workdir:
```shell
cd url-shortener
```
Run dev server
```shell
uv fastapi dev
```

### Snipets
```shell
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```
# setup

```bash
   python -m venv myenv
```
## Quick start link with
https://flask.palletsprojects.com/en/3.0.x/quickstart/
## Activate
```
./myenv/Scripts/Activate.ps1
```
## virtual ENV
```sh
 git init
```
## Git

### initalizing the project
```sh
 git init
```

### Git ignore
 Add `.gitignore`


## Create a repo in github
1. stage files -> `git add .`
2. commit -> `commit -m "commit message"`
3. push to github

## installing flask
make sure your myenv is activated
```pip install Flask```

## How to run Flask
```flask --app main run```
>only if the file is app.py ```flask run```

> for development perposes 
```
flask run ---debug
```



# Why Flask?
1. improves your DX
2. micro framework
3. Ready made tools to implemented the API (CRUD)
4. lightweight

# Django vs Flask
- django has full operations already in-buit, no freedom to edit the methods
- Flask allows you to choose libraries and partially implemented

# Rest API
- uses http request to access and use data
- you should have 
    - get (Read)
    - post (Create)
    - put (Update)
    - delete (Delete)
- it converts the get request to the sql query and s
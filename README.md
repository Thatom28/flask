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

## stashing changes
```
git add.
git stash apply  # applys the changes
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

> for development purposes 
> if you dont want to restart the server the whole time
```
flask run ---debug
```

## Take snapshot of packages installed and what their dependencies are
## The package that your app depends on
```sh
    pip freeze > requirements.txt
 ```

 ## install all dependencies and dependencies
 ```sh
  pip install -r requirements.txt
```
> is useful for documentation purposes

the drive that is used to connect with the database that translates between raw and sqlachemy
```
pip install pyodbc
```

# connection to database
```
pip install SQLAlchemy
pip install flask_sqlalchemy
```

env- to hide the url, allows you to inherit

uuid - randow generation od pk
# Why Flask?
1. improves your DX
2. micro framework
3. Ready made tools to implemented the API (CRUD)
4. lightweight
5. gives ready made tools to implement REST API
6. has templates(can build templates)
7. blue prints to organise things
8. 

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
"""
1. create virtual environment
python3 -m venv .venv

2. select interpretor
        1. ctrl + shift + p
        2. type select interpretor
        3. choose venv .venv interpretor
        4. restart terminal - kill and open new
        5. open new terminal using command - ctrl + j
        6. terminal looks like - (.venv) saravananma@SOLVERLAPT564:~/Home Files/Flask 2024/REST_API$

3. install  requirements
        1. pip install flask
                flask
                flask-smorest
                python-dotenv
                1.flask just installed inside venv

4.  create app.py
        1. write 'flask run' in .venv terminal

5. what is JSON
        1. REST Apis usually work with JSON
        2. It follows a specific format
        3. It is a string and in key-value pair format
        4. why stringify, it uses less bytes and than other format
        5. easy to transfer in less bandwidth to client from server

6. 200 - OK, 201 - Created successfully, 404

7. What is Docker Container?
        - docker
        - docker build -t rest-apis-flask-python . (. - where is the dockerfile location - it is in the current directory)
        - run docker through terminal
                docker run -p 5005:5000 rest-apis-flask-python

        - docker compose up

8. requirements.txt
        sqlalchemy
        flask-sqlalchemy
        pip install -r requirements.txt

9. flask-smorest
        - used to handle error messsage (abort(404, message='Store not found')), retrun no need

10. run docker
        - docker build -t flask-smorest-api .
        - docker run -dp 5000:5000 flask-smorest-api
        -[ docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api ]  -> it helps to move new code to docker container

11. Blueprint from flask_smorest
        - it is used to divide api into multiple segments
        - reduce writing path in each api
        - reduce providing name to each function
        - need to import it in app.py - register this blueprint in app.py
        - add configurations
12. Add swagger api

13. marshmallow schemas for api
        - define item data strucute, it is same as interface
        - define store data structure
        - it is used to reduce if conditions for payload validation
        - incoming data is validated here
        - we can if conditions from each functions
        - it will check only incoming data
        - it provide validated data to functions, just put item_data after self
        - remove - item_data = request.get_json()
        - item_data must be placed after self
        - implement schema only on the function which receive data from client
        - in swagger - example value schema is shown due implementation of this marshmallow
        - @blp.response(200, itemSchema) must be keep always at last in all fuctions
        - dictionary into json changed by marshmallow
        - for delete api - we dont need to apply blp.response, because it just sending the message

14. sqlalchemy
        - SQLAlchemy() object
        - link SQLAlchemy() to flash app first
        - one to many relationship
                - every item is associated with one store
                - one store is associated with many item
        - foriegn key, why it is used ? - when we create an item, we use storeid, storeid must be a valide one, else item will not be created
        - how to check the store id is valid one, by making the store id as foreign key

15. __init__
        - it helps use to import models to other files easily

16. create_app()
        define function, whose job is to call flask app

17. configure DB connection
        create db connection inside flask app

18. create with app.app_context(): function


19. re-build docker container
        - docker build -t flask-smorest-api .
        - docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api


20. Refresh Token
        Creation of a Refresh Token:
        The refresh token is used to generate a new access token.
        Usage of a Refresh Token:
        When logging in with credentials, both an access token and a refresh token are generated.
        When the access token expires, the refresh token can be used to create a new access token.
        Using the /refresh API, we can obtain a new access token, but it is not considered a fresh token.
        To receive a fresh token, the refresh token must be included in the headers of the request.


21. database migration
        - flask db init - this command used to interact with alembic
        - it will create migration folder
        - verison folder - this folder is used to store all the database changes
        - alembic.ini - this file is used to configure alembic
        - flask db migrate - this command is used to create a migration file
        - add some columns in models then do flask db migrate, inside version folder, it will create a migration file
        - flask db upgrade - this command is used to upgrade the database
        - mention length in db.String(100), when adding the column description = db.Column(db.String(100))
        - flask db downgrade - this command is used to downgrade the database
        - manualy modify the migration file
                - there is som problem in row which has default values, it will not work
        - flask db revision --autogenerate - this command is used to create a migration file
        
22. git repositories
        - git init
        - git commit
        - git push
        - git pull
        - git clone
        - git checkout --myfile.py
        - git reset HEAD myfile.py
        - git reset COOMIT_ID - it tells git to get rid of the changes in the commit and deletes it
        - git revert COOMIT_ID - it will create a new commit with the opposite changes of another commit
                                - if you revert a commit, you can revert the revert later.
                                - It is safer to revert a commit than to reset it.
                                - Also, if you share a remote repository with others, you can revert a commit without affecting them, but resetting can cause problems.
                                
                                
        folow below steps to create a new branch
        - git init - it creates a .git folder
        - ls - a - used to view all the files and folders in the current directory
        - git status - it tells the status of the files in the current directory
        
        - create another file called .gitignore
        - git add . - it adds all the files in the current directory to the staging area
        
        
        how to remove staged files from the staging area
        - git rm --cached schemas.py - it removes the file from the staging area
        - git add schemas.py - it adds the file back to the staging area
        - git commit - m "message" - it commits the changes to the local repository
        - git push -u origin main - it pushes the changes to the remote repository
        
        - git checkout -- app.py - it restores the file to the previous version
                        or
        - git restore -- app.py - it restores the file to the previous version
        
        - git reset HEAD app.py - it just removes the file from the staging area and removes all the changes
        
        learn about
        - git commit -a
        - git commit -m message
        - git commit -am 
        
        git commit -m message "docs(readme): update readme"
        
        
        markdown file .md files styling the text
        1.      # biggest title
                ## second biggest title
                ### third biggest title
                
        2. ```
                message
           ```
        
        3. > 
                > message
                
        4. _italic_ - for italic text
         
        5. **bold** - for bold text
        
        6. `code` - for inline code
        
        7. [This is a link](https://www.google.com) - for link

        8. image link - ![alt text](image link)



23. .flake8 file
        - it is used to configure the flake8
        
24. official git repository of techlado is techladocode 
"""

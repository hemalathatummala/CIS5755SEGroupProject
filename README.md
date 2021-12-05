# CIS5775SEGroupProject
### Group Members
Hemalatha Tummala , Divya Nuthalapati
### GitHub url
https://github.com/hemalathatummala/CIS5755SEGroupProject.git
### Project Introduction
we are designing fast session store for online applications by referring https://aws.amazon.com/getting-started/hands-on/building-fast-session-caching-with-amazon-elasticache-for-redis/. Our application will have login page where user will be asking for his email and upon successful login we will show number of times user has logged into particular
application. In this application, we have consider ttl for email as 30 secs which means within 30 seconds if user logged in multiple times we will be capturing each successful login and showing it as number of Visits for application.

### Activities done by the Group
### Initial design plan: (1 hr)
We initially discussed about session caching, how we can use redis and flask to achieve this task . We thought of implementing our application using AWS cloud platform by following the tutorial. 
To design this application we have choosed python Flask framework , Amazon elasticache for redis as a distributed cache for session management,Amazon cloud9 as IDE and github as code management tool.

### Our approach to design Application(5hrs) : 

Our primary requirement for this application is designing a login page which will ask user to enter his email address and upon successful login we want to show his visting information(number of times he has accessed particualr application within specifc time)

During development of our application we have followed AWS hands on approach to build fast session store for online applications , understand and did below steps.

step1: First we have created redis cluster using elasticache aws service , given default configurations like name, 0 nodes etc. After successful creation of redis cluster we have copied the primary end point url and tested whether redis is accessible or not using redis-cli.

step2: We have implemented small application using flask (a micro framework for web development in python) .In this step we have included login, logout functionalities for our application, also checking whether user email exists in session or not as root action

step3: We have configured redis url , tried running application from command line. We have previewed our application and validated the application.

step4: As we have integrated cloud9 with github, we have pushed all our changes to github repository. 

### Major Steps: 
1. We logged in to github and created public repository CIS5755SEGroupProject by including git ignore file for python,readme.md file and MIT license.
2. We created personal access token by going to : account profile --> settings -->Developer Settings -->Personal Access Tokens (gave appropriate name, expiration date along with scope) and noted it down for future reference.
3. We created cloud9 environment and delete readme.md file
4. We executed following command from cloud9 command terminal to store git credentials for future purposes: git config --global credential.helper store 
5. We then go to github and copied the repository url 
6. We cloned the git repository by using following command : git clone <repository-url> (we entered our git hub username and token (in place of password))
7. After cloning the repository, we changed the directory to CIS5755SEGroupProject
8. We have created project directory by following command : mkdir SessionCaching
9. We then changed to project directory and started setting up the python environment by executing below commands.
        1. for creating environment we executed "python3 -m venv env" 
        2. to activate python environment we executed "source env/bin/activate"
10. Meanwhile we created redis cluster by choosing elasticache from aws management console (we have selected all defaults and given 0 clusters to minimize the cost) 
11. We then come to cloud9 and setup the redis cli by following commands
12.     1. we downloaded redis cli utility : wget http://download.redis.io/redis-stable.tar.gz
13.     2. we unzipped it : tar xvzf redis-stable.tar.gz
14.     3. we then changed the directory to redis-stable and build the redis components using "sudo make BUILD_TLS=yes"
15. Once redis cluster is available, we copie the end point url and tested the connection using command : src/redis-cli -p 6379 -h sessionstore.bxgo7b.0001.use1.cache.amazonaws.com:6379
16. We installed flask,flask-session and redis using fllowing command : python3 -m pip install Flask Flask-Session redis
17. Now we tried verifying redis connection from command line using steps mentioned in redisConnectionTest.py
18. We have created application.py , added required code to it. I have attached code snippet for reference at the end.      
19. We executed the file using following command : python3 application.py(application is up on the url :https://59211903e00640d2a5b2392a84a67bf8.vfs.cloud9.us-east-1.amazonaws.com/login and validated our changes)
20. Post validation, we created requirements file by following command : pip freeze > requirements.txt
21. We have pushed our changes to github by below commands(While keeping the current terminal window for project,  open a new terminal for git to manage the source code)
        1. git add --all
        2. git status
        3. git commit -m "commit message"
        4. git push (during this step please give ur email and token as password)
22. We came to git hub repository to check our changes(we saw all our changes commited to github)
23. To stop the application we can press Ctrl + C in cloud9 command line 
24. We have prepared the readme file content accordingly and pushed the changes to git hub by follwing steps mentioned in 21.
25. We cleaned up all resources in aws as our code changes are there in github.
        
application.py:
#####################################code############################################

import redis
from flask import Flask, session,  escape, request

app = Flask(__name__)
app.secret_key = "Choose very long secret key"

#please copy redis elasticache instance primary end point url
store = redis.from_url('redis://sessionstore.bxgo7b.0001.use1.cache.amazonaws.com:6379')

#mapping route application path
        
@app.route('/')
def index():
    if 'username' in session:
        username = escape(session['username'])
        #hincrby in redis used for incrementing the counter 
        visits = store.hincrby(username, 'visits', 1)
        #specifying ttl for username key - 30 secs
        store.expire(username, 30000)
        return '''
        Logged in as {0}.<br>
        Visits: {1}
        '''.format(username, visits)
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        username = escape(session['username'])
        visits = store.hincrby(username, 'visits', 1)
        store.expire(username, 150)
        return  '''
               Logged in as {0}.<br>
               Visits: {1}
               '''.format(username, visits)
    else:
        return '''
        <form method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <p><input type=text name=username>
        <p><input type=submit value=Login>
        </form>'''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'You are not logged in'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = True)
        
################################################################################
redisConnectionTest.py
      
import redis

#copy primary end point url of redis elasticache
store = redis.from_url('redis://sessionstore.bxgo7b.0001.use1.cache.amazonaws.com:6379')

store.ping()

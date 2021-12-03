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

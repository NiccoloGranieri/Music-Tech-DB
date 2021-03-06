from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
# from boto.s3.connection import S3Connection
import os

app = Flask(__name__)

# Database connection info
app.config['MYSQL_DATABASE_USER'] = os.environ['MTechDB-usr']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MTechDB-psw']
app.config['MYSQL_DATABASE_DB'] = os.environ['MTechDB-db']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MTechDB-host']

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

#endpoint for search
@app.route('/', methods=['GET', 'POST'])

def search():
    if request.method == "POST":
        entry = request.form['entry']
        # search by artist or name
        cursor.execute("SELECT name, artist from Entry WHERE name LIKE %s OR artist LIKE %s", (entry, entry))
        conn.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and entry == 'all': 
            cursor.execute("SELECT name, artist from Entry")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')

@app.route('/insert', methods=['GET', 'POST'])

def insert():
    if request.method == "POST":
        name = request.form['name']
        artist = request.form['artist']
        cursor.execute("INSERT INTO Entry (name, artist) Values (%s, %s)", (name, artist))
        conn.commit()
        return redirect("/", code=302)
    return render_template('insert.html')

def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    app.run()

    
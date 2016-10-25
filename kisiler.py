import psycopg2 as dbapi2

from flask import render_template
from flask import redirect
from flask import request
from flask.helpers import url_for
from config import app

@app.route('/kisiler', methods=['GET', 'POST'])
def kisiler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        query = "SELECT * FROM KISILER"
        cursor.execute(query)
        return render_template('kisiler.html', kisiler = cursor)
    else:
        name_in = request.form['name']
        age_in = request.form['age']
        city_in = request.form['city']
        work_in = request.form['work']
        university_in = request.form['university']
        query = """INSERT INTO KISILER (KisiName, KisiCity, KisiAge, KisiWork, KisiUniversity  )
        VALUES ('"""+name_in+"', '"+city_in+"', '"+age_in+"', '"+work_in+"', '"+university_in+"')"
        cursor.execute(query)
        connection.commit()
        return redirect(url_for('kisiler_sayfasi'))



@app.route('/kisiler/initdb')
def initialize_database_kisiler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = """DROP TABLE IF EXISTS KISILER CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE KISILER (ID SERIAL PRIMARY KEY, KisiName VARCHAR NOT NULL, KisiCity VARCHAR NOT NULL, KisiAge INTEGER, KisiWork VARCHAR, KisiUniversity VARCHAR"""
    cursor.execute(query)
    query = """INSERT INTO KISILER (KisiName, KisiCity, KisiAge, KisiWork, KisiUniversity) VALUES ('Tugba Ozkal','Afyonkarahisar',22, 'Student', 'ITU')"""
    cursor.execute(query)
    query = """INSERT INTO KISILER (KisiName, KisiCity, KisiAge, KisiWork, KisiUniversity) VALUES ('Cagri Gokce', 'Ankara', 22, 'Engineer', 'ITU')"""
    cursor.execute(query)
    query = """INSERT INTO KISILER (KisiName, KisiCity, KisiAge, KisiWork, KisiUniversity) VALUES ('Furkan Evirgen', 'Istanbul', 26, 'CEO', 'BAU')"""
    cursor.execute(query)


    connection.commit()
    return redirect(url_for('kisiler_sayfasi'))

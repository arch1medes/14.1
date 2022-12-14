import json
import sqlite3
import flask

app = flask.Flask(__name__)


def get_value_from_db(sql):
    """Функция, которая возвращает все данные из базы данных"""

    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


def search_by_title(title):
    """Функция, которая возвращает самый свежий фильм по названию фильма из БД"""

    sql = f'''
          SELECT *
          FROM netflix
          WHERE title = '{title}'
          ORDER BY release_year DESC
          LIMIT 1
    '''

    result = get_value_from_db(sql)
    tmp = []
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)



@app.get("/movie/<title>")
def view_title(title):
    sql = f'''SELECT title, country, release_year, listed_in as genre, description
    WHERE title = '{title}'
    ORDER BY release_year DESC
    limit 1'''

    result = get_value_from_db(sql)

    for item in result:
        return dict(item)


@app.get("/movie/<int:year1>/to/<int:year2>")
def search_by_year(year1,year2):

    sql=f'''
        SELECT *      
        FROM netflix       
        WHERE release_year BETWEEN {year1} and {year2}
        LIMIT 100'''
    result=get_value_from_db(sql)

    tmp=[]
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)
    
    

@app.get("/rating/<rating>")
def search_by_raiting(rating):
    """Функция, которая возвращает фильм по рейтингу"""

    my_dict = {"children": ("G"), "family": ("G", "PG", "PG-13"), "adult": ("R", "NC-17")}

    sql = f'''
           SELECT title,rating,description
           FROM netflix
           WHERE rating in {my_dict.get(rating, "NC-17")}'''
    result = get_value_from_db(sql)

    tmp=[]
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)
    

@app.get("/genre/<genre>")
def get_by_genre(genre):
    """Функция возвращает фильм по жанру"""

    sql = f'''
          SELECT title,description
          FROM netflix
          WHERE listed_in LIKE '%{str(genre)[1:]}'
          ORDER BY release_year DESC
          LIMIT 10
    '''

    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)
    

def search_double_name(name1,name2):
    """Функция возвращает актеров, которые играли больше двух раз с введенными актерами"""

    sql = f'''
          SELECT "cast"
          FROM netflix
          WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
          ORDER BY release_year DESC
    '''


    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)

def step_6(type,year,genre):
    """Функция, которая принимает три параметра и возвращает по ним фильмы"""

    sql = f'''
          SELECT title,description,listed_in
          FROM netflix
          WHERE type = '{type}'
          AND release_year = '{year}'
          AND listed_in LIKE '%{genre}%'
    '''
    result = get_value_from_db(sql)

    tmp=[]
    for item in result:
        tmp.append(dict(item))


from flask import jsonify
return jsonify(tmp)
    

if __name__ == '__main__':
  app.run(host='localhost',port=8000,debug=True)

       

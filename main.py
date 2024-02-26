import  sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from usefull.FDataBase import FDataBase
DATABASE = "/tmp/test.db"
DEBUG = True
SECRET_KEY = "sdas231sd2wadasww123ASDWeqw231"
USERNAME = "admin"
PASSWORD = "123"

app = Flask(__name__)
app.config.update(dict(DATABASE = os.path.join(app.root_path, 'test.db') ))
app.config["SECRET_KEY"] = "sdas231sd2wadasww123ASDWeqw231"
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource("sql_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


#ROUTES

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("index.html", menu = dbase.get_menu(), posts = dbase.getPostAnonce())

@app.route("/add_post", methods = ["GET", "POST"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Ошибка добавления", category = "error")
            else:
                flash("Успешно добавлено", category = "success")
        else:
            flash("Ошибка добавления, проверьте ваши данные", category = "error")
    return render_template("add_post.html", menu=dbase.get_menu(), title="Добавление статьи")

@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)

    title, post = dbase.getPost(alias)

    if not title:
        abort(404)

    return render_template("post.html", menu=dbase.get_menu(), title=title, post=post)



def get_db():
    if not  hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="Страница не найдена!")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == "__main__":
    create_db()
    app.run(debug=DEBUG)

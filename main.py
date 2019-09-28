from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key='randomsecretkey4BuildABlog'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog_posts():
    # titles = Blog.query.get(id).all()
    # bodies = Blog.query.get(body).all()
    title='test'
    return render_template('blog.html', title=title)

if __name__ == '__main__':
    app.run()
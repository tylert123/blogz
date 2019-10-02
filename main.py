from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:blogzpass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key='randomsecretkey4BuildABlog'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['user_login','blog_posts','index','user_signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/blog', methods=['GET','POST'])
def blog_posts():
    params = request.args.get('id')
    if not params:
        return render_template('blog.html', blog_post=Blog.query.order_by(Blog.id.desc()).all())
    else:
        indv_post = Blog.query.get(params)
        title = indv_post.title
        body = indv_post.body
        return render_template('single_post.html',blog_title=title,blog_body=body)

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        owner = User.query.filter_by(username=session['username']).first()

        if (blog_title.strip()=='') and (blog_body.strip()==''):
            flash('Please enter a blog title', 'error')
            flash('Please enter a blog message', 'error')
            return render_template('newpost.html', no_title=1, no_body=2)

        if (not blog_title) or (blog_title.strip()==''):
            flash('Please enter a blog title', 'error')
            return render_template('newpost.html', blog_body=blog_body, no_title=1)

        if (not blog_body) or (blog_body.strip()==''):
            flash('Please enter a blog message', 'error')
            return render_template('newpost.html', blog_title=blog_title, no_body=1)

        if (blog_title.strip()!='') and (blog_body.strip()!=''):
            new_blog_post = Blog(blog_title,blog_body,owner)
            db.session.add(new_blog_post)
            db.session.commit()
            new_post_id = Blog.query.order_by(Blog.id.desc()).first()
            new_post_id = new_blog_post.id
            return redirect('/blog?id='+str(new_post_id))

    else: 
        return render_template('newpost.html')

@app.route('/login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash('Logged In!')
            return redirect('/newpost')

        if user and user.password != password:
            flash('Incorrect Password')
            return redirect('/login')

        if not user:
            flash('User does not exist')
            return redirect('/login')

    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if password != verify:
            flash('Passwords do not match')
            return redirect('/signup')

        if existing_user:
            flash('User already exists')
            return redirect('/signup')

        if len(username.strip()) < 3:
            flash('Please enter a username longer then 2 characters')
            return redirect('/signup')

        if len(password.strip()) < 3:
            flash('Please enter a password longer then 2 characters')
            return redirect('/signup')

        if (username.strip()!='') and (password.strip()!='') and (password == verify):

            if not existing_user:
                new_user = User(username,password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

        else:
            flash('Please do not leave any fields blank')
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/logout')
def user_logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()
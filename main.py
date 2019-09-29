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

@app.route('/blog', methods=['GET','POST'])
def blog_posts():
    params = request.args.get('id')
    if not params:
        return render_template('blog.html', blog_post=Blog.query.all())
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

        if (blog_title.strip()=='') and (blog_body.strip()==''):
            flash('Please enter a blog title', 'error')
            flash('Please enter a blog message', 'error')
            return render_template('newpost.html')

        if (not blog_title) or (blog_title.strip()==''):
            flash('Please enter a blog title', 'error')
            return render_template('newpost.html', blog_body=blog_body)

        if (not blog_body) or (blog_body.strip()==''):
            flash('Please enter a blog message', 'error')
            return render_template('newpost.html', blog_title=blog_title)

        if (blog_title.strip()!='') and (blog_body.strip()!=''):
            new_blog_post = Blog(blog_title,blog_body)
            db.session.add(new_blog_post)
            db.session.commit()
            new_post_id = Blog.query.order_by(Blog.id.desc()).first()
            new_post_id = new_blog_post.id
            return redirect('/blog?id='+str(new_post_id))

    else: 
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from csv import writer

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes1.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db=SQLAlchemy(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
key="Qwe123~!"
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///contact.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db_c = SQLAlchemy(app)
# ##CONFIGURE TABLE
# class Contact(db_c.Model):
#     id = db_c.Column(db_c.Integer, primary_key=True)
#     name=db_c.Column(db_c.String(250),unique=False, nullable=False)
#     number=db_c.Column(db_c.Integer, unique=False, nullable=False)
#     mail=db_c.Column(db_c.String(250),unique=False, nullable=False)
#     text=db_c.Column(db_c.String(100000),unique=False, nullable=False)



class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    post=db.session.query(BlogPost).all()
    posts=post
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    # for blog_post in posts:
    #     if blog_post["id"] == index:
    #         requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    m=CreatePostForm()
    if m.validate_on_submit() :
        newpost=BlogPost(
            title=m.title.data,
            subtitle=m.subtitle.data,
            body=m.body.data,
            img_url=m.img_url.data,
            author=m.author.data,
            date=date.today().strftime("%B %d,%Y")
        )
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html",form=m,is_edit=False)

@app.route("/edit/<int:post_id>",methods=["GET","POST"])
def edit_post(post_id):
    post=BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
    title=post.title,
    subtitle=post.subtitle,
    img_url=post.img_url,
    author=post.author,
    body=post.body
)
    if edit_form.validate_on_submit():
        post.title=edit_form.title.data
        post.subtitle=edit_form.subtitle.data
        post.author=edit_form.author.data
        post.img_url=edit_form.img_url.data
        post.body=edit_form.body.data
        db.session.commit()
        return redirect((url_for("show_post",index=post_id)))
    return render_template("make-post.html",form=edit_form,is_edit=True)

@app.route("/delete/<int:index>",methods=["GET","Post"])
def delete_post(index):
    post=BlogPost.query.get(index)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST" :
        name=request.form["name"]
        mail=request.form["mail"]
        num=request.form["num"]
        message=request.form["message"]
        with open("contact.csv","a") as file:
            # file.append([name,mail,num,message])
            writer_object = writer(file)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow([name,mail,num,message])
        print([name,mail,num,message])

        # n=Contact(
        #     name=name,
        #     mail=mail,
        #     number=num,
        #     text=message
        # )
        # db_c.session.add(n)
        # db_c.session.commit()
        return render_template("contact.html",flag_c=True)

    return render_template("contact.html",flag_c=False)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
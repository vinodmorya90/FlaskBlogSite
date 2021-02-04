from datetime import datetime

from bson import ObjectId
from flask import Flask, render_template, request, json, session, redirect
import pymongo
from flask_mail import Mail
from MongoDbConnector import  MongoDbConnector
# Must to define
from pymongo import ReturnDocument

app = Flask(__name__)
app.secret_key = 'secret_key'


# to read app.json file
with open('app.json', 'r') as f:
    params = json.load(f)["params"]
local_server = params['local_server']

if local_server == 'True':
    env_config = 'config_dev.json'
else:
    env_config = 'config_prod.json'

with open(env_config, 'r') as f:
    params = json.load(f)["params"]

# smtp info
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_passwd']
)
# TBD and checked
mail = Mail(app)

## To fetch connection string from app.json file
#client = pymongo.MongoClient(params['uri'])

#my_db = client['Employee']
## Defining Collection name  / employee_information
#info = my_db.employee_information

## Defining Collection name / posts
#info2 = my_db.posts


mongoDb = MongoDbConnector(params['uri'],'Employee')


# Homepage
@app.route('/')
def home():
    return "Hello World . Namaste "
    # posts = mongoDb.GetAllRecords('posts',{})
    # return render_template('index.html', params=params, posts=posts)

# About Us
@app.route('/about')
def about():
    return render_template('about.html')

#
# login page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # if users already login and in session
    if 'user' in session and session['user'] == params['admin_user']:
        posts = mongoDb.GetAllRecords('posts',{})
        #posts = info2.find({})
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            posts = mongoDb.GetAllRecords('posts', {})
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template('login.html', params=params)


# # #New Post
@app.route('/post', methods=['GET'])
def post_route():
    #post1 = info2.find_one({"_id": int(post_id)})
    #post = mongoDb.GetSingleRecord('posts', "")
    #print(post1)
    post1=None
    return render_template('post.html', params=params, output=post1)

#
# #ADD/EDIT POST
@app.route('/edit', defaults={'post_id': None})
@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 'user' in session and session['user'] == params['admin_user']:
        retrievedPost=None
        if post_id!=None:
            retrievedPost=  mongoDb.GetSingleRecord("posts",str(post_id))
        return render_template('edit.html', params=params, id =post_id, post = retrievedPost)


@app.route('/save/<post_id>', methods=['GET','POST'])
def save(post_id):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            tline = request.form.get('tline')
            content= request.form.get('content')
            img_file= request.form.get('img_file')

            record = {
                'title': title,
                'slug': slug,
                'content': content,
                'img_file': img_file,
                'tagline': tline
            }

            if post_id is None or post_id=='None':
                addedPost = mongoDb.insertIntoTable("posts",record)
            else:
                mongoDb.UpdateSingleRecordInTable("posts",str(post_id),record)
    # redirecting after saving post
    return redirect("/dashboard")




# Contact Us
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        record = {
            'name': name,
            'email': email,
            'phone_num': phone,
            'msg': message
        }
        mongoDb.insertIntoTable("employee_information",record)
        mail.send_message(
            'New Message From' + name,
            sender=email,
            recipients=[params['gmail_user']],
            body=message + "\n" + phone
        )
    return render_template('contact.html')


# Sample Post
@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/delete/<post_id>')
def deletePost(post_id):
    mongoDb.DeleteItem('posts',str(post_id))
    return redirect("/dashboard")

# To automatically run without loading again and again
# app.run(debug=True, params[])


app.run(debug=True,port=80)

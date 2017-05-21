""" Web project catalog using flask """
import os
from functools import wraps
from base64 import b64encode
import json
import httplib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, flash, redirect, url_for
from flask import session, jsonify, make_response
from flask_bcrypt import Bcrypt
from oauth2client import client, crypt
from database_setup import User, Category, Items


app = Flask("__name__")
bcrypt = Bcrypt(app)
engine = create_engine("sqlite:///catalog.db")
connectDb = sessionmaker(bind=engine)()


def login_required(f):
    """Wrap function to make sure if user logedinor not
    if not redirect to login page
    for page only allowed for logedin users
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if ("login" in session and session["login"]) is True:
            try:
                user_query = connectDb.query(User).filter(
                    User.id == session["id"]).one()
                if user_query.name == session["user"]:
                    username = [
                        user_query.name,
                        user_query.photo,
                        user_query.id]
                    return f(username, *args, **kwargs)
                else:
                    return redirect(url_for("login"))
            except:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    return wrap


def login_check(session):
    """ Function to check if user loged in or not """
    if ("login" in session and session["login"]) is True:
        try:
            user_query = connectDb.query(User).filter(
                User.id == session["id"]).one()
            if user_query.name == session["user"]:
                username = [user_query.name, user_query.photo, user_query.id]
                return username
            else:
                username = ["None"]
                return username

        except:
            username = ["None"]
            return username

    else:
        username = ["None"]
        return username


def has_privilege(session, item):
    """ Function to ckeck if the user is the owner of the item"""
    user_id = session['id']
    item = connectDb.query(Items).filter(Items.title == item).one()
    if user_id == item.user_id:
        return True
    else:
        return False


@app.route("/")
@app.route("/catalog")
def mainpage():
    """ mainpage for the project  only view category and latest items add"""

    all_category = connectDb.query(Category).all()
    # makeing list of latest items by query for every category for latest

    latest = map(lambda x: [x.name, connectDb.query(Items).filter(
        Items.category_id == x.id).order_by(Items.created.desc()).first()],
        all_category)
    username = login_check(session)
    return render_template("mainpage.html", latest=latest, username=username)


@app.route("/catalog/signup", methods=["GET", "POST"])
def signup():
    """ Signup page to register local users """

    if request.method == "POST":
        username = login_check(session)
        # Check that the user is not loged in
        if username[0] == "None":
            newuser = request.form["user"]
            email = request.form["email"]
            password = request.form["password"]
            h_password = bcrypt.generate_password_hash(password)
            # TODO(mohy) add server side validation before submit.

            check_user = connectDb.query(User).filter(
                User.name == newuser).all()

            check_email = connectDb.query(User).filter(
                User.email == email).all()
            # Check for user if allready registered

            if check_user != []:
                return render_template("signup.html", username=username,
                                       error=newuser)
            # Check for email if allready registered

            if check_email != []:
                return render_template("signup.html", username=username,
                                       error=email)
            # Adding user to database then log him in
            new = User(name=newuser, email=email, password=h_password)
            connectDb.add(new)
            connectDb.commit()
            user_query = connectDb.query(User).filter(
                User.email == email).one()

            session["provider"] = "local"
            session["login"] = True
            session["id"] = user_query.id
            session["user"] = user_query.name
            flash("you loged in successfully")
            return redirect(url_for("mainpage"))
        else:

            flash("you allready loged in ")
            return redirect("/")
    else:

        username = login_check(session)
        if username[0] == "None":

            return render_template("signup.html", username=username)
        else:

            flash("you allready loged in ")
            return redirect("/")


@app.route("/catalog/newcategory", methods=["GET", "POST"])
@login_required
def new_category(username):
    """ Adding new category to the project only loged in user are allowed"""

    if request.method == "POST":
        name = request.form["name"]
        new = Category(name=name)
        connectDb.add(new)
        connectDb.commit()
        return redirect(url_for("mainpage"))
    else:
        return render_template("newC.html", username=username)


@app.route("/catalog/<string:category_name>/items")
def catalog(category_name):
    """ Previewing for any one items for selected category"""

    try:
        # Query for category by id
        category_id = connectDb.query(Category.id).filter(
            Category.name == category_name).one()
        # Query for all items in this category
        items = connectDb.query(Items).filter(
            Items.category_id == category_id[0]).order_by(Items.created).all()
        all_category = connectDb.query(Category).all()
        # Check for login for the navbar info
        username = login_check(session)
        return render_template(
            "items.html", len=len(items), allcategory=all_category,
            items=items, catalog=category_name, username=username)
    except:
        flash("not exist categort")
        return redirect("/")


@app.route("/catalog/<string:category_name>/<string:item>")
def info(category_name, item):
    """ Previewing information about selected item"""

    try:
        items = connectDb.query(Items).filter(
            Items.title == item).one()
        username = login_check(session)
        return render_template(
            "iteminfo.html", items=items,
            catalog=category_name, username=username)

    except:
        flash("not exist item")
        return redirect("/")


@app.route("/catalog/newitem", methods=["GET", "POST"])
@login_required
def newitem(username):
    """ Adding new items in database only regisetered user are allowed"""

    if request.method == "POST":
        title = request.form["title"]
        details = request.form["details"]
        category_name = request.form["category"]
        user_id = session["id"]
        category_id = connectDb.query(Category.id).filter(
            Category.name == category_name).all()[0][0]
        new = Items(title=title, details=details,
                    user_id=user_id, category_id=category_id)
        connectDb.add(new)
        connectDb.commit()
        flash("new item has been add")
        return redirect(url_for("mainpage"))

    else:
        category = connectDb.query(Category).all()
        return render_template(
            "newitem.html", category=category, username=username)


@app.route("/catalog/<string:category_name>/<string:item>/edit",
           methods=["GET", "POST"])
@login_required
def edit(username, category_name, item):
    """ Editing items info only its owner  """

    # Check if the editor is the owner
    if has_privilege(session, item) is True:
        if request.method == "POST":
            # Saving edited data in variables
            item_id = request.form["id"]
            title = request.form["title"]
            details = request.form["details"]
            category_name = request.form["category"]

            # Query to obtain id of category from name
            category_id = connectDb.query(Category.id).filter(
                Category.name == category_name).all()[0][0]
            qedit = connectDb.query(Items).filter(Items.id == item_id).one()
            qedit.title = title
            qedit.details = details
            qedit.category_id = category_id
            connectDb.commit()
            flash("updated successfully")
            return redirect(
                url_for("info", category_name=category_name, item=title))

        else:
            items = connectDb.query(Items).filter(Items.title == item).one()
            category = connectDb.query(Category).all()
            return render_template(
                "edit.html", items=items, category=category, username=username)

    else:
        flash("you do not have privilege to edit or delete %s" % item)
        return redirect(url_for("mainpage"))


@app.route("/catalog/<string:category_name>/<string:item>/delete",
           methods=["GET", "POST"])
@login_required
def delete(username, category_name, item):
    """ Deleteing item from database. """

    # Check if user is the owner of item
    if has_privilege(session, item) is True:
        if request.method == "POST":
            item_id = request.form["id"]
            delete = request.form["delete"]
            if delete == "ok":
                qdelete = (connectDb.query(Items).filter(
                    Items.id == item_id).one())
                connectDb.delete(qdelete)
                connectDb.commit()
                flash("you have deleted an item")
                return redirect(
                    url_for("catalog", category_name=category_name))
            else:
                return redirect(
                    url_for("info", category_name=category_name, item=item))

        else:
            items = connectDb.query(Items).filter(Items.title == item).one()
            return render_template(
                "delete.html", items=items,
                category=category_name, username=username)

    else:
        flash("you do not have privilege to edit or delete %s" % item)
        return redirect(url_for("mainpage"))


@app.route("/catalog.json")
def jsonrequest():
    """Handleing json requests."""

    all_category = connectDb.query(Category).all()
    all_data = []
    for x in all_category:
        # Obtain the object in json format by calling jsonreq method
        y = x.jsonreq
        itemslist = connectDb.query(Items).filter(
            Items.category_id == y["id"]).all()
        items = []
        for i in itemslist:
            items.append(i.jsonreq)
        y["items"] = items
        all_data.append(y)
    return jsonify(catalog=[all_data])


@app.route("/catalog/login", methods=["GET", "POST"])
def login():
    """login page for users """

    if request.method == "POST":
        user = login_check(session)
        if user[0] == "None":
            username = request.form["username"]
            password = request.form["password"]
            # Login by username
            if username.find("@") == -1:
                user_q = connectDb.query(User).filter(
                    User.name == username).all()
                pass_check = bcrypt.check_password_hash(user_q[0].password,
                                                        password)

                if user_q != [] and pass_check is True:
                    session["provider"] = "local"
                    session["login"] = True
                    session["id"] = user_q[0].id
                    session["user"] = user_q[0].name
                    flash("you loged in successfully")
                    return redirect("/")
                else:
                    error = "username or password are not correct"
                    return render_template(
                        "login.html", error=error, username=user)

            # Login by email
            else:
                user_q = connectDb.query(User).filter(
                    User.email == username).all()
                pass_check = bcrypt.check_password_hash(user_q[0].password,
                                                        password)
                if user_q != [] and pass_check is True:
                    session["provider"] = "local"
                    session["login"] = True
                    session["id"] = user_q[0].id
                    session["user"] = user_q[0].name
                    flash("you loged in successfully")
                    return redirect("/")
                else:
                    error = "username or password are not correct"
                    return render_template(
                        "login.html", error=error, username=user)
        else:
            flash("ALLREADY LOGED IN ")
            return redirect("/")

    else:
        username = login_check(session)
        if username[0] == "None":
            # Adding random to cookie to prevent manpulating from  users
            rand = b64encode(os.urandom(20)).encode("utf-8")
            session["rand"] = rand
            return render_template("login.html", username=username)
        else:
            return redirect("/")


@app.route("/facelogin", methods=["POST"])
def facelogin():
    """ Facebook users login to our  website"""
    # Check rand to prevent manpulating from  users

    rand = request.args["rand"]
    if rand == session["rand"]:
        username = login_check(session)
        if username[0] != "None":
            flash("you are allready loged in ")
            return redirect("/")

        accessToken = request.data
        url = ("https://graph.facebook.com/v2.4/me?access_token=%s&fields=name"
               ",id,email,picture.width(720).height(720),gender" % accessToken)
        http = httplib2.Http()
        result = http.request(url, method="GET")
        if "error" in result[0]:
            response = make_response(json.dumps(
                "there is an error in facebook login please try again"), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        data = json.loads(result[1])
        user_q = connectDb.query(User).filter(User.email == data["email"]).all()
        if user_q == []:
            new = User(
                name=data["name"], email=data["email"],
                photo=data["picture"]["data"]["url"]
                )
            connectDb.add(new)
            connectDb.commit()
            user_q = connectDb.query(User).filter(
                User.email == data["email"]).all()

        session["provider"] = "facebook"
        session["login"] = True
        session["id"] = user_q[0].id
        session["user"] = user_q[0].name
        flash("you loged in successfully")
        return "logedin"
    else:
        response = make_response(json.dumps(
            "your session has expire the page will reload the page "), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/gconnect", methods=["POST"])
def gconnect():
    """ Google users login method """

    client_id = ("122663021563-qgegpul8s3rjflmk3im5grfmj29f2i78"
                 ".apps.googleusercontent.com")
    rand = request.args["rand"]
    if rand == session["rand"]:
        username = login_check(session)
        if username[0] != "None":
            flash("you are allready loged in ")
            return redirect("/")
        
        id_token = request.data
        # Verify id token is made by google for our app
        try:
            idinfo = client.verify_id_token(id_token, client_id)

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError:
            response = make_response(json.dumps("invalid token"), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        user_q = connectDb.query(User).filter(
            User.email == idinfo["email"]).all()
        if user_q == []:
            new = User(
                name=idinfo["name"], email=idinfo["email"],
                photo=idinfo["picture"])

            connectDb.add(new)
            connectDb.commit()
            user_q = connectDb.query(User).filter(
                User.email == data["email"]).all()

        session["provider"] = "google"
        session["login"] = True
        session["id"] = user_q[0].id
        session["user"] = user_q[0].name
        flash("you loged in successfully")
        return "logedin"
    else:
        response = make_response(json.dumps(
            "your session has expire the page will reload the page "), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/catalog/<string:user_id>/profile")
@login_required
def profile(username, user_id):
    """ View user information"""

    if int(user_id) == int(session["id"]):
        user = connectDb.query(User).filter(User.id == user_id).one()
        return render_template("profile.html", user=user, username=username)
    else:
        flash("you do not have privilege to view this profile")
        return redirect(url_for("mainpage"))


@app.route("/catalog/logout")
def logout():
    """ clear all add cookeis for log out"""
    try:
        session.pop("rand")
        session.pop("provider")
        session.pop("login")
        session.pop("id")
        session.pop("user")
        return redirect("/catalog/login")
    except:
        return redirect("/catalog/login")


@app.route("/confirm", methods=["post"])
def password_confirm():
    """ Saving changes that made by user in their profile"""

    username = login_check(session)
    if username != ["None"]:
        string_data = request.data
        data = json.loads(string_data)
        user_q = connectDb.query(User).filter(User.id == session["id"]).one()
        confirm = bcrypt.check_password_hash(user_q.password, data[0])
        if confirm is True:
            if data[1] != "":
                user_q.name = data[1]
                session.pop("user")
                session["user"] = data[1]

            if data[2] != "":
                user_q.email = data[2]
            if data[3] != "":
                password = data[3]
                h_password = bcrypt.generate_password_hash(password)
                user_q.password = h_password
            if data[4] != "":

                user_q.photo = data[4]
            connectDb.commit()

            flash("user info update successfully")
            return "submit"
        else:
            return "wrong pass"

    else:
        return "wrong user"


if __name__ == "__main__":
    app.secret_key = "ddffgghh:cv.xvlkfdsmdf6df092348395yrqw%$#$$&*&^&^$#@"
    app.run("0.0.0.0", port=8080, debug=True)

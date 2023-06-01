import flask
from DatabaseManager import DatabaseManager
from PageManeger import PageManeger

app = flask.Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

databaseManager = DatabaseManager("database.db")
databaseManager.printPages()

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/page/<id>")
def loadPage(id):
    return flask.render_template(databaseManager.getPageById(id)[10:])

@app.route("/create_page", methods=['POST', 'GET'])
def create_page():
    name = flask.request.form.get("name")
    databaseManager.createPage(name)
    response = flask.redirect("/")
    return response

@app.route("/del_page", methods=['POST', 'GET'])
def del_page():
    name = flask.request.form.get("name")
    databaseManager.delPage(name)
    databaseManager.printPages()
    response = flask.redirect("/")
    return response

@app.route("/page_ids", methods=['GET'])
def page_ids():
    return {"ids": databaseManager.getListOfPageIds()}


@app.route("/verify_login", methods=["POST"])
def verify_login():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    response = flask.redirect("/")
    if databaseManager.verify_login(username, password):
        token = databaseManager.generate_token()
        response.set_cookie("token", token)
        databaseManager.verify_token(token)

    return response

@app.route("/verify_token", methods=["GET"])
def verify_token():
    return {"valid": databaseManager.verify_token(flask.request.headers.get("token", ""))}

@app.route("/logout", methods=["POST"])
def logout():
    response = flask.redirect("/")
    databaseManager.removeToken(flask.request.headers.get("token", ""))
    return response

app.run("0.0.0.0", 80)
 
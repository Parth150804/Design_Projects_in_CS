from flask import Flask, render_template

app = Flask(__name__)

# @app.route("/")     ## it is basically saying that what url in your website I am navigating through
# def hello_world():
#     return "<h1>Hello World</h1>"

## To avoid using long strings inside the function, we use template files (basically html files)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/about")
def about_page():
    return "<h1>About Page</h1>"

## if we want to add a route dynamically
@app.route("/about/<username>")
def about_the_person(username):
    return f"<h1>This is about page of {username}</h1>"

@app.route("/market")
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template("market.html", items = items)


if __name__ == "__main__":
    app.run(debug = True)   ## debug = true will synchronize our changes here with the website we are making
from flask import Flask, render_template

app = Flask(__name__)

categories = {
    "Fiction": {
        "products": [{
            "title": "The Song of Achilles",
            "description": "Divergent is the debut novel of American novelist Veronica Roth",
            "author": "Veronica Roth",
        }, {
            "title": "The Handmaid's Tale",
            "description": "The Handmaid's Tale is a dystopian novel[6] by Canadian author Margaret Atwood,"
                           "published in 1985. It is set in a near-future New England, in a totalitarian state,"
                           "known as Gilead, that has overthrown the United States government.",
            "author": "Margaret Atwood",
        }, {
            "title": "The Nightingale",
            "description": "The Nightingale (2015) is a novel by the American author Kristin Hannah."
                           "The book tells the story of two sisters in France during World War II, and"
                           "their struggle to survive and resist the German occupation of France.",
            "author": "Kristin Hannah",
        }],
        "title": "Titles, Descriptions, and Authors",
        "subtitle": "Fiction",
        "route": "collectables",
    },
    "Non-Fiction": {
        "products": [{
            "title": "A Brief history in Time",
            "description": "The Maze Runner is a 2009 young adult dystopian science fiction novel",
            "author": "James Dashner",
        },{
            "title": "H is for Hawk",
            "description": "H is for Hawk tells Macdonald's story of the year she spent training a"
                           "northern goshawk in the wake of her father's death.",
            "author": "Helen Macdonald",
        },{
            "title": "In Cold Blood",
            "description": "In Cold Blood is a non-fiction novel[1] by American author Truman Capote,"
                           "first published in 1966; it details the 1959 murders of four members of the"
                           "Herbert Clutter family in the small farming community of Holcomb, Kansas.",
            "author": "Truman Capote",
        }],
        "title": "Titles, Descriptions, and Authors",
        "subtitle": "Non-Fiction",
        "route": "collectables",
    },
    "Action": {
        "products": [{
            "title": "The Maze Runner",
            "description": "The Maze Runner is a 2009 young adult dystopian science fiction",
            "author": "James Dashner",
        },{
            "title": "Divergent",
            "description": "Divergent is the debut novel of American novelist Veronica Roth",
            "author": "Veronica Roth",
        },
        {
            "title": "Catching Fire",
            "description": "Catching Fire is a 2009 science fiction young adult novel by "
                           "the American novelist Suzanne Collins",
            "author": "Suzanne Collins",
        }],
        "title": "Titles, Descriptions, and Authors",
        "subtitle": "Action",
        "route": "electronics",
    },
}

@app.route("/")
def index():
    return render_template("index.html", categories=categories)

@app.route("/category/<name>")
def category(name):
    return render_template("category.html", category=categories[name])

@app.route("/<category>/product/<int:id>")
def product(category, id):
    product = categories[category]["products"][id]
    return render_template("product.html", product=product)

@app.route("/browse")
def browse():
    return render_template("browse.html")

@app.route("/browse/fiction")
def fiction():
    return render_template("fiction.html")

@app.route("/browse/fiction/thesongofachilles")
def song():
    return render_template("TheSongofAchilles.html")

@app.route("/browse/fiction/thehandmaidstale")
def maid():
    return render_template("Thehandmaidstale.html")

@app.route("/browse/fiction/thenightingale")
def night():
    return render_template("thenightingale.html")

@app.route("/browse/nonfiction")
def nonfiction():
    return render_template("nonfiction.html")

@app.route("/browse/nonfiction/abriefhistoryoftime")
def history():
    return render_template("Abriefhistoryoftime.html")

@app.route("/browse/nonfiction/incoldblood")
def blood():
    return render_template("incoldblood.html")

@app.route("/browse/nonfiction/hisforhawk")
def hawk():
    return render_template("Hisforhawk.html")

@app.route("/browse/action")
def action():
    return render_template("action.html")

@app.route("/browse/action/catchingfire")
def catching():
    return render_template("CatchingFire.html")

@app.route("/browse/action/themazerunner")
def maze():
    return render_template("TheMazeRunner.html")

@app.route("/browse/action/divergent")
def diver():
    return render_template("Divergent.html")


"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    melons_purchased = session['cart']

    # Create dictionary of id as the key, values: common name, count, total
    # melon_dictionary = {
    #   id: [common name, count, price, type_total],
    #}
    order_total = 0
    melon_dictionary = {}
    for melon_id in melons_purchased:
        if melon_id in melon_dictionary.keys():
            melon_dictionary[melon_id][1] += 1
            melon_dictionary[melon_id][3] += model.Melon.get_by_id(melon_id).price
        else:
            melon_dictionary[melon_id] = [model.Melon.get_by_id(melon_id).common_name, 1, model.Melon.get_by_id(melon_id).price, model.Melon.get_by_id(melon_id).price]
        order_total += model.Melon.get_by_id(melon_id).price

    return render_template("cart.html", order_total = order_total, melon_dictionary = melon_dictionary)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    if "cart" in session.keys():
        session['cart'].append(id)
    else:
        session['cart'] = [id]

    flash("Melon was added!")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    session['username'] = request.form.get("email")
    session['password'] = request.form.get("password")

    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)

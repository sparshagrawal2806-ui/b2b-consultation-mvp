from flask import Flask, render_template, request
import sqlite3
import os
from flask import redirect


app = Flask(__name__)

DB_NAME = "app_data.sqlite"

# ---------- DATABASE ----------
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """)

        conn.commit()
        conn.close()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/consult", methods=["GET", "POST"])
def consult():
    if request.method == "POST":
        business = request.form.get("business")
        area = request.form.get("area")

        score = 0.80
        verdict = "Highly Recommended"

        return render_template(
            "result.html",
            business=business,
            area=area,
            score=score,
            verdict=verdict
        )

    return "Please submit the form from Home page"


@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()
        conn.close()

    return render_template("add_product.html")

@app.route("/products")
def products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()

    return render_template("products.html", products=data)

# ---------- DATABASE DEMO ----------
@app.route("/db-demo")
def db_demo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()
    return render_template("db_demo.html", products=data)


@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/db-demo")


@app.route("/update/<int:id>", methods=["POST"])
def update_product(id):
    new_price = request.form["price"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET price = ? WHERE id = ?",
        (new_price, id)
    )
    conn.commit()
    conn.close()
    return redirect("/db-demo")


# ---------- MAIN ----------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)




from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "app_data.sqlite"

# ---------- DATABASE ----------
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# ---------- ROUTES ----------

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# CONSULTATION
@app.route("/consult", methods=["GET", "POST"])
def consult():
    if request.method == "POST":
        business = request.form.get("business")
        area = request.form.get("area")

        score = 0.80
        verdict = "Highly Recommended"

        return render_template(
            "consultation.html",
            business=business,
            area=area,
            score=score,
            verdict=verdict
        )

    return render_template("consultation.html")

# ---------- DATABASE DEMO ----------

# ADD PRODUCT
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

        return redirect("/db-demo")

    return render_template("db_demo.html")

# VIEW PRODUCTS (DB DEMO)
@app.route("/db-demo")
def db_demo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()

    return render_template("db_demo.html", products=data)

# DELETE PRODUCT
@app.route("/delete/<int:id>")
def delete_product(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/db-demo")

# UPDATE PRODUCT
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

# ---------- OTHER PAGES ----------

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/buyer")
def buyer():
    return render_template("buyerUI.html")

@app.route("/supplier")
def supplier():
    return render_template("supplierUI.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")

# ---------- MAIN ----------

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)







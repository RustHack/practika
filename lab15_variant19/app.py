"""
ЛР15 — Flask веб-приложение, вариант 19: портфель активов.
Запуск: flask --app app run --port 5000
"""
from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "lab15-secret"

assets = [
    {"id": 1, "ticker": "SBER", "name": "Сбербанк", "type": "stock", "qty": 100, "price": 280.5},
    {"id": 2, "ticker": "GAZP", "name": "Газпром", "type": "stock", "qty": 50, "price": 160.0},
    {"id": 3, "ticker": "OFZ26238", "name": "ОФЗ", "type": "bond", "qty": 10, "price": 980.0},
]
_next = 4

@app.route("/")
def index():
    total = sum(a["qty"] * a["price"] for a in assets)
    return render_template("index.html", assets=assets, total=total)

@app.route("/assets/add", methods=["GET", "POST"])
def add():
    global _next
    if request.method == "POST":
        assets.append({
            "id": _next,
            "ticker": request.form["ticker"].upper(),
            "name": request.form["name"],
            "type": request.form["type"],
            "qty": float(request.form["qty"]),
            "price": float(request.form["price"]),
        })
        _next += 1
        flash("Актив добавлен")
        return redirect(url_for("index"))
    return render_template("form.html")

@app.route("/assets/<int:aid>/edit", methods=["GET", "POST"])
def edit(aid):
    asset = next((a for a in assets if a["id"] == aid), None)
    if not asset:
        flash("Не найден")
        return redirect(url_for("index"))
    if request.method == "POST":
        asset["price"] = float(request.form["price"])
        asset["qty"] = float(request.form["qty"])
        flash("Обновлено")
        return redirect(url_for("index"))
    return render_template("form.html", asset=asset)

@app.route("/assets/<int:aid>/delete", methods=["POST"])
def delete(aid):
    global assets
    assets = [a for a in assets if a["id"] != aid]
    flash("Удалено")
    return redirect(url_for("index"))

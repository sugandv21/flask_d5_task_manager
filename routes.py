from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Task
from extensions import db
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template("index.html", tasks=tasks)

@main.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d").date()
        task = Task(title=title, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add_task.html")

@main.route("/toggle/<int:id>")
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    tasks = Task.query.order_by(Task.due_date).all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "is_done": t.is_done,
        "due_date": t.due_date.strftime("%Y-%m-%d")
    } for t in tasks])


@main.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json()
    due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    task = Task(title=data["title"], due_date=due_date)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "is_done": task.is_done,
        "due_date": task.due_date.strftime("%Y-%m-%d")
    }), 201


@main.route("/api/tasks/<int:id>", methods=["PUT"])
def api_update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    if "title" in data:
        task.title = data["title"]
    if "is_done" in data:
        task.is_done = bool(data["is_done"])
    if "due_date" in data:
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "is_done": task.is_done,
        "due_date": task.due_date.strftime("%Y-%m-%d")
    })


@main.route("/api/tasks/<int:id>", methods=["DELETE"])
def api_delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {id} deleted successfully."})

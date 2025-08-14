from extensions import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

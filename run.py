from app.views import app, db
import os

app.template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

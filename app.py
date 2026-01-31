from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///etudiants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

@app.route("/", methods=["GET", "POST"])
def accueil():
    if request.method == "POST":
        nom = request.form.get("nom")

        if nom:
            nouvel_etudiant = Etudiant(nom=nom)
            db.session.add(nouvel_etudiant)
            db.session.commit()

        return redirect("/")

    etudiants = Etudiant.query.all()

    html = """
    <h1>Liste des étudiants</h1>

    <form method="post">
        <input type="text" name="nom" placeholder="Nom de l'étudiant" required>
        <button type="submit">Ajouter</button>
    </form>
    <hr>
    """

    for e in etudiants:
        html += f"<p>{e.nom}</p>"

    return html

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "astraeus_core_system_9931"


# -----------------------------
# STATE INIT
# -----------------------------
def get_state():
    if "game" not in session:
        session["game"] = {
            "dock": False,
            "electrical": False,
            "medbay": False,
            "lab": False,
            "cockpit": False,
            "cafeteria_unlocked": False
        }
    return session["game"]


def save(state):
    session["game"] = state
    session.modified = True


# -----------------------------
# MAIN MENU
# -----------------------------
@app.route("/")
def main():
    return render_template("main.html")


# -----------------------------
# STORY MESSAGE
# -----------------------------
@app.route("/message")
def message():
    return render_template("message.html")


# -----------------------------
# DOCK PUZZLE (ENTRY GATE)
# -----------------------------
@app.route("/dock", methods=["GET", "POST"])
def dock():
    s = get_state()

    if request.method == "POST":
        code = request.form.get("code")

        if code == "5237":
            s["dock"] = True
            s["cafeteria_unlocked"] = True
            save(s)
            return redirect(url_for("cafeteria"))

        return render_template("dock.html", error="ACCESS DENIED")

    return render_template("dock.html", unlocked=s["cafeteria_unlocked"])


# -----------------------------
# CAFETERIA (ONLY HUB)
# -----------------------------
@app.route("/cafeteria")
def cafeteria():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    return render_template("cafeteria.html", state=s)


# -----------------------------
# ELECTRICAL PUZZLE
# -----------------------------
@app.route("/electrical", methods=["GET", "POST"])
def electrical():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    if request.method == "POST":
        ans = request.form.get("order", "").replace(" ", "").lower()

        correct = "purpleredgreenorangeblueyellow"

        if ans == correct:
            s["electrical"] = True
            save(s)
            return render_template("electrical.html", success=True)

        return render_template("electrical.html", error="SEQUENCE FAILED")

    return render_template("electrical.html")


# -----------------------------
# MEDBAY PUZZLE
# -----------------------------
@app.route("/medbay", methods=["GET", "POST"])
def medbay():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    if request.method == "POST":
        code = request.form.get("code")

        if code == "0526":
            s["medbay"] = True
            save(s)
            return render_template("medbay.html", success=True)

        return render_template("medbay.html", error="MEDICAL LOCKOUT")

    return render_template("medbay.html")


# -----------------------------
# RESEARCH LAB PUZZLE
# -----------------------------
@app.route("/lab", methods=["GET", "POST"])
def lab():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    if request.method == "POST":
        code = request.form.get("code")

        if code == "7138":
            s["lab"] = True
            save(s)
            return render_template("lab.html", success=True)

        return render_template("lab.html", error="DATA CORRUPT")

    return render_template("lab.html")


# -----------------------------
# COCKPIT (FINAL PUZZLE)
# -----------------------------
@app.route("/cockpit", methods=["GET", "POST"])
def cockpit():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    if request.method == "POST":
        code = request.form.get("code")

        if code == "4157":
            s["cockpit"] = True
            save(s)
            return render_template("cockpit.html", ending=True)

        return render_template("cockpit.html", error="FINAL LOCK ACTIVE")

    return render_template("cockpit.html")


# -----------------------------
# RESET
# -----------------------------
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("main"))


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

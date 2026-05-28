from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "astraeus_core_system_9931"


# -----------------------------
# STATE INIT (SAFE)
# -----------------------------
def get_state():
    if "game" not in session:
        session["game"] = {
            "dock": False,
            "cafeteria_unlocked": False,

            "electrical": False,
            "electrical_audio_pending": False,

            "medbay": False,
            "lab": False,
            "cockpit": False
        }
    return session["game"]


def mark_dirty():
    session.modified = True


# -----------------------------
# MAIN
# -----------------------------
@app.route("/")
def main():
    return render_template("main.html")


@app.route("/message")
def message():
    return render_template("message.html")


# -----------------------------
# DOCK (ENTRY)
# -----------------------------
@app.route("/dock", methods=["GET", "POST"])
def dock():
    s = get_state()

    if request.method == "POST":
        code = request.form.get("code")

        if code == "5237":
            session["game"]["dock"] = True
            session["game"]["cafeteria_unlocked"] = True
            mark_dirty()
            return redirect(url_for("cafeteria"))

    return render_template("dock.html")


# -----------------------------
# CAFETERIA (HUB)
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
@app.route("/electrical/puzzle", methods=["GET", "POST"])
def electrical_puzzle():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    correct = "purpleredgreenorangeblueyellow"

    if request.method == "POST":
        ans = request.form.get("order", "").replace(" ", "").lower()

        if ans == correct:
            session["game"]["electrical"] = True
            session["game"]["electrical_audio_pending"] = True
            mark_dirty()
            return render_template("electrical_puzzle.html", solved=True)

        return render_template("electrical_puzzle.html", error="SEQUENCE FAILED", solved=False)

    return render_template("electrical_puzzle.html", solved=s.get("electrical", False))


# -----------------------------
# ELECTRICAL DIARY
# -----------------------------
@app.route("/electrical/diary")
def electrical_diary():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    return render_template("electrical_diary.html")


# -----------------------------
# ELECTRICAL MANUAL
# -----------------------------
@app.route("/electrical/manual")
def electrical_manual():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    return render_template("electrical_manual.html")


# -----------------------------
# ELECTRICAL AUDIO CUTSCENE
# -----------------------------
@app.route("/electrical/audio")
def electrical_audio():
    s = get_state()

    if not s.get("electrical"):
        return redirect(url_for("electrical_puzzle"))

    session["game"]["electrical_audio_pending"] = False
    mark_dirty()

    return render_template("electrical_audio.html")


# -----------------------------
# MEDBAY
# -----------------------------
@app.route("/medbay", methods=["GET", "POST"])
def medbay():
    s = get_state()

    if not s["cafeteria_unlocked"]:
        return redirect(url_for("dock"))

    if not s["electrical"]:
        return redirect(url_for("cafeteria"))

    solved = False
    error = None

    if request.method == "POST":

        nora_symptom = request.form.get("nora_symptom")
        ryland_job = request.form.get("ryland_job")
        theodore_symptom = request.form.get("theodore_symptom")
        grace_job = request.form.get("grace_job")
        grace_diagnosis = request.form.get("grace_diagnosis")

        correct = (
            nora_symptom == "paranoia" and
            ryland_job == "Researcher" and
            theodore_symptom == "auditory" and
            grace_job == "Botanist" and
            grace_diagnosis == "unstable"
        )

        if correct:
            session["game"]["medbay"] = True
            mark_dirty()
            solved = True
        else:
            error = "MEDICAL RECORD MISMATCH"

    return render_template("medbay.html", solved=solved, error=error)


# -----------------------------
# RESEARCH LAB
# -----------------------------
@app.route("/lab", methods=["GET", "POST"])
def lab():
    s = get_state()

    if not s["medbay"]:
        return redirect(url_for("cafeteria"))

    solved = False
    error = None

    correct_code = "94843"

    if request.method == "POST":
        code = request.form.get("code", "")

        if code == correct_code:
            session["game"]["lab"] = True
            mark_dirty()
            solved = True
        else:
            error = "RESEARCH CONTAINMENT OVERRIDE FAILED"

    return render_template("lab.html", solved=s.get("lab", False), error=error)


@app.route("/lab/message")
def lab_message():
    s = get_state()

    if not s.get("lab"):
        return redirect(url_for("lab"))

    return render_template("lab_message.html")


# -----------------------------
# COCKPIT (FINAL)
# -----------------------------
@app.route("/cockpit", methods=["GET", "POST"])
def cockpit():
    s = get_state()

    if not s["lab"]:
        return redirect(url_for("cafeteria"))

    error = None

    if request.method == "POST":
        code = request.form.get("code", "")

        correct_code = "2785"

        if code == correct_code:
            session["game"]["cockpit"] = True
            mark_dirty()
            return redirect(url_for("ending"))

        error = "INVALID SELF-DESTRUCT CODE"

    return render_template("cockpit.html", error=error)

@app.route("/cockpit/image/1")
def cockpit_image_1():
    return render_template("cockpit_image_1.html")


@app.route("/cockpit/image/2")
def cockpit_image_2():
    return render_template("cockpit_image_2.html")


@app.route("/cockpit/image/3")
def cockpit_image_3():
    return render_template("cockpit_image_3.html")


@app.route("/cockpit/image/4")
def cockpit_image_4():
    return render_template("cockpit_image_4.html")


@app.route("/ending")
def ending():
    s = get_state()

    if not s.get("cockpit"):
        return redirect(url_for("cockpit"))

    return render_template("ending.html")


# -----------------------------
# RESET GAME
# -----------------------------
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("main"))


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
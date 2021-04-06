from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def get_title_page():
    """Create title page with survey name and instructions"""
    return render_template("home.html", survey=survey)


@app.route("/start", methods=["GET", "POST"])
def start_survey():
    """redirect user to first question"""
    return redirect("/question/0")


@app.route("/question/<int:quest_id>")
def show_questions(quest_id):
    """get questions based on order and  display
    if statements prevent user from going to page they are not supposed to be on"""
    if responses is None:
        return redirect("/")
    if len(responses) == len(survey.questions):
        return redirect("/thankyou")
    if quest_id != len(responses):
        flash(
            f"***You were on an invalid question ({quest_id}), so we redirected you! :) ***"
        )
        return redirect(f"/question/{len(responses)}")
    question = survey.questions[quest_id]
    return render_template("question.html", question=question, quest_id=quest_id)


@app.route("/answer", methods=["POST"])
def handle_ans():
    """get user answer that was submitted, add it to the response list, and redirect
    to next question. If survey is completed, redirect user to thank you page"""
    user_answer = request.form["answer"]
    responses.append(user_answer)
    if len(responses) != len(survey.questions):
        return redirect(f"/question/{len(responses)}")
    else:
        return redirect("/thankyou")


@app.route("/thankyou")
def finish_survey():
    """Show page that shows survey is complete"""

    return render_template("thankyou.html")
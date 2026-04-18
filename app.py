from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    name = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            # INTENTIONALLY VULNERABLE: user input is embedded in the template
            # string before render_template_string is called.
            tmpl = (
                f'<span class="greeting-text">'
                f"Hello, {name}! Welcome to HootCorp Internal Greeter."
                f"</span>"
            )
            result = render_template_string(tmpl)
    return render_template("index.html", result=result, name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



import main_functions

app = Flask(__name__)

raw_data = main_functions.scrap()

print(raw_data)   

preprocessed_data = main_functions.preprocess_news_text(raw_data)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None

    if request.method == "POST":
        user_text = request.form["user_text"]
        output = main_functions.response(user_text, preprocessed_data)

    return render_template("index.html", preprocessed=preprocessed_data, output=output)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

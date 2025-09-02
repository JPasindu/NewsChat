from flask import Flask, render_template, request

import main_functions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    
    if request.method == "POST":
        user_text = request.form["user_text"]
        output = main_functions.response(user_text)
    
    preprocessed_data, _ = main_functions.get_news_data()
    
    return render_template("index.html", 
                         preprocessed=preprocessed_data[:1000] + "..." if preprocessed_data else "",
                         output=output)


if __name__ == "__main__":
    main_functions.initialize_components()
    app.run()
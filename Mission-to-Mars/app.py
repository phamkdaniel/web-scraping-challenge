from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return rander_template('index.html', name=name)


@app.route('/scrape')
def scrape():
    return

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, request, render_template
import requests

app = Flask(__name__)

NUMVERIFY_API_KEY = "e2a124b534c2404e935181df56541bec"

def validate_phone(number):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}"
    response = requests.get(url)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def home():
    result = {}
    if request.method == 'POST':
        number = request.form['phone']
        result = validate_phone(number)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

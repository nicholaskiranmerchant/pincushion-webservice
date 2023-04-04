from flask import Flask

app = Flask(__name__)

@app.get("/")
def hello_world():
    return {
        'data': {
            'message': "Yo what's popping kings and kingesses"
        }, 
        'links': [
            {
                'rel': 'self', 
                'href': '/'
            }
        ]
    }

if __name__ == '__main__':
    app.run(debug=False)
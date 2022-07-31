from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mynoteapp'


# @app.route('/')
# def index():
#     return "Welcome" 
    
if __name__ == '__main__':
    app.run(debug=True)
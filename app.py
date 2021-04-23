from flask import Flask,render_template,request,redirect
import pandas as pd
#import plotly
#import plotly.graph_objs as go
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

"""
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Boxtrends15AC15@localhost/yoga'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(200),unique=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

"""



@app.route("/")
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home', methods=['GET','POST'])
def home():
        #r = request.form.get('search')
        query = request.form['search']
        cx = '79c6aa852ef78707e'
        key = 'AIzaSyCYJR3f-WyjmUz3_8eAC6OmKTAfCx-KR5A'

                    #query = request.form['text']
        page = 1
        start = (page - 1) * 10 + 1
        for url in query:
            url=f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}"

        data = requests.get(url).json()
        search_items = data.get("items")
        import urllib.parse as p
        target_domain = "google.com"

        for i, search_item in enumerate(search_items, start=1):
            rank = search_item.get("rank")
            title = search_item.get("title")
            snippet = search_item.get("snippet")
            html_snippet = search_item.get("htmlSnippet")
            link = search_item.get("link")

        df = pd.DataFrame(search_items, columns=["title","snippet","link"])

        #html = df.to_html()
        #print(html)

        text = df.snippet[3]
        wordcloud = WordCloud(max_font_size=50, max_words=20, background_color="white").generate(text)

                    # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('static/images/new_plot.png')

        #return render_template('home.html',query=query,output='home')
        #return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
        return render_template('home.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
    return render_template('/home')



if __name__=="__main__":
    app.run(debug=True)

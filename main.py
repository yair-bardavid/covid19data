import json
import datetime
import random

from flask import Flask, render_template, url_for, request, session
from analysis import *
from heb_utils import titles2heb, contry2heb


# =============================================================================
# anchor_date = datetime.datetime(2020, 4, 13)
# with open(f'news_strings_{anchor_date.strftime("%d-%m-%Y")}.json', 'w') as f:
#     news_strings_dict = json.load(f)
# =============================================================================

country = "Israel"

news_strings_dict, anchor_date = generate_news(country=country)

indices_dict = {}
for news_type in news_strings_dict.keys():
    indices = list(range(len(news_strings_dict[news_type])))
    random.shuffle(indices)
    indices_dict[news_type] = indices
    
news2color = {'up_news': "#28a745", 'dn_news': "#dc3545"}

app = Flask(__name__)
app.secret_key = '5lZMUR5uTSyjHwxRd0Buht2D'

@app.route("/", methods=['GET','POST'])
def home():
    
    if request.method == "POST":
        news_type = request.form['news_type']
        counter_var = news_type.split('_')[0] + '_counter'
        session[counter_var] = session.get(counter_var, -1) + 1
        if session[counter_var] == len(indices_dict[news_type]):
            session[counter_var] = 0

        return render_template("home.html", 
                               country=contry2heb.get(country),
                               news_string = news_strings_dict[news_type][indices_dict[news_type][session[counter_var]]],   
                               news_strings_dict=news_strings_dict, 
                               news_type=news_type,
                               news_color = news2color[news_type],
                               news_title = titles2heb[news_type][random.randint(0,len(titles2heb[news_type])-1)],
                               anchor_date = anchor_date.strftime("%d-%m-%Y"))
        
    if request.method == "GET":
        session['up_counter'] = -1
        session['dn_counter'] = -1
        return render_template("home.html",
                               country=contry2heb.get(country),
                               news_strings_dict=news_strings_dict,
                               news_color = "#cecece")
    return render_template("home.html",
                           country=contry2heb.get(country),
                           news_strings_dict=news_strings_dict,
                           news_color = "#cecece")

if __name__ == "__main__":
    app.run(debug=True)

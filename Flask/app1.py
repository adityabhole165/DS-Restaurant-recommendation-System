import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, redirect, render_template, request, url_for
import os

app = Flask(__name__)

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zomato_df = pd.read_csv(os.path.join(BASE_DIR, 'restaurant1.csv'))

def get_recommendations(restaurant_name):
    match = zomato_df[zomato_df['name'] == restaurant_name]
    if match.empty:
        return None
    input_restaurant = match.iloc[0]
    first_cuisine_keyword = input_restaurant['cuisines'].split()[0]
    similar_restaurants = zomato_df[zomato_df['cuisines'].apply(
        lambda x: x.split()[0] == first_cuisine_keyword)]
    top_restaurants = similar_restaurants.sort_values(
        by='Mean Rating', ascending=False)
    top_restaurants = top_restaurants[~top_restaurants.duplicated(
        subset=['name', 'cuisines', 'cost'], keep='first')]
    return top_restaurants.head(10)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    return render_template('recommend.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant_name')
        if not restaurant_name:
            return "Error: No restaurant name provided."
        top_restaurants = get_recommendations(restaurant_name)
        if top_restaurants is None:
            return "Error: Restaurant not found. Please go back and try another name."
        top_restaurants_list = top_restaurants.to_dict('records')
        return render_template('result.html', 
                             recommended_restaurants=top_restaurants_list)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

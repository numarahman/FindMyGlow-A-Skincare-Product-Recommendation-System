from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# load vectorizer and tf-idf matrix
vectorizer = joblib.load("tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load("tfidf_matrix.pkl")

# Connect to database
def get_db_connection():
    conn = sqlite3.connect("skincare_products.db")
    conn.row_factory = sqlite3.Row 
    return conn

# Home page
@app.route('/')
def index():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    all_categories = sorted(df['product_category'].dropna().unique())
    all_prices = ["0-15", "16-30", "31-45", "46-60", "61+"]
    skin_types = ['for_dry_skin', 'for_oily_skin', 'for_combination_skin']
    constraints = ['is_alcohol_free', 'is_vegan', 'is_hypoallergenic']

    return render_template(
        "index.html",
        categories=all_categories,
        prices=all_prices,
        skin_types=skin_types,
        constraints=constraints
    )


# Results page
@app.route('/results', methods=['POST'])
def results():
    selected_categories = request.form.getlist("product_category")
    selected_skin_types = request.form.getlist("skin_type")
    selected_prices = request.form.getlist("price_category")
    selected_constraints = request.form.getlist("constraint")

    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()


    mask = pd.Series([True] * len(df))

    # category filtering
    if selected_categories:
        mask &= df['product_category'].isin(selected_categories)

    # price filtering
    if selected_prices:
        mask &= df['price_category'].isin(selected_prices)

    # Skin types
    if selected_skin_types:
        skin_mask = pd.Series([False] * len(df))
        for skin_type in selected_skin_types:
            skin_mask |= df[skin_type] == 1
        mask &= skin_mask

    # constraints filtering
    for constraint in selected_constraints:
        mask &= df[constraint] == 1

    filtered_df = df[mask].copy()


    if filtered_df.empty:
        return render_template("results.html", products=[], message="No matching products found.")

    # create user profile and score similarity to sort by relevance
    user_profile = ' '.join(selected_categories + selected_prices + selected_skin_types)
    user_vector = vectorizer.transform([user_profile])
    filtered_vectors = vectorizer.transform(filtered_df['combined_text'])

    scores = cosine_similarity(user_vector, filtered_vectors).flatten()
    filtered_df['score'] = scores
    top_products = filtered_df.sort_values(by='score', ascending=False).head(10)

    return render_template("results.html", products=top_products.to_dict(orient='records'))

# Product detail page
@app.route('/product/<product_id>')
def product(product_id):
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    # get main product
    product = df[df['product_id'] == product_id].iloc[0]

    # recommend similar products
    index = df[df['product_id'] == product_id].index[0]
    similarity_scores = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
    similar_indices = similarity_scores.argsort()[::-1][1:6]
    similar_products = df.iloc[similar_indices].to_dict(orient='records')

    # more from same brand
    brand_matches = df[(df['brand_name'] == product['brand_name']) & (df['product_id'] != product_id)].head(5)
    brand_products = brand_matches.to_dict(orient='records')

    return render_template(
        "product.html",
        product=product,
        similar_products=similar_products,
        brand_products=brand_products
    )

if __name__ == "__main__":
    app.run(debug=True)

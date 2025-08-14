from flask import Flask, render_template, request
import numpy as np
import pickle

popularity_df = pickle.load(open('popularity.pkl', 'rb'))
pivot_Table = pickle.load(open('pivot_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
                           image=list(popularity_df['Image-URL-L'].values),
                           votes=list(popularity_df['Num-Ratings'].values),
                           rating=list(popularity_df['Avg-Rating'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')

    try:
        index = np.where(pivot_Table.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pivot_Table.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
            data.append(item)

        return render_template('recommend.html', data=data)

    except IndexError:
        return render_template('recommend.html', data=[], error=f"No recommendations found for '{user_input}'")

if __name__ == '__main__':
    app.run(debug=True)
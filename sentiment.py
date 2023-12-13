import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import streamlit as st
import pickle
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.cluster import KMeans
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
import numpy as np
from keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('wordnet')

# Data scraping from finviz

finviz_url = 'https://finviz.com/quote.ashx?t='


tickers = ['AMZN', 'GOOG', 'NFLX', 'AAPL']
news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})

    try:
        response = urlopen(req)
        html = BeautifulSoup(response, 'html')
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

# Data cleaning
parsed_data = []
for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        if row.a is not None:
            title = row.a.get_text()
            date_data = row.td.text.split(' ')
            date_data = list(filter(lambda x: x.strip() != '', date_data))  # Remove empty strings
            if len(date_data) == 1:
                time = date_data[0].strip()
            else:
                date = date_data[0].strip()
                time = date_data[1].strip()

            parsed_data.append([ticker, date, time, title])
        else:
            title = "Default value"
            parsed_data.append([ticker, "", "", title])

print(parsed_data)

# data creation
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
print(df.head())
lemmatizer = WordNetLemmatizer()
print(df['title'])
corpus = []

# Lemmatization
for i in range(0, len(df)):
    review = re.sub('[^a-zA-Z]', ' ', df['title'][i])
    review = review.lower()
    review = review.split()

    review = [lemmatizer.lemmatize(word) for word in review if word not in stopwords.words('english')]

    review = ' '.join(review)
    print(review)  # Add this line to see the preprocessed review
    corpus.append(review)

cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()



# loading the saved model
loaded_model = pickle.load(open('model.sav', 'rb'))


def kmeans_sentiment_analysis(data):
    # sourcery skip: inline-immediately-returned-variable
    k = 3
    kmeans = KMeans(n_clusters=k)
    
    # Transform the input data using the same CountVectorizer used for training
    X = cv.transform(data).toarray()

    cluster_labels = kmeans.fit_predict(X)
    cluster_sentiments = {
        0: "positive",
        1: "negative",
        2: "neutral"
    }
    X = cv.transform(data).toarray()

    cluster_labels = kmeans.fit_predict(X)
    # Assign sentiments to sentences based on cluster labels
    sentiment_predictions = [cluster_sentiments[label] for label in cluster_labels]
    
    return sentiment_predictions



# using nltk
nltk.download('vader_lexicon')



def nltksentimentanalysis(data):
    sid = SentimentIntensityAnalyzer()
    sentiment_predictions = []

    for sentence in data:
        ss = sid.polarity_scores(sentence)
        compound = ss['compound']
        
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        sentiment_predictions.append(sentiment)

    return sentiment_predictions

#instance for title column if df
sent=df['title']
## Vocabulary Size
voc_size = 10000
# One-hot representation
one_hot_repr=[one_hot(words,voc_size) for words in sent]
print(one_hot_repr)

# Word Embedding
sent_length=20
embedded_docs=pad_sequences(one_hot_repr, padding='pre',maxlen=sent_length)
print(embedded_docs)
embedding_vector_features=40
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))

# Define the LSTM model
def lstmRNN(data):
    # sourcery skip: inline-immediately-returned-variable
    k = 3
    kmeans = KMeans(n_clusters=k)
    # fit your training dataset on the k means algorithm and predict clusters of test set points
    X = cv.transform(data).toarray()
    cluster_labels = kmeans.fit_predict(X)
    # Transform the input data using the same CountVectorizer used for training
    model = Sequential()
    model.add(Embedding(input_dim=voc_size, output_dim=embedding_vector_features, input_length=sent_length))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dense(3, activation='softmax'))  # 3 classes for positive, negative, and neutral
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    one_hot_labels = to_categorical(cluster_labels, num_classes=3)
    y = one_hot_labels
    model.summary()

    # Split the data into training and testing sets
    len(embedded_docs),y.shape
    X_final=np.array(embedded_docs)
    Y_final=np.array(y)
    X_final.shape,Y_final.shape
    X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.33, random_state=42)
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=64)
    predicted_sentiments = []
    for sentence in sent:
        sentence_encoded = [one_hot(sentence, voc_size)]
        sentence_padded = pad_sequences(sentence_encoded, maxlen=sent_length, padding='pre')

        # Using trained model to predict sentiment
        predicted_probabilities = model.predict(sentence_padded)

        # Converting the predicted probabilities to a sentiment label
        predicted_sentiment_label = np.argmax(predicted_probabilities)

        # Maping the numeric sentiment label to its corresponding sentiment class
        sentiment_classes = ['positive', 'negative', 'neutral']
        predicted_sentiment = sentiment_classes[predicted_sentiment_label]

        # Append the predicted sentiment to the list
        predicted_sentiments.append(predicted_sentiment)
        
        # Print the predicted sentiments for all sentences
        for sentence, sentiment in zip(sent, predicted_sentiments):
            print(f"Sentence: {sentence} - Predicted Sentiment from RNN: {sentiment}")

    return predicted_sentiments


def main():  # sourcery skip: extract-method
    st.markdown('<h1 style="color:dark blue;">Sentiment Analysis of Financial news of Big Tech companies</h1>', unsafe_allow_html=True)
    st.image("image2.jpg", caption="Financial Sentimental Analysis")

    st.text("This project is about predicting the sentiments of financial news headlines viz. ")
    st.text(" positive(0), negative(1) and neutral(2).")
    st.text("The real time financial news headlines of 4 tech giants Google,Amazon,Netflix ")
    st.text("and Apple are scraped from finviz using python library BeautifulSoup.")
    st.text("Sentiment analysis has been done using three techniques : Kmeans, nltk library and LSTM RNN. ")
    st.text("User can choose the technique by which they want to see the prediction of sentiment. ")

    if st.button("View dataframe"):
        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
        st.dataframe(df[['ticker', 'date', 'time', 'title']])

    st.text("Choose the technique using which you wish to do the sentiment analysis --> ")
    st.text("Kmeans or nltk or LSTM RNN")
    prediction = ' '
    if st.button("KMeans"):
        prediction = kmeans_sentiment_analysis(corpus)
        st.success("Sentiment prediction using KMeans")
        st.write(prediction)
    elif st.button("nltk"):
        prediction = nltksentimentanalysis(corpus)
        st.success('Sentiment Prediction')
        st.write(prediction)
    elif st.button("LSTM RNN"):
        prediction = lstmRNN(corpus)
        st.success('Sentiment Prediction')
        st.write(prediction)
    else:
        st.error("Please select a technique")


if __name__=='__main__':
    main()
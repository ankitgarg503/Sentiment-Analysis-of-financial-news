# Sentiment-Analysis-of-financial-news

<h3>Machine Learning</h3>
<p>A Machine Learning Project to predict the sentiments (positive, negative, or neutral) on real-time financial news headlines through unsupervised textual data of big tech companies using NLTK, K-Means Clustering Algorithm, and LSTM RNN and thus performing the mismatch or divergence between both the models.</p>
<h3>Come, Visit the Site for a Better Choice of Stock Investment!&#127881;</h3>

# Tech Stack<br>
<details>
  <summary>Data Collection</summary>  <br>
  
  > Python's BeautifulSoup module is used to scrape real-time financial news data from finviz.
  > Following that, the headlines are cleaned and prepared for analysis.

</details>

<details>
  <summary>Preprocessing</summary>  <br>
  
  > Lemmatization and stopword elimination are two preprocessing techniques used on the headlines to get the data ready for sentiment analysis.

</details>


  # Analysis Techniques<br>
<details>
<summary>KMeans Clustering</summary>  <br>

  > CountVectorizer is used to create the bag of words model.

  > used to group similar data points together in a process known as clustering. There are three clusters for sentiments like <b>Positive, Negative, and Neutral</b>.


</details>

<details>
<summary>Vader lexicon NLTK</summary>  <br>
  
  > A suite of libraries and programs for symbolic and statistical natural language processing (NLP) for English written in the Python programming language. It supports classification, tokenization, parsing, and semantic reasoning functionalities.

  > Sentiment analysis is done using the NLTK library, more especially the VADER sentiment analyzer. Headlines are categorised as good, negative, or neutral based on the computation of sentiment scores.

  > Results are visualized using matplotlib.
  <img src="https://github.com/ankitgarg503/Sentiment-Analysis-of-financial-news/assets/114798433/0a64284a-c483-4684-9f21-cd750a6e19e0" alt="image" width=500/>

</details>


<details>
<summary>LSTM RNN(Recurrent Neural Network)</summary>  <br>

  > A type of RNN with higher memory power to remember the outputs of each node for a more extended period to produce the outcome for the next node efficiently.
  
  > The preprocessed data is used to train an LSTM RNN model for more sophisticated sentiment analysis. Based on the patterns that were learned from the text input through K-Means clustering, the model classifies attitudes as positive, negative, or neutral, thereby confirming its predictions.

  > Results for the RNN model are visualized using a pie chart in Matplotlib.
  <img src="https://github.com/ankitgarg503/Sentiment-Analysis-of-financial-news/assets/114798433/7e8d01b4-3ead-4208-94a8-f4e114d9907b" alt="image" width=500>

</details>


<h3>Mismatch Between both models</h3>
<details>
  <summary>KMeans v/s RNN</summary>
  <img src="https://github.com/ankitgarg503/Sentiment-Analysis-of-financial-news/assets/114798433/fe37acd4-d5f2-45e0-b412-f839b8107e41" alt="image" width=500>
</details>

<h3>Google Colab</h3>
<p>Link: https://colab.research.google.com/drive/1BJnqb02DR1WtWv8I159GNiqC4uhXtp1b?usp=sharing</p>

<h3>Deployment</h3>
<h5>Deployment is done using Streamlit</h5>
<p>
  Website Link: https://ankitgarg.streamlit.app/
</p>

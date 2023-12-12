# %matplotlib inline
import numpy as np 
import pandas as pd 
import re
import nltk 
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.metrics import confusion_matrix
import seaborn as sn
from textblob import TextBlob
from afinn import Afinn


def sentimental_analysis():

    #Loading the File
    df = pd.read_csv('./files/comments_cleaned_for_sentimental.csv')
    # df = pd.read_csv('./files/comments_cleaned.csv',usecols=['domain_name','reviewer_country','reviewer_rate', 'reviewer_message']).rename(columns={'domain_name': 'company','reviewer_country':'country','reviewer_rate': 'rating', 'reviewer_message': 'reviews'})
    #df.columns = ['rating', 'reviews']
    #df
    # Now, the DataFrame will have the "Reviews" column
    rating_mapping = {1: 'negative', 2: 'negative', 3: 'neutral', 4: 'positive', 5: 'positive'}

    # Use the replace method to update the 'rating' column.
    df['rating_scale3'] = df['rating'].replace(rating_mapping)

    #Preprocessing
    #lowercase
    df['reviews']= df['reviews'].str.replace('rt ',"").str.replace('@','').str.replace('#','').str.replace('[^\w\s]','').str.replace('[1-9]','')


    #1. Sentiment Analysis with TextBlob
    threshold=0.1
    def get_tweet_sentiment(tweet):
            
            sentiment= []
            text = []
            
            for i in np.arange(0, len(tweet)):
            
                # create TextBlob object of passed tweet text
                analysis = TextBlob(tweet[i])
            
                # set sentiment
                if analysis.sentiment.polarity > threshold:
                    #text.append(tweet[i])
                    sentiment.append('positive')
                if analysis.sentiment.polarity < -threshold:
                    #text.append(tweet[i])
                    sentiment.append('negative')
                
                else:
                    #text.append(tweet[i])
                    sentiment.append('neutral')
            
            return pd.DataFrame(sentiment, columns=['sentiment'])
        
    # Define a function to perform sentiment analysis using TextBlob and categorize into three categories.
    def get_sentiment_category(text):
        # Convert any non-string values to strings.
        if isinstance(text, float):
            text = str(text)
        
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    # Apply the sentiment analysis function to the 'reviews' column and create a new 'sentiment' column.
    df['sentiment_TextBloB'] = df['reviews'].apply(get_sentiment_category)

    ##>>>>>>>>>> RASA ADD: inset dataset into csv, elasticsearch and add plot to pdf
    from utils import write_sentimential_dataset
    write_sentimential_dataset(df)

    from matplotlib.backends.backend_pdf import PdfPages
    pdf_pages = PdfPages(f'./files/plots.pdf')
    ##>>>>>>>>>> END OF RASA ADD

    # Calculate the confusion matrix
    confusion = confusion_matrix(df['rating_scale3'], df['sentiment_TextBloB'], labels=['positive', 'neutral', 'negative'])
    y_true=df['rating_scale3']
    y_pred=df['sentiment_TextBloB']

    confusion_matrix_df = pd.crosstab(df['rating_scale3'], df['sentiment_TextBloB'], rownames=['Actual'], colnames=['Predicted'])

    # Plot the confusion matrix
    sn.heatmap(confusion_matrix_df, annot=True, fmt='d')  # 'fmt' specifies format for the numbers
    plt.show()
    pdf_pages.savefig() ##>>> save plot
    MatchTextBlob = df['rating_scale3'] == df['sentiment_TextBloB']
    df
    rating_accuracy_textblob = (sum(MatchTextBlob) / len(df)) * 100
    print("Number of sentimental Analysis by TextBlob:", sum(MatchTextBlob))
    print("Number of dataset:", len(df))
    print(f"Accuracy percentage of sentimental by TextBlob {str(round(rating_accuracy_textblob, 2))}%")

    #2. Sentiment Analysis with Afinn¶
    afn = Afinn(emoticons=True) 
    sentiment = []  # This list will contain the sentiment scores

    # Loop through the reviews and calculate sentiment scores
    for g in range(len(df.reviews)):
        fg = afn.score(str(df.reviews[g]))
        sentiment.append(fg)
    df['sentiment_Afinn0']=sentiment
    threshold=1

    def get_sign(value):
        if value > threshold:
            return 'positive'
        elif value < -threshold:
            return 'negative'
        else:
            return 'neutral'

    # Apply the function to create a new column 
    #df['sentiment0']=sentiment 
    df['sentiment_Afinn'] = df['sentiment_Afinn0'].apply(get_sign)
    df.drop('sentiment_Afinn0', axis=1, inplace=True)


    ##>>>>>>>>>> RASA ADD: inset dataset into csv, elasticsearch and add plot to pdf
    write_sentimential_dataset(df)
    ##>>>>>>>>>> END OF RASA ADD


    # Calculate the confusion matrix
    confusion = confusion_matrix(df['rating_scale3'], df['sentiment_Afinn'], labels=['positive', 'neutral', 'negative'])
    y_true=df['rating_scale3']
    y_pred=df['sentiment_Afinn']

    confusion_matrix_df = pd.crosstab(df['rating_scale3'], df['sentiment_Afinn'], rownames=['Actual'], colnames=['Predicted'])

    # Plot the confusion matrix
    sn.heatmap(confusion_matrix_df, annot=True, fmt='d')  # 'fmt' specifies format for the numbers
    plt.show()
    pdf_pages.savefig() ##>>> save plot
    MatchAfinn = df['rating_scale3'] == df['sentiment_Afinn']
    df
    rating_accuracy_afinn = (sum(MatchAfinn) / len(df)) * 100
    print("Number of sentimental Analysis by Afinn:", sum(MatchAfinn))
    print("Number of dataset:", len(df))
    print(f"Accuracy percentage of sentimental by Afinn {str(round(rating_accuracy_afinn, 2))}%")

    #3.SentimentAnalysis with Vader

    # Initialize the sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Define a function to get sentiment labels
    def get_sentiment_label(text):
        vs = analyzer.polarity_scores(str(text))
        compound_score = vs["compound"]
        
        if compound_score > 0.1:
            return "positive"
        elif compound_score < -0.1:
            return "negative"
        else:
            return "neutral"

    # Apply the sentiment analysis function to the 'reviews' column and create the 'sentiment' column
    df['sentiment_Vader'] = df['reviews'].apply(get_sentiment_label)


    ##>>>>>>>>>> RASA ADD: inset dataset into csv, elasticsearch and add plot to pdf
    write_sentimential_dataset(df)
    ##>>>>>>>>>> END OF RASA ADD


    # Calculate the confusion matrix
    confusion = confusion_matrix(df['rating_scale3'], df['sentiment_Vader'], labels=['positive', 'neutral', 'negative'])
    y_true=df['rating_scale3']
    y_pred=df['sentiment_Vader']

    confusion_matrix_df = pd.crosstab(df['rating_scale3'], df['sentiment_Vader'], rownames=['Actual'], colnames=['Predicted'])

    # Plot the confusion matrix
    sn.heatmap(confusion_matrix_df, annot=True, fmt='d')  # 'fmt' specifies format for the numbers
    plt.show()
    pdf_pages.savefig() ##>>> save plot
    MatchVader = df['rating_scale3'] == df['sentiment_Vader']
    df
    rating_accuracy_vader = (sum(MatchVader) / len(df)) * 100
    print("Number of sentimental Analysis by Vader:", sum(MatchVader))
    print("Number of dataset:", len(df))
    print(f"Accuracy percentage of sentimental by Vader {str(round(rating_accuracy_vader, 2))}%")


    ##>>>>>>>>>> RASA ADD: inset dataset into csv, elasticsearch and add plot to pdf
    print("\n\nSentimental Analysis Result of All Models 'TextBlob, Afinn, Vader'")
    rating_counts = df['rating_scale3'].value_counts(normalize=True) * 100
    rating_counts_vader = df['sentiment_Vader'].value_counts(normalize=True) * 100
    rating_counts_afinn = df['sentiment_Afinn'].value_counts(normalize=True) * 100
    rating_counts_text_blob = df['sentiment_TextBloB'].value_counts(normalize=True) * 100
    sentimental_output = {"rating_counts": {"Overal": rating_counts.to_dict(), "sentiment_vader": rating_counts_vader.to_dict(), "sentiment_afinn": rating_counts_afinn.to_dict(), "sentiment_text_blob": rating_counts_text_blob.to_dict()},
                          "rating_accuracy": {"textblob_accuracy": rating_accuracy_textblob, "afinn_accuracy": rating_accuracy_afinn, "vader_accuracy": rating_accuracy_vader}}
    from pprint import pprint
    pprint(sentimental_output)

    from auth.server_authentication import elastic_authen
    client_conn = elastic_authen()
    resp = client_conn.index(index="sentimental_result", id=1,  document=sentimental_output)
    print(resp['result'])
    ##>>>>>>>>>> END OF RASA ADD
    

    # Filter the DataFrame for entries related to Amscot
    ams_df = df[df['company'] == 'Amscot']

    # Pie chart for ratings of Amscot
    ams_rating_counts = ams_df['rating'].value_counts()
    labels_rating = ams_rating_counts.index.tolist()
    sizes_rating = ams_rating_counts.values.tolist()

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)  # Creating the first subplot for ratings
    plt.pie(sizes_rating, labels=labels_rating, autopct='%1.1f%%', startangle=140)
    plt.title('Ratings Distribution for Amscot')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Pie chart for sentiment_Vader of Amscot
    ams_sentiment_counts = ams_df['sentiment_Vader'].value_counts()
    labels_sentiment = ams_sentiment_counts.index.tolist()
    sizes_sentiment = ams_sentiment_counts.values.tolist()

    plt.subplot(1, 2, 2)  # Creating the second subplot for sentiment_Vader
    plt.pie(sizes_sentiment, labels=labels_sentiment, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution for Amscot')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
    pdf_pages.savefig() ##>>> save plot

    # Calculating the average rating per country
    avg_rating_per_country = ams_df.groupby('country')['rating'].mean().reset_index()

    # Sorting the DataFrame by 'reviewer_rate' in ascending order
    avg_rating_per_country = avg_rating_per_country.sort_values(by='rating')

    # Plotting the results using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(avg_rating_per_country['country'], avg_rating_per_country['rating'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Average Rating')
    plt.title('Average Rating per Country for Amscot(Sorted)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pdf_pages.savefig() ##>>> save plot

    # Filter the DataFrame for entries related to Biz2Credit
    ams_df = df[df['company'] == 'Biz2Credit']

    # Pie chart for ratings of Amscot
    ams_rating_counts = ams_df['rating'].value_counts()
    labels_rating = ams_rating_counts.index.tolist()
    sizes_rating = ams_rating_counts.values.tolist()

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)  # Creating the first subplot for ratings
    plt.pie(sizes_rating, labels=labels_rating, autopct='%1.1f%%', startangle=140)
    plt.title('Ratings Distribution for Biz2Credit')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Pie chart for sentiment_Vader of Amscot
    ams_sentiment_counts = ams_df['sentiment_Vader'].value_counts()
    labels_sentiment = ams_sentiment_counts.index.tolist()
    sizes_sentiment = ams_sentiment_counts.values.tolist()

    plt.subplot(1, 2, 2)  # Creating the second subplot for sentiment_Vader
    plt.pie(sizes_sentiment, labels=labels_sentiment, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution for Biz2Credit')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
    pdf_pages.savefig() ##>>> save plot

    # Calculating the average rating per country
    avg_rating_per_country = ams_df.groupby('country')['rating'].mean().reset_index()

    # Sorting the DataFrame by 'reviewer_rate' in ascending order
    avg_rating_per_country = avg_rating_per_country.sort_values(by='rating')

    # Plotting the results using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(avg_rating_per_country['country'], avg_rating_per_country['rating'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Average Rating')
    plt.title('Average Rating per Country for Biz2Credit(Sorted)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pdf_pages.savefig() ##>>> save plot


    # Filter the DataFrame for entries related to Oportun
    ams_df = df[df['company'] == 'Oportun']

    # Pie chart for ratings of Amscot
    ams_rating_counts = ams_df['rating'].value_counts()
    labels_rating = ams_rating_counts.index.tolist()
    sizes_rating = ams_rating_counts.values.tolist()

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)  # Creating the first subplot for ratings
    plt.pie(sizes_rating, labels=labels_rating, autopct='%1.1f%%', startangle=140)
    plt.title('Ratings Distribution for Oportun')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Pie chart for sentiment_Vader of Amscot
    ams_sentiment_counts = ams_df['sentiment_Vader'].value_counts()
    labels_sentiment = ams_sentiment_counts.index.tolist()
    sizes_sentiment = ams_sentiment_counts.values.tolist()

    plt.subplot(1, 2, 2)  # Creating the second subplot for sentiment_Vader
    plt.pie(sizes_sentiment, labels=labels_sentiment, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution for Oportun')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
    pdf_pages.savefig() ##>>> save plot

    # Calculating the average rating per country
    avg_rating_per_country = ams_df.groupby('country')['rating'].mean().reset_index()

    # Sorting the DataFrame by 'reviewer_rate' in ascending order
    avg_rating_per_country = avg_rating_per_country.sort_values(by='rating')

    # Plotting the results using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(avg_rating_per_country['country'], avg_rating_per_country['rating'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Average Rating')
    plt.title('Average Rating per Country for Oportun (Sorted)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pdf_pages.savefig() ##>>> save plot


    ##=== Closing pdf file for store plots
    pdf_pages.close()


    # Save the PDF file to Elasticsearch
    from utils import save_pdf_to_elasticsearch
    res = save_pdf_to_elasticsearch()

    print(f"plots: {res['result']}")

    return sentimental_output
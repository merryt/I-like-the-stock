import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

reddit_client_ID = os.environ.get("reddit_client_ID")
reddit_secret_token = os.environ.get("reddit_secret_token")
reddit_username = os.environ.get("reddit_username")
reddit_password = os.environ.get("reddit_password")


import praw


reddit = praw.Reddit(client_id=reddit_client_ID,
                     client_secret=reddit_secret_token,
                     user_agent="I like the stock",
                     username=reddit_username,
                     password=reddit_password)

wsb = reddit.subreddit('wallstreetbets')

top_wsb_posts = wsb.hot(limit=10)

word_list = {}

boring_words = ["just","them","if","that","as","we","has","same","at", "it","it's","does","i've","of","is","my","me","a","em","go" "we", "do","are", "what", "i'm", "in", "the", "and","i", "every", "it", "for", "you", "your", "have", "they", "good", "great", "about", "luck"]

def breakAppartComment(comment, word_dict):
    quoteArray = comment.split()
    for word in quoteArray:
        word = word.lower()
        if word[-1] in [",", ".","!"]:
            word = word[0:-1]

        if word.lower() in boring_words:
            break

        if word in word_list:
            word_list[word] = word_list[word] + 1
        else:
            word_list[word] = 1

    return word_list


for post in top_wsb_posts:
    title = post.title
    breakAppartComment(title, word_list)
    for index, comment in enumerate(post.comments.list()):
        breakAppartComment(comment.body, word_list)
        for reply in comment.replies.list():
            if(type(reply) != praw.models.reddit.more.MoreComments):
                breakAppartComment(reply.body, word_list)    
        if index == 20:
            break


print(word_list)

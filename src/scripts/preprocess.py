import os
import re
import json

from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import *

tweet_tok = TweetTokenizer()
port_stem = PorterStemmer()

anime_season = "spring_2017"
data_path = os.path.join("..", "..", "data", anime_season)

stop_words = [
    "a", "above", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "been", "but", "by",
    "can", "could",
    "did", "do", "does",
    "each",
    "few", "for", "from",
    "had", "has", "have", "he", "her", "here", "him","himself", "his", "how",
    "i", "if", "in", "is", "it", "its", "itself",
    "just",
    "let",
    "me", "my", "myself",
    "no", "nor",
    "of", "off", "on", "once", "only", "or", "our", "ourselves", "out",
    "she", "so", "such",
    "than", "that", "the", "their", "them", "then", "they", "this", "those", "to", "too",
    "under", "up",
    "very",
    "was", "we", "what", "when", "where", "who", "why", "with", "would",
    "you", "your", "yourself"
]

link_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
non_alpha_pattern = "[^a-zA-Z]+"

for path in os.walk(data_path):
    anime_path = path[0]
    episode_paths = path[2]
    for ep in episode_paths:
        ep_path = os.path.join(anime_path, ep)
        ep_thread = json.load(open(ep_path))
        ep_links = []
        ep_comments = []
        ep_comments_meta = []
        for comment in ep_thread["comments"]:
            ep_comment_dict = {
                "score": comment["score"],
                "id": comment["id"],
                "pid": comment["pid"],
                "date": comment["date"],
                "depth": comment["depth"],
                "text": []
            }


            tokenized_comment = tweet_tok.tokenize(comment["text"])
            preprocessed_comment = []
            for tok in tokenized_comment:
                if re.match(link_pattern, tok):
                    ep_links.append(tok)
                else:
                    if len(tok) <= 2:
                        continue
                    elif tok in stop_words:
                        continue
                    else:
                        preprocessed_comment.append(tok.lower())

            preprocessed_comment = [port_stem.stem(tok) for tok in preprocessed_comment]
            preprocessed_comment = [re.sub(non_alpha_pattern, "", tok) for tok in preprocessed_comment]

            clean_comment = []
            for tok in preprocessed_comment:
                if len(tok) <= 2:
                    continue
                elif tok in stop_words:
                    continue
                else:
                    clean_comment.append(tok)

            ep_comment_dict["text"] = clean_comment
            ep_comments_meta.append(ep_comment_dict)

        anime_name = anime_path.split("/")[4]
        preprocessed_path = os.path.join("..", "..", "data", "preprocessed",
                                         anime_season, anime_name)

        if not os.path.exists(preprocessed_path):
            os.makedirs(preprocessed_path)

        submission_dict = {
            "score": ep_thread["score"],
            "id": ep_thread["id"],
            "num_comments": ep_thread["num_comments"],
            "date": ep_thread["date"],
            "comments": ep_comments_meta
        }

        submission_fname = os.path.join(preprocessed_path, ep)

        with open(submission_fname, 'w') as file:
            json.dump(submission_dict, file, indent=1, default=str)


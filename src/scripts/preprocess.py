# Preprocess the data via tokenizing comments, removing some stopwords, punctuation, etc
# Place into

import os
import json
import re

from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import *

tweet_tok = TweetTokenizer()
port_stem = PorterStemmer()

anime_season = "spring_2017"
data_path = os.path.join("..", "..", "data", anime_season)

stop_words = [
    "a", "above", "all", "also", "am", "an", "and", "any", "are", "as", "at",
    "be", "been", "but", "by",
    "can", "could",
    "did", "do", "does",
    "each",
    "few", "for", "from", "fuck",
    "get",
    "had", "has", "have", "he", "her", "here", "him","himself", "his", "how",
    "i", "if", "in", "is", "it", "its", "itself",
    "just",
    "let", "like", "lol",
    "me", "my", "myself",
    "no", "nor", "now",
    "of", "off", "on", "once", "one", "only", "or", "our", "ourselves", "out",
    "she", "so", "such",
    "than", "that", "the", "there", "their", "them", "then", "these", "they", "this", "those", "to", "too", "two",
    "under", "up",
    "very",
    "was", "we", "were", "what", "when", "where", "who", "why", "will", "with", "would",
    "you", "your", "yourself"
]

link_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
non_alpha_pattern = "[^a-zA-Z]+"


label_counter = 0

preprocessed_path = os.path.join("..", "..", "data", "preprocessed", anime_season)
if not os.path.exists(preprocessed_path):
    os.mkdir(preprocessed_path)

season_dict = {
    "season": 0,
    "year": 2017,
    "animes": []
}
season_animes = []

anime_id_mapping = {}

for path in os.walk(data_path):
    anime_path = path[0]
    episode_paths = path[2]

    if not episode_paths:
        continue
    else:
        anime_name = os.path.split(anime_path)[-1]

        anime_dict = {
            "anime_name": anime_name,
            "anime_id": label_counter,
            "ep_submissions": []
        }

        anime_id_mapping[label_counter] = anime_name

        label_counter += 1

        ep_submissions = []
        for ep in episode_paths:
            ep_path = os.path.join(anime_path, ep)
            ep_thread = json.load(open(ep_path))
            ep_links = []
            ep_comments = []
            ep_comments_meta = []
            ep_num = re.findall("\d+", ep)

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

            if not os.path.exists(preprocessed_path):
                os.makedirs(preprocessed_path)

            submission_dict = {
                "score": ep_thread["score"],
                "episode_num": ep_num,
                "id": ep_thread["id"],
                "num_comments": ep_thread["num_comments"],
                "date": ep_thread["date"],
                "comments": ep_comments_meta
            }

            ep_submissions.append(submission_dict)

        anime_dict["ep_submissions"] = ep_submissions

        preprocessed_anime_file = os.path.join(preprocessed_path, anime_name + ".json")

        with open(preprocessed_anime_file, "w") as file:
            json.dump(anime_dict, file, indent=1, default=str)

        season_animes.append(anime_dict)

season_dict["animes"] = season_animes

packaged_season_file = os.path.join(preprocessed_path, anime_season + ".json")
with open(packaged_season_file, "w") as file:
    json.dump(season_dict, file, indent=1, default=str)

anime_id_mapping_file = os.path.join(preprocessed_path, "anime_mapping.json")
with open(anime_id_mapping_file, "w") as file:
    json.dump(anime_id_mapping, file, indent=1, default=str)


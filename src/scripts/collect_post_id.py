import json

import praw

from my_secret import MySecret

reddit = praw.Reddit(client_id=MySecret.client_id,
                     client_secret=MySecret.client_secret,
                     redirect_uri='http://localhost:8080',
                     user_agent='collect_post_ids_script')

spring_2017_anime = [
    "shingeki no kyojin season 2",
    "boku no hero academia 2nd season",  # includes summer cour
    "eromanga-sensei",
    "rokudenashi majutsu koushi to akashic records",
    "re:creators",
    "boruto: naruto next generations",
    "dungeon ni deai wo motomeru no wa",
    "renai boukun",
    "tsuki ga kirei",
    "shuumatsu nani shitemasu ka?",
    "zero kara hajimeru mahou no sho",
    "busou shoujo machiavellianism",
    "shingeki no bahamut: virgin soul",
    "saenai heroine no sodatekata",
    "clockwork planet",
    "sakura quest",
    "granblue fantasy the animation",
    "sagrada reset",
    "alice to zouroku",
    "seikaisuru kado"
]

anime_posts = {}
anime_subreddit = reddit.subreddit("anime")
for anime in spring_2017_anime:
    posts = anime_subreddit.search(anime + " episode discussion",
                                   sort="new",
                                   time_filter="year")
    anime_posts[anime] = []
    for post in posts:
        anime_posts[anime].append(post.id)

with open('../../data/post_ids.json', 'w') as file:
    json.dump(anime_posts, file, indent=1)
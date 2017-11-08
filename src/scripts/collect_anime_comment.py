import json
import datetime
import praw
import os

from my_secret import MySecret

reddit = praw.Reddit(client_id=MySecret.client_id,
                     client_secret=MySecret.client_secret,
                     redirect_uri='http://localhost:8080',
                     user_agent='collect_post_ids_script')

data_path = os.path.join("..", "..", "data", "post_ids.json")
with open(data_path, "r") as data_file:
    anime_post_ids = json.load(data_file)


spring_2017_start = datetime.datetime.strptime("2017-04-01 00:00:00", "%Y-%m-%d %H:%M:%S")
spring_2017_end = datetime.datetime.strptime("2017-06-30 23:59:59", "%Y-%m-%d %H:%M:%S")



for anime in anime_post_ids:
    anime_name = anime.replace(" ", "_")
    anime_path = os.path.join("..", "..", "data", anime_name)
    if not os.path.exists(anime_path):
        os.makedirs(anime_path)

    idx = 1
    for post_id in anime_post_ids[anime]:
        submission = reddit.submission(id=post_id)

        sscore = submission.score
        sid = submission.id
        snum_comments = submission.num_comments
        sdate = datetime.datetime.fromtimestamp(submission.created_utc)

        if spring_2017_start <= sdate <= spring_2017_end:
            # Submission details -- will be turned to a JSON file
            submission_dict = {
                "score": sscore,
                "id": sid,
                "num_comments": snum_comments,
                "date": sdate,
                "comments": []
            }

            submission.comments.replace_more(limit=None)
            comment_stack = submission.comments[::-1]
            while comment_stack:
                comment = comment_stack.pop()

                cscore = comment.score
                cid = comment.id
                cpid = comment.parent_id
                cdate = datetime.datetime.fromtimestamp(comment.created_utc)
                cdepth = comment.depth
                ctext = comment.body

                # Appened to "comments"
                comment_dict = {
                    "score": cscore,
                    "id": cid,
                    "pid": cpid,
                    "date": cdate,
                    "depth": cdepth,
                    "text": ctext
                }

                submission_dict["comments"].append(comment_dict)

                comment_stack.extend(comment.replies)

            submission_fname = os.path.join(anime_path, "ep_" + str(idx))
            idx += 1

            with open(submission_fname, 'w') as file:
                json.dump(submission_dict, file, indent=1, default=str)






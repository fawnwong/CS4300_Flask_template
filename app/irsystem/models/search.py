import Levenshtein  # package python-Levenshtein

def edit_distance(query_str, msg_str):
    return Levenshtein.distance(query_str.lower(), msg_str.lower())

def similar_names(query, msgs):
    li = [(edit_distance(query, msg),msg) for msg in msgs]
    li.sort(key=lambda x: x[0])
    return li[0:5]

def bot_to_list(query, bot_names):
    edit_dist = similar_names(query, bot_names)
    data = [{"rank": "1", "list": [{"name": edit_dist[0][1], "comment": "A Comment 1", "link": "http://reddit.com/u/"+ edit_dist[0][1], "category": "bot_name"},
                                   {"name": "B Bot 1", "comment": "B Comment 1", "link": "http://www.google.com", "category": "bot_comments"},
                                   {"name": "C Bot 1", "comment": "C Comment 1", "link": "http://www.google.com", "category": "user_comments"}
                                   ]},
            {"rank": "2",
            "list": [
                     {"name": edit_dist[1][1], "comment": "A Comment 2", "link": "http://reddit.com/u/" + edit_dist[1][1], "category": "bot_name"},
                     {"name": "B Bot 2", "comment": "B Comment 2", "link": "http://www.google.com", "category": "bot_comments"},
                     {"name": "C Bot 2", "comment": "C Comment 2", "link": "http://www.google.com", "category": "user_comments"}
                     ]},
            {"rank": "3",
            "list": [
                     {"name": edit_dist[2][1], "comment": "A Comment 3", "link": "http://reddit.com/u/" + edit_dist[2][1], "category": "bot_name"},
                     {"name": "B Bot 3", "comment": "B Comment 3", "link": "http://www.google.com", "category": "bot_comments"},
                     {"name": "C Bot 3", "comment": "C Comment 3", "link": "http://www.google.com", "category": "user_comments"}
                     ]},
            {"rank": "4",
            "list": [
                     {"name": edit_dist[3][1], "comment": "A Comment 4", "link": "http://reddit.com/u/" + edit_dist[3][1], "category": "bot_name"},
                     {"name": "B Bot 4", "comment": "B Comment 4", "link": "http://www.google.com", "category": "bot_comments"},
                     {"name": "C Bot 4", "comment": "C Comment 4", "link": "http://www.google.com", "category": "user_comments"}
                     ]},
            {"rank": "5",
            "list": [
                     {"name": edit_dist[4][1], "comment": "A Comment 5", "link":"http://reddit.com/u/" + edit_dist[4][1], "category": "bot_name"},
                     {"name": "B Bot 5", "comment": "B Comment 5", "link": "http://www.google.com", "category": "bot_comments"},
                     {"name": "C Bot 5", "comment": "C Comment 5", "link": "http://www.google.com", "category": "user_comments"}
                     ]},
            ]
    return data



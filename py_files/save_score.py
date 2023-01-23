import pickle
import collections

Score = collections.namedtuple("Score", ["name", "score"])


def write_hs(name, score):
    new_scores = Score(name, score)
    try:
        with open("highscores.pkl", "rb") as in_:
            high_scores = pickle.load(in_)
    except (OSError, IOError) as e:
        high_scores = {}

    if new_scores.name not in high_scores:
        high_scores[new_scores.name] = new_scores.score
    elif new_scores.score > high_scores[new_scores.name]:
        high_scores[new_scores.name] = new_scores.score
    with open("highscores.pkl", "wb") as out:
        pickle.dump(high_scores, out)


def get_hs():
    with open("highscores.pkl", "rb") as in_:
        high_scores = pickle.load(in_)
    sorted_hs = sorted(high_scores, key=high_scores.get, reverse=True)
    return {name: high_scores[name] for name in sorted_hs}

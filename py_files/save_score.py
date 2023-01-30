import pickle


def write_hs(name: str, score: int):
    try:
        with open("highscores.pkl", "rb") as in_:
            high_scores: dict = pickle.load(in_)
    except (OSError, IOError):
        high_scores: dict = {}

    if name not in high_scores:
        high_scores[name] = score
    elif score > high_scores[name]:
        high_scores[name] = score
    with open("highscores.pkl", "wb") as out:
        pickle.dump(high_scores, out)


def get_hs() -> dict[str, int]:
    with open("highscores.pkl", "rb") as in_:
        high_scores: dict[str, int] = pickle.load(in_)
    sorted_hs: list[str] = sorted(high_scores, key=high_scores.get, reverse=True)
    return {name: high_scores[name] for name in sorted_hs}

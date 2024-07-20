import json


class Scores:
    def __init__(self):
        self.scores = self.read_scores()

    def read_scores(self):
        with open("./data/scores.jsonl") as f:
            scores = [json.loads(line) for line in f]
            return scores
        return {}

    def get_by_id(self, id: int):
        return [score for score in self.scores if score["id"] == id]

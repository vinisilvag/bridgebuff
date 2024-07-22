import json


class Scores:
    def __init__(self):
        self.scores = self.read_scores()

    def read_scores(self):
        with open("./data/scores.jsonl") as f:
            scores = []
            for line in f:
                processed = json.loads(line)
                if not processed.get("sunk_ships"):
                    processed["sunk_ships"] = 0
                if not processed.get("valid_shots"):
                    processed["valid_shots"] = 0
                if not processed.get("shot_received"):
                    processed["shot_received"] = 0
                scores.append(processed)
            return scores
        return {}

    def get_by_id(self, id: int):
        for score in self.scores:
            if score["id"] == id:
                return score
        return None

    def sorted_by_sunk(self):
        games_sorted = sorted(
            self.scores, key=lambda item: item["sunk_ships"], reverse=True
        )
        return games_sorted

    def sorted_by_escaped(self):
        games_sorted = sorted(self.scores, key=lambda item: item["escaped_ships"])
        return games_sorted

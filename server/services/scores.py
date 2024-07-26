import json


class Scores:
    def __init__(self):
        self.scores = self.read_scores()
        print("Scores: ", len(self.scores))
        self.highest_sunk = self.get_descending_by_sunk_ships()
        print("Highest sunk: ", len(self.highest_sunk))
        self.lowest_escaped = self.get_ascending_by_escaped_ships()

    def read_scores(self):
        with open("./data/scores.jsonl") as f:
            scores = [json.loads(line) for line in f]
            return scores
        return {}
    
    def get_highest_sunk(self):
        return self.highest_sunk
    
    def get_lowest_escaped(self):
        return self.lowest_escaped

    def get_by_id(self, id: int):
        for score in self.scores:
            if score["id"] == id:
                return score
        return None
    
    def get_descending_by_sunk_ships(self):
        # Sort the scores list in descending order based on the 'sunk_ships' key
        sorted_scores = sorted(self.scores, key=lambda score: score.get('sunk_ships', 0), reverse=True)
        
        return sorted_scores

        
    def get_ascending_by_escaped_ships(self):
        # ordena lista a partir dos menores 'escaped_ships'
        sorted_scores = sorted(self.scores, key=lambda x: x.get('escaped_ships', 0))
        
        return [score for score in sorted_scores]

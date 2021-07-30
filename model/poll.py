from typing import Dict, List

class Poll:

    OPTION_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    BAR_CHAR = "█"
    BAR_LENGTH = 20

    def __init__(self, message_id: int, question: str, options: List[str], votes: Dict = None):
        self.message_id = message_id
        self.question = question
        self.options = options 
        self.votes = {option: [] for option in options} if not votes else votes

    def get_vote_count(self, option: str) -> int:
        if option not in self.options:
            return 0 
        return len(self.votes[option])

    def get_total_vote_count(self) -> int:
        return sum([self.get_vote_count(option) for option in self.options])

    def get_vote_percentage(self, option: str) -> float:
        vote_count = self.get_vote_count(option)

        # avoid divide by zero
        return 0 if self.get_total_vote_count() == 0 else vote_count / self.get_total_vote_count()

    def add_vote(self, user_id: str, emoji: str) -> None:
        option = self._get_option(emoji)

        # only add vote if user has not already voted
        if user_id not in self.votes[option]:
            self.votes[option].append(user_id)

    def remove_vote(self, user_id: str, emoji: str) -> None:
        option = self._get_option(emoji)

        # only remove if user has voted
        if user_id in self.votes[option]:
            self.votes[option].remove(user_id)

    def get_emoji(self, option: str) -> str:
        return Poll.OPTION_EMOJIS[self.options.index(option)]

    def _get_option(self, emoji: str) -> str:
        # check if valid emoji
        if emoji not in self.OPTION_EMOJIS:
            return None

        option_index = Poll.OPTION_EMOJIS.index(emoji)

        # check if valid vote
        if option_index >= len(self.options):
            return None

        return self.options[option_index]

    @staticmethod
    def create_from(poll_dict: Dict) -> "Poll":
        return Poll(int(poll_dict["message_id"]), poll_dict["question"], poll_dict["options"], poll_dict["votes"])
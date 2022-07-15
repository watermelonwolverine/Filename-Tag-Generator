class Tag:
    def __init__(self,
                 letter_code: str,
                 full_name: str):
        self.letter_code = letter_code
        self.full_name = full_name

    def __lt__(self, other):
        if type(other) != Tag:
            raise Exception("Cannot compare")

        return self.full_name < other.full_name

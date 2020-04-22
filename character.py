COMMENT_CHARACTER = '@'


class Character:
    def __init__(self, character, character_index, line_number):
        self.character = character
        self.character_index = character_index
        self.line_number = line_number

    def __repr__(self):
        return '< {} >'.format(self.__str__())

    def __str__(self):
        return 'character: {}; character_index {}; line_number: {};'.format(self.character, self.character_index, self.line_number)

class Cell(object):

    displaySets = {'basic': {'liveChar': 'O', 'deadChar': '.'},
                    'squares': {'liveChar': '\u2B1B', 'deadChar': '\u2B1C'},
                    'soccer': {'liveChar': '\u26BD', 'deadChar': '\u2B1C'},
                    'at sign': {'liveChar': '@', 'deadChar': ' '},
                        'circles': {'liveChar': '\u26AB', 'deadChar': '\u26AA'}}

    currentDisplaySet = 'basic'

    liveChar = displaySets[currentDisplaySet]['liveChar']
    deadChar = displaySets[currentDisplaySet]['deadChar']

    @classmethod
    def set_display(cls, displaySet):
        """
        Given a currentDisplaySet that is a key of the displaySets, change the
        liveChar and deadChar class variables to the corresponding values for that
        displayset.
        :param displaySet: A key to the displaySets
        :return:
        """
        legalValues = cls.displaySets.keys()
        if displaySet in legalValues:
            cls.currentDisplaySet = displaySet
            cls.liveChar = cls.displaySets[displaySet]['liveChar']
            cls.deadChar = cls.displaySets[displaySet]['deadChar']
        else:
            raise ValueError(f'DisplaySet must be in {legalValues}.')

    @classmethod
    def set_display_user_values(cls, alive, dead):
        """
        Add an item to the displaySets for user defined characters.
        :param alive: character string that represents alive cells.
        :param dead: character string that represents dead cells.
        :return: None
        """
        numberOfCharacterSets = len(Cell.displaySets)
        key = f'user defined {numberOfCharacterSets}'
        Cell.displaySets[key] = {'liveChar': alive, 'deadChar': dead}


    def __init__(self, row, column):
        """Given a row and a column, creates a cell that knows its row,
           column, living (all cells start off with living as False), and
           neighbors (all cells start off with an empty list for neighbors)."""
        self.__row = row
        self.__column = column
        self.living = False
        self.__neighbors = []

    def __str__(self):
        """Returns either the liveChar or the deadChar for the Cell class
           depending on the state of the cell."""
        if self.living:
            return Cell.liveChar
        else:
            return Cell.deadChar

    def get_living(self):
        """Returns whether the cell is alive."""
        return self.living

    def set_living(self, state):
        """Sets whether the cell is alive or dead."""
        if isinstance(state, bool):
            self.living = state
        else:
            raise TypeError('state must be boolean.')

    def get_row(self):
        return self.__row

    def get_column(self):
        return self.__column

    def add_neighbor(self, cell):
        #
        # Print statement below is for debugging. Comment
        # out you know all the neighbors are working.
        #
        #print(f'{self.__repr__()} add neighbor {cell.__repr__()}')
        self.__neighbors.append(cell)

    def living_neighbors(self):
        neighborCount = 0
        for neighbor in self.__neighbors:
            if neighbor.get_living() == True:
                neighborCount += 1
        return neighborCount

    def __repr__(self):
        #
        # Here's a handy way to use if..else that we haven't talked about.
        #
        state = 'alive' if self.living else 'dead'
        return f'Cell({self.__row},{self.__column}) [{state}]'

    def debug(self):
        """Sometimes you just need to know about a cell."""
        neighbors = len(self.__neighbors)
        string = self.__repr__() + f' neighbors: {self.living_neighbors()}/{neighbors}'
        for neighbor in self.__neighbors:
            string += '\n     ' + neighbor.__repr__()
        print(string)
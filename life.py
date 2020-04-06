from world import World
from cell import Cell
import time
import os
import toolbox

class Life(object):

    speeds = [10, 7, 5, 3, 2, 1.5, 1, 0.75, 0.5, 0.25, 0.15, 0]

    def __init__(self):
        self.__world = World(34, 66)
        self.__fillrate = 25
        self.__speed = 5
        self.__delay = Life.speeds[self.__speed]
        self.__menu = 'main'
        self.random()

    def main(self):
        """
        Main event loop for store.
        :return: choice
        """
        command = 'help'
        parameter = None
        while command != 'quit':
            if command == 'help':
                self.help('help3.txt', 'Press <return> to continue. ')
                self.display()
            elif command == 'more menu':
                self.__menu = 'more'
                self.display()
            elif command == 'back to main menu':
                    self.__menu = 'main'
            elif command == 'run simulation':
                self.run_simulation(parameter)
            elif command == 'skip generations':
                self.skip_generations(parameter)
            elif command == 'random world':
                self.random()
                self.display()
            elif command == 'save world':
                self.save(parameter, './worlds/')
            elif command == 'open world':
                self.open(parameter, './worlds/')
            elif command == 'change fillrate':
                self.change_fillrate(parameter)
            elif command == 'change speed':
                self.change_speed(parameter)
            elif command == 'change size':
                self.change_size(parameter)
            elif command == 'change graphics':
                self.change_graphics(parameter)
            elif command == 'geometry':
                self.set_geometry()
            elif command == 'library':
                self.from_library(parameter, './library/')
            command, parameter = self.get_command()
        print('See ya, thanks for playing!')

    def menu(self):
        """
        returns a string containing the menu.
        :return: string containing the menu
        """
        return '[R]un  s[K]ip   [N]ew   [S]ave   [O]pen   [M]ore   [H]elp [L]ibrary   [Q]uit'

    def menu_more(self):
        """
        returns a string containing the menu.
        :return: string containing the menu
        """
        return 's[P]eed   [D]elay   s[I]ze   [G]raphics  g[E]ometry   [H]elp   [B]ack'

    def get_command(self):
        """
        Get a valid command from the user.
        :return: command
        """
        commands = {'r': 'run simulation',
                    'k': 'skip generations',
                    'n': 'random world',
                    's': 'save world',
                    'o': 'open world',
                    'f': 'change fillrate',
                    'p': 'change speed',
                    'i': 'change size',
                    'g': 'change graphics',
                    'e': 'geometry',
                    'l': 'library',
                    'm': 'more menu',
                    'b': 'back to main menu',
                    'h': 'help',
                    '?': 'help',
                    'q': 'quit'}

        validCommands = commands.keys()

        userInput = '&'
        parameter = None
        while userInput[0].lower() not in validCommands:
            userInput = input('Command: ')
            if userInput == '':
                userInput = 'n'
                parameter = 1
        command = commands[userInput[0].lower()]
        if len(userInput) > 1:
            parameter = userInput[1:].strip()
        return command, parameter

    def status(self):
        """
        Returns a string representing the status of the world.
        :return: string showing the status
        """
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        percentAlive = (self.__world.get_living_cell_count() / (rows * columns)) * 100
        string = 'Status:   '
        string += f'gen:{self.__world.get_generation()}   '
        string += f'speed: {self.__speed}   '
        string += f'size:[{rows}x{columns}]   '
        string += f'alive: {percentAlive:0.0f}%   '
        return string

    def help(self, filename, prompt = None):
        """
        Displays instructions.
        :param filename: help3.txt
        :param prompt:
        :return: None
        """
        with open(filename, 'r') as file:
            help = file.read()
        print(help, end='')
        if prompt:
            input('\n'+prompt)

    def next_generation(self, parameter):
        """
        Displays the next generation of the world
        :param parameter: parameter
        :return:
        """
        self.__world.next_generation()
        self.display()

    def run_simulation(self, generations):
        """
        Displays the next generation of the world
        :param generations:
        :return: next generation
        """
        if toolbox.is_integer(generations) and int(generations) > 0:
            generations = int(generations)
        else:
            prompt = 'How many generations do you want to do?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        for generation in range(generations):
            self.__world.next_generation()
            if self.__world.is_stable() == True:
                break
            string = self.__world.__str__()
            string += self.status()
            string += f'left: {generations - generation}'
            print(string)
            time.sleep(self.__delay)
        print(self.menu())

    def skip_generations(self, generations):
        """
        Displays the next generation of the world
        :param generations:
        :return: next generation
        """
        if toolbox.is_integer(generations) and int(generations) > 0:
            generations = int(generations)
        else:
            prompt = 'How many generations do you wanna skip?'
            generations = toolbox.get_integer_between(1, 10000, prompt)
        print(f'Skipping {generations} generations.', end='')
        while True:
            for generation in range(generations):
                self.__world.next_generation()
                self.__world.is_stable(self.__world)
                if generation % 100 == 0:
                    print('.', end='')
        print(' done!')
        time.sleep(2)
        self.display()

    def change_fillrate(self, fillrate):
        """
        Change the fillrate for the simulation.
        :param fillrate:
        :return: fillrate
        """
        if toolbox.is_number(fillrate) and 0 <= float(fillrate) <= 100:
            fillrate = float(fillrate)
        else:
            prompt = 'What percent of cells do you want to be alive?'
            fillrate = toolbox.get_integer_between(0,100,prompt)
        self.__fillrate = fillrate
        self.random()

    def change_speed(self, speed):
        """
        Change the delay betwen generations of the simulation.
        :param speed:
        :return: speed
        """
        if toolbox.is_number(speed):
            speed = int(speed)
        else:
            prompt = 'How fast should the generations update?'
            speed = toolbox.get_integer_between(0,11,prompt)
        self.__delay = Life.speeds[speed]

    def change_graphics(self, whichCharacters):
        """
        Change the live and dead characters for the cells.
        :param whichCharacters:
        :return: whichCharacters
        """
        if toolbox.is_integer(whichCharacters) and \
           1 <= int(whichCharacters) <= len(Cell.displaySets.keys()):
            whichCharacters = int(whichCharacters)
        else:
            print('**************************************')
            for number, set in enumerate(Cell.displaySets):
                liveChar = Cell.displaySets[set]['liveChar']
                deadChar = Cell.displaySets[set]['deadChar']
                print(f'{number+1}: living cells: {liveChar} dead cells: {deadChar}')
            print(f'{number + 2}: pick your own characters')
            print('**************************************')
            prompt = 'What character do you want to use?'
            whichCharacters = toolbox.get_integer_between(1, number + 2, prompt)
            if whichCharacters == number + 2:
                alive = toolbox.get_string('Which character should represent alive cells?')
                dead = toolbox.get_string('Which character should represent dead cells?')
                Cell.set_display_user_values(alive, dead)
        setString = list(Cell.displaySets.keys())[whichCharacters - 1]
        Cell.set_display(setString)
        self.display()

    def set_geometry(self):
        userGeo = toolbox.get_integer_between(1, 2, """
        Choose 1 or 2:
        1. bowl
        2. torus""")
        self.__world.set_geometry(userGeo)
        print(self.__world, end='')
        print(self.status() + '\n' + self.menu(), end='')

    def random(self):
        """
        Create a random world
        :return: world
        """
        self.__world.randomize(self.__fillrate)

    def save(self, filename, myPath='./'):
        """
        Save the current generation of the current world as a text file.
        :param filename: name of the file, may be None at this point.
        :param myPath: Where the file should be saved.
        :return: None
        """
        if filename == None:
            filename = toolbox.get_string('What do you wanna call the file? ')
        #
        # Make sure the file has the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        #
        # if the path doesn't already exist, create it.
        #
        if not os.path.isdir(myPath):
            os.mkdir(myPath)
        #
        # Add on the correct path for saving files if the user didn't
        # include it in the filename.
        #
        if filename[0:len(myPath)] != myPath:
            filename = myPath + filename
        self.__world.save(filename)

    def open(self, filename, myPath='./'):
        """
        open a text file and use it to populate a new world.
        :param filename: name of the file, may be None at this point.
        :param myPath: Where the file is located.
        :return: None
        """
        if filename == None:
            filename = toolbox.get_string('Which file do you wanna open?')
        #
        # Check for and add the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        allFiles = os.listdir(myPath)
        if filename not in allFiles:
            print('404: File not found...thanks for breaking the program, idiot.')
        else:
            #
            # Add on the correct path for saving files if the user didn't
            # include it in the filename.
            #
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            self.__world = World.from_file(filename)

    def change_size(self, parameter):
        if parameter and ('x' in parameter):
                rows, columns = parameter.split('x',2)
                if toolbox.is_integer(rows) and toolbox.is_integer(columns):
                    rows = int(rows)
                    columns = int(columns)
        else:
            prompt = 'How many rows of cells?'
            rows = toolbox.get_integer_between(1,40,prompt)
            prompt = 'How many cells in each row?'
            columns = toolbox.get_integer_between(1,120,prompt)
        self.__world = World(rows, columns)
        self.random()

    def display(self):
        """
        Prints the world, status bar and menu
        :return: None
        """
        if self.__menu == 'main':
            print(self.__world, self.status() + '\n' + self.menu())
        elif self.__menu == 'more':
            print(self.__world, self.status() + '\n' + self.menu_more())

    def long_l_world(self):
        """Create a blank world and put this pattern in the middle:
        ....
        .x..
        .x..
        .x..
        .xx.
        .... """
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        self.__world = World(rows, columns)

        middleRow = int(rows / 2)
        middleColumn = int(columns / 2)

        self.__world.set_cell(middleRow - 2, middleColumn, True)
        self.__world.set_cell(middleRow - 1, middleColumn, True)
        self.__world.set_cell(middleRow - 0, middleColumn, True)
        self.__world.set_cell(middleRow + 1, middleColumn, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 1, True)
        self.display()

    def acorn_world(self):
        """Create a blank world and put this pattern in the middle:
         .........
         ..x......
         ....x....
         .xx..xxx.
         .........
         """
        rows = self.__world.get_rows()
        columns = self.__world.get_columns()
        self.__world = World(rows, columns)

        middleRow = int(rows / 2)
        middleColumn = int(columns / 2)

        self.__world.set_cell(middleRow - 1, middleColumn - 2, True)
        self.__world.set_cell(middleRow - 0, middleColumn - 0, True)
        self.__world.set_cell(middleRow + 1, middleColumn - 3, True)
        self.__world.set_cell(middleRow + 1, middleColumn - 2, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 1, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 2, True)
        self.__world.set_cell(middleRow + 1, middleColumn + 3, True)
        self.display()

    def from_library(self, filename, myPath= './'):
        allFiles = os.listdir(myPath)
        if filename not in allFiles:
            for file in allFiles:
                print(file)
        if filename == None:
            filename = toolbox.get_string('Which world do you wanna use?')
        if filename[-5:] != '.life':
            filename = filename + '.life'
        else:
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            self.__world = World.from_file(filename)




if __name__ =='__main__':
    simulation = Life()
    simulation.main()
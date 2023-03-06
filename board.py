

class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """
    BOARD_LENGTH = 7
    VERTICAL = 0
    HORIZONTAL = 1
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'
    MOVES_MSG_DIR = {'u': "Can move up",
                     'd': "Can move down",
                     'l': "Can move left",
                     'r': "Can move right"}
    # You can change the board design here with the following static variables:
    EXIT_SYMBOL = 'EXIT'
    RIGHT_BORDER = "****"
    EMPTY_CELL_SIGN = '_'

    def __init__(self):
        """board variables"""
        self.__board_len = Board.BOARD_LENGTH
        self.__board_lst = [([Board.EMPTY_CELL_SIGN] * Board.BOARD_LENGTH + [None])
                            for i in range(Board.BOARD_LENGTH)]
        self.__cars_dir = {}
        self.__cars_locations = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        for i in range(Board.BOARD_LENGTH):
            self.__board_lst[i][Board.BOARD_LENGTH] = Board.RIGHT_BORDER
        self.__board_lst[3][7] = Board.EXIT_SYMBOL
        board = '\n'.join(map(' '.join, self.__board_lst))
        return str(board)

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        lst = []
        for i in range(self.__board_len):
            for j in range(self.__board_len):
                lst.append((i, j))
        lst.append((3, 7))
        return lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        legal_moves_lst = []
        cell_lst = self.cell_list()
        if self.__cars_dir:
            for car_tuple in self.__cars_dir.items():
                name = car_tuple[0]
                car = car_tuple[1]
                if self.check_car_moves(car, Board.UP, cell_lst):
                    legal_moves_lst.append((name, Board.UP, Board.MOVES_MSG_DIR.get(Board.UP)))
                if self.check_car_moves(car, Board.DOWN, cell_lst):
                    legal_moves_lst.append((name, Board.DOWN, Board.MOVES_MSG_DIR.get(Board.DOWN)))
                if self.check_car_moves(car, Board.LEFT, cell_lst):
                    legal_moves_lst.append((name, Board.LEFT, Board.MOVES_MSG_DIR.get(Board.LEFT)))
                if self.check_car_moves(car, Board.RIGHT, cell_lst):
                    legal_moves_lst.append((name, Board.RIGHT, Board.MOVES_MSG_DIR.get(Board.RIGHT)))
            return legal_moves_lst
        return []

    def check_car_moves(self, car, direction, cell_lst):
        """checks if the cell in the direction is empty and inside the board's limits."""
        """returns: True if the cell is ok, False if not."""
        direction_movements_lst = car.movement_requirements(direction)
        if direction_movements_lst:
            if direction_movements_lst[0] in cell_lst:
                for coordinates in direction_movements_lst:
                    if not self.cell_content(coordinates) or self.cell_content(coordinates) == Board.EXIT_SYMBOL:
                        return True
                    else:
                        return False
        return False

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        cell_lst = self.cell_list()
        # (3,7) is in the last cell of the list.
        return cell_lst[-1]

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if self.__board_lst[coordinate[0]][coordinate[1]] == "_":
            return
        else:
            # returns the name of the car in that cell
            return self.__board_lst[coordinate[0]][coordinate[1]]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        coord_lst = car.car_coordinates()
        cell_lst = self.cell_list()
        cars_locations = sum(self.__cars_locations.values(), [])  # makes a list of all the cars locations on the board.
        # checks if the car has legal length and name.
        if not coord_lst or car.get_name() in self.__cars_dir.keys():
            return False
        # checks if the coordination are in the board limits, and not on another car's location.
        for cord_tuple in coord_lst:
            if cord_tuple not in cell_lst or cord_tuple in cars_locations:
                return False
        # adds the car's location to the board and dictionaries.
        for cord_tuple in coord_lst:
            self.__board_lst[cord_tuple[0]][cord_tuple[1]] = car.get_name()  # changes the empty cells to the car's name.
        self.__cars_dir.update({car.get_name(): car})
        self.__cars_locations.update({car.get_name(): car.car_coordinates()})
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # find name of the car in the board:
        possible_moves = self.possible_moves()
        for car in self.__cars_dir.values():
            if name == car.get_name():
                for move in possible_moves:
                    if move[0] == name and move[1] == movekey:
                        # delete the previous first cell of the car:
                        for coordinates in self.__cars_locations.get(name):
                            row = coordinates[0]
                            col = coordinates[1]
                            self.__board_lst[row][col] = Board.EMPTY_CELL_SIGN
                        # implement the new coordinates and move the car on the board:
                        car.move(movekey)
                        self.__cars_locations[name] = car.car_coordinates()
                        for cords in self.__cars_locations[name]:
                            row = cords[0]
                            col = cords[1]
                            self.__board_lst[row][col] = name
                        return True
        return False

    def target_is_empty(self):
        """returns True if (3,7) is empty, False if a car is inside"""
        if self.target_location() not in self.__location_list():
            return True
        return False

    def __location_list(self):
        """makes a list of car locations"""
        location_lst = []
        for location in self.__cars_locations.values():
            for cord in location:
                location_lst.append(cord)
        return location_lst

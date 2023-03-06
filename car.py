
class Car:
    """
    Add class description here
    """
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'
    VERTICAL = 0
    HORIZONTAL = 1
    VERTICAL_DIR = {'u': 'can go up',
                    'd': 'can go down'}
    HORIZONTAL_DIR = {'l': 'can go left',
                      'r': 'can go right'}
    MOVES_DIR = {'u': (-1, 0),
                 'd': (1, 0),
                 'l': (0, -1),
                 'r': (0, 1)}

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coord_lst = [tuple(self.__location)]
        row = self.__location[0]
        col = self.__location[1]
        if self.__orientation == Car.VERTICAL and self.__length > 0:
            for car_length in range(self.__length-1):
                row += 1
                coord_lst.append((row, col))
        if self.__orientation == Car.HORIZONTAL and self.__length > 0:
            for car_length in range(self.__length-1):
                col += 1
                coord_lst.append((row, col))
        return coord_lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        if self.__orientation == Car.VERTICAL:
            return Car.VERTICAL_DIR
        if self.__orientation == Car.HORIZONTAL:
            return Car.HORIZONTAL_DIR

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if not self.__legal_movekey(movekey):
            return []
        coordinates_lst = self.car_coordinates()
        start_pos = coordinates_lst[0]  # a tuple of the first coordinates of the car
        end_pos = coordinates_lst[-1]   # a tuple of the last coordinates of the car
        if self.__orientation == Car.VERTICAL:
            if movekey == Car.UP:
                return [(start_pos[0] - 1, start_pos[1])]
            elif movekey == Car.DOWN:
                return [(end_pos[0] + 1, end_pos[1])]
        elif self.__orientation == Car.HORIZONTAL:
            if movekey == Car.LEFT:
                return [(start_pos[0], start_pos[1] - 1)]
            elif movekey == Car.RIGHT:
                return [(end_pos[0], end_pos[1] + 1)]

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if self.__legal_movekey(movekey):
            if movekey in Car.MOVES_DIR.keys():
                corrent_row = self.__location[0]
                corrent_col = self.__location[1]
                add_one_up_or_down = Car.MOVES_DIR.get(movekey)[0]
                add_one_left_or_right = Car.MOVES_DIR.get(movekey)[1]
                self.__location = (corrent_row + add_one_up_or_down, corrent_col + add_one_left_or_right)
                return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"
        return self.__name

    def __get_orientation(self):
        return self.__orientation

    def __legal_movekey(self, movekey):
        """Returns True if the move-key is legal"""
        if movekey in self.possible_moves().keys():
            return True
        return False

#####################################
# This uses origin shift to generate a random perfect maze of given size.
# Origin shift was created by CaptainLuma. Link to his video for explanation of how it works:
# https://www.youtube.com/watch?v=zbXKcDVV4G0
# The turtle implementation is done to represent the maze
########################################

import random
import sys


class Point:
    def __init__(self, pos: (int, int), outwards=tuple()) -> None:
        self.pos = list(pos)
        # [right, down, left, up]
        self.outwards = list(outwards)


class Maze:
    def __init__(self, size: (int, int) = (0, 0)) -> None:
        """
        initializes the maze object
        :param size: denotes the size of the maze
        """
        # size cannot be 1, 1 or less
        if size[0] + size[1] < 3:
            raise ValueError("Size has to be greater than (1, 1).")
        self.size = size
        self.maze = [[Point((i, j)) for i in range(size[0])] for j in range(size[1])]

        # setting the current root at the corner
        self.cur_root = [size[0]-1, 0]

        # putting None values for directions where propagation of origin is no longer possible
        for i in self.maze:
            for j in i:
                j.outwards = [1, 0, 0, 0]

        for i in self.maze:
            i[-1].outwards = [None, 1, 0, 0]

        for i in self.maze:
            i[0].outwards[2] = None

        for i in self.maze[-1]:
            i.outwards[1] = None

        for i in self.maze[0]:
            i.outwards[3] = None

    def create_new_root(self, seed: int = None) -> list[int, int]:
        """
        Shifts root of the map
        :param seed: seed for the randomizer
        :return: The new root
        """
        root = self.maze[self.cur_root[1]][self.cur_root[0]]
        choice = None
        direction = None
        # Chooses a  direction which is not None
        while choice is None:
            seed += 1
            random.seed(seed)
            direction = random.randint(0, 3)
            choice = root.outwards[direction]
        root.outwards[direction] = 1
        # Changes the current root on the basis of the chosen direction
        match direction:
            case 0:
                self.cur_root[0] += 1
            case 1:
                self.cur_root[1] += 1
            case 2:
                self.cur_root[0] -= 1
            case 3:
                self.cur_root[1] -= 1
        root = self.maze[self.cur_root[1]][self.cur_root[0]]
        # removes all the pointers from that node to make it a root
        for i in range(4):
            if root.outwards[i] == 1:
                root.outwards[i] = 0
        return self.cur_root

    def create_maze(self, seed: int = 0) -> tuple[list[list[Point]], int]:
        """
        Creates a new maze from the current maze state
        :param seed: Randomizer seed to get consistent results if needed
        :return: the maze and the seed in the form of a tuple
        """
        # generates random maze with random seed in case seed is given as 0
        for i in range(self.size[0]*self.size[1]*10):
            if seed == 0:
                seed = random.randrange(sys.maxsize)
                self.create_new_root(seed=seed)
            else:
                self.create_new_root(seed=i*seed)
        # in case you really like the seed, you can re-use it
        return self.maze, seed


# This main function is basically a demo
if __name__ == '__main__':
    import turtle

    # The commented part here helps in case the direction which each node is pointing to is required
    def draw_arrow():
        turtle.pendown()
        turtle.forward(length)
        # turtle.right(135)
        # turtle.forward(10)
        # turtle.back(10)
        # turtle.left(135)
        turtle.back(length)

    # draws all the points using turtle
    def point(points):
        # Since the origin in turtle is in bottom left, the maze has been flipped vertically to match
        for i in points[::-1]:
            for j in i:
                turtle.penup()
                turtle.goto(j.pos[0] * length - 500, j.pos[1] * length - 200)
                turtle.setheading(0)
                for k in j.outwards:
                    if k:
                        draw_arrow()
                    turtle.right(90)


    length = 100

    turtle.speed(0)

    turtle.hideturtle()

    obj = Maze((5, 5))
    # set seed as 0 for random
    maze, cur_seed = obj.create_maze(seed=0)
    print(f"{cur_seed = }")

    point(obj.maze)

    turtle.mainloop()

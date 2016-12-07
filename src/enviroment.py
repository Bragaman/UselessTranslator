import sys


class Robot:
    def __init__(self, x,y, count_tp, map):
        self.map = map
        self.x = x
        self.y = y
        self.count_tp = count_tp

    def move(self, move_x, move_y):
        new_x = self.x + move_x
        new_y = self.y + move_y
        size = len(self.map)
        if not (0 > new_x) and (new_x < size) and not new_y < 0 and new_y < size:
            if self.map[new_y][new_x]:
                self.x = new_x
                self.y = new_y
                return True
            else:
                return False
        else:
            return False

    def move_left(self):
        return self.move(-1, 0)

    def move_right(self):
        return self.move(1, 0)

    def move_forward(self):
        return self.move(0, 1)

    def move_back(self):
        return self.move(0, -1)




if __name__ == '__main__':
    lab = [[True, True, True, True],
           [True, False, False, True],
           [False, True, True, True],
           [True, False, False, True]
           ]

    robot = Robot(0, 0, 0, lab)
    l = []


    def dfs():
        if (robot.x, robot.y) not in l:
            print(robot.x, robot.y)
            l.append((robot.x, robot.y))
            if robot.move_back():
                dfs()
                robot.move_forward()
            if robot.move_forward():
                dfs()
                robot.move_back()
            if robot.move_left():
                dfs()
                robot.move_right()
            if robot.move_right():
                dfs()
                robot.move_left()

    # def dfs(x, y):
    #     if (x,y) not in l:
    #         print(x, y)
    #         l.append((x, y))
    #         robot.x = x
    #         robot.y = y
    #         if robot.move_back():
    #             dfs(x, y - 1)
    #             robot.move_forward()
    #         if robot.move_forward():
    #             dfs(x, y + 1)
    #             robot.move_back()
    #         if robot.move_left():
    #             dfs(x - 1, y)
    #             robot.move_right()
    #         if robot.move_right():
    #             dfs(x + 1, y)
    #             robot.move_left()

    dfs()
    # print(robot.move_forward())


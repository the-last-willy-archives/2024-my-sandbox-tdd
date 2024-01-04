class Grid:
    def __init__(self):
        self._arr = [["."] * self.width()] * self.height()

    def width(self) -> int:
        return 10

    def height(self) -> int:
        return 10

    def at(self, *, width, height):
        return self._arr[height][width]

    def print(self):
        for i in range(self.height()):
            print(self._arr[i])
        print()

    def has_obstacle_at(self, i, j):
        return self._arr[i][j] == "X"

    def add_obstacle_at(self, i, j):
        self._arr[i][j] = "X"


class State:
    def __init__(self, *, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

        self.is_halted = False

    def __str__(self):
        s = f"{self.x}:{self.y}:{self.dir}"
        if self.is_halted:
            s = "O:" + s
        return s


class Rover:
    def __init__(self, grid, state=None):
        self._grid = grid
        self._state = State(x=0, y=0, dir='N')

        if state is not None:
            self._set_state(state)

    def execute(self, commands):
        while len(commands) > 0:
            cmd = commands[0]
            commands = commands[1:]  # remove first command

            self._execute_once(cmd)

        return self.state()

    def _execute_once(self, cmd):
        actions = self._command_actions()
        if cmd not in actions:
            raise ValueError(f"unknown command `{cmd}`")
        else:
            actions[cmd]()

    def _command_actions(self):
        return {
            "L": self._turn_left,
            "M": self._move_forward,
            "R": self._turn_right,
        }

    def state(self):
        return str(self._state)

    def _set_state(self, state):
        comps = state.split(":")
        if len(comps) == 3:
            self._state.x = int(comps[0])
            self._state.y = int(comps[1])
            self._state.dir = comps[2]
        elif len(comps) == 4:
            self._state.is_halted = True
            self._state.x = int(comps[1])
            self._state.y = int(comps[2])
            self._state.dir = comps[3]

    def _move_forward(self):
        action = self._move_actions()[self._state.dir]
        action()

    def _move_actions(self):
        return {
            "E": self._move_east,
            "N": self._move_north,
            "S": self._move_south,
            "W": self._move_west,
        }

    def _move_east(self):
        self._move_toward(1, 0)

    def _move_north(self):
        self._move_toward(0, 1)

    def _move_south(self):
        self._move_toward(0, -1)

    def _move_west(self):
        self._move_toward(-1, 0)

    def _move_toward(self, x, y):
        if not self._state.is_halted:
            moved_x = (self._state.x + x) % self._grid.width()
            moved_y = (self._state.y + y) % self._grid.height()

            if self._grid.has_obstacle_at(moved_x, moved_y):
                self._state.is_halted = True
            else:
                self._state.x = moved_x
                self._state.y = moved_y

    def _turn_left(self):
        self._turn_counterclockwise(+1)

    def _turn_right(self):
        self._turn_counterclockwise(-1)

    def _turn_counterclockwise(self, signed_count):
        if not self._state.is_halted:
            dirs = ["E", "N", "W", "S"]
            idx = (dirs.index(self._state.dir) + signed_count) % len(dirs)
            self._state.dir = dirs[idx]

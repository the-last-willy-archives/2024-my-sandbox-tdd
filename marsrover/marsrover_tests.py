import marsrover
import unittest


class GridShould(unittest.TestCase):
    def test_have_width_of_10(self):
        grid = marsrover.Grid()
        self.assertEqual(grid.width(), 10)

    def test_have_height_of_10(self):
        grid = marsrover.Grid()
        self.assertEqual(grid.height(), 10)

    def test_should_be_filled_with_dots_by_default(self):
        grid = marsrover.Grid()
        for i in range(grid.width()):
            for j in range(grid.height()):
                self.assertEqual(grid.at(width=i, height=j), ".")

    def test_add_obstacle(self):
        grid = marsrover.Grid()
        self.assertFalse(grid.has_obstacle_at(2, 3))
        grid.add_obstacle_at(2, 3)
        self.assertTrue(grid.has_obstacle_at(2, 3))


class RoverTestCase(unittest.TestCase):
    def some_empty_grid(self):
        return marsrover.Grid()


class RoverShould(RoverTestCase):
    def test_face_north(self):
        rover = marsrover.Rover(self.some_empty_grid())
        self.assertEqual(rover.state(), "0:0:N")

    def test_move_for_each_move_command(self):
        rover = marsrover.Rover(self.some_empty_grid())
        self.assertEqual(rover.execute("MMM"), "0:3:N")

    def test_move_to_opposite_corner(self):
        rover = marsrover.Rover(self.some_empty_grid())
        self.assertEqual("9:9:N", rover.execute("RMLM" * 9))

    def test_raise_value_error_on_unknown_command(self):
        rover = marsrover.Rover(self.some_empty_grid())
        self.assertRaises(ValueError, rover.execute, "?")

    def subtest_start_with_state(self, state):
        rover = marsrover.Rover(self.some_empty_grid(), state=state)
        self.assertEqual(state, rover.state())

    def test_start_with_state(self):
        states = [
            "0:0:E",
            "0:0:N",
            "0:0:S",
            "0:0:W",
            "1:0:N",
            "9:0:N",
            "0:9:N",
            "5:6:S",
            "O:0:0:N",
        ]
        for s in states:
            with self.subTest(state=s):
                self.subtest_start_with_state(s)


class RoverShouldMove(RoverTestCase):
    def test_east(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:E")
        rover.execute("M")
        self.assertEqual("1:0:E", rover.state())

    def test_north(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:N")
        rover.execute("M")
        self.assertEqual("0:1:N", rover.state())

    def test_south(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:1:S")
        rover.execute("M")
        self.assertEqual("0:0:S", rover.state())

    def test_west(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="1:0:W")
        rover.execute("M")
        self.assertEqual("0:0:W", rover.state())

    def subtest_halt_on_obstacle(self, state, obstacle):
        grid = self.some_empty_grid()
        rover = marsrover.Rover(grid, state)

        grid.add_obstacle_at(*obstacle)

        rover.execute("M")
        self.assertEqual(rover.state(), f"O:{state}")

    def test_halt_on_obstacle(self):
        tests = [
            {"state": "0:0:E", "obstacle": [1, 0]},
            {"state": "0:0:N", "obstacle": [0, 1]},
            {"state": "0:1:S", "obstacle": [0, 0]},
            {"state": "1:0:W", "obstacle": [0, 0]},
        ]
        for t in tests:
            with self.subTest(**t):
                self.subtest_halt_on_obstacle(**t)


class RoverShouldTurn(RoverTestCase):
    def subtest_left_n_times(self, turn_count, expected_dir):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:N")
        rover.execute("L" * turn_count)
        self.assertEqual(
            f"0:0:{expected_dir}", rover.state(),
            msg=f"After {turn_count} left turns, the rover's facing should be `{expected_dir}`.")

    def test_left_n_times(self):
        self.subtest_left_n_times(1, "W")
        self.subtest_left_n_times(2, "S")
        self.subtest_left_n_times(3, "E")
        self.subtest_left_n_times(4, "N")

    def subtest_right_n_times(self, turn_count, expected_dir):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:N")
        rover.execute("R" * turn_count)
        self.assertEqual(
            f"0:0:{expected_dir}", rover.state(),
            msg=f"After {turn_count} right turns, the rover's facing should be `{expected_dir}`.")

    def test_right_n_times(self):
        self.subtest_right_n_times(1, "E")
        self.subtest_right_n_times(2, "S")
        self.subtest_right_n_times(3, "W")
        self.subtest_right_n_times(4, "N")


class RoverShouldWrap(RoverTestCase):
    def test_east(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="9:0:E")
        rover.execute("M")
        self.assertEqual("0:0:E", rover.state())

    def test_north(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:9:N")
        rover.execute("M")
        self.assertEqual("0:0:N", rover.state())

    def test_south(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:S")
        rover.execute("M")
        self.assertEqual("0:9:S", rover.state())

    def test_west(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="0:0:W")
        rover.execute("M")
        self.assertEqual("9:0:W", rover.state())


class HaltedRoverShould(RoverTestCase):
    def test_not_move(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="O:0:0:S")
        rover.execute("M")
        self.assertEqual("O:0:0:S", rover.state())

    def test_not_turn_left(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="O:0:0:S")
        rover.execute("L")
        self.assertEqual("O:0:0:S", rover.state())

    def test_not_turn_right(self):
        rover = marsrover.Rover(self.some_empty_grid(), state="O:0:0:S")
        rover.execute("R")
        self.assertEqual("O:0:0:S", rover.state())

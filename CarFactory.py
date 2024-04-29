import CarAdapter

class CarFactory:
    def get_car(self, width, length, front_left_pos, direction, wheels_max_turn, color="#14cc2d"):
        return CarAdapter.CarAdapter(width, length, front_left_pos, direction, wheels_max_turn, color=color)
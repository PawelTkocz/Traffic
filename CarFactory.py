import Car
import CarAdapter

class CarFactory:
    def get_car(self, width, length, start_x, start_y, direction, color="#14cc2d"):
        #return Car.Car(width, length, start_x, start_y, direction, color=color)
        return CarAdapter.CarAdapter(width, length, start_x, start_y, direction, color=color)
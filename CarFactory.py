import Car
import CarAdapter

class CarFactory:
    def get_car(self, width, height, start_x, start_y, color="#14cc2d"):
        #return Car.Car(width, height, start_x, start_y, color=color)
        car = Car.Car(width, height, start_x, start_y, color=color)
        return CarAdapter.CarAdapter(width, height, start_x, start_y, color=color)
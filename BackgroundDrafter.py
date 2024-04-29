import pygame

class BackgroundDrafter:
    """Class responsible for drawing background - the street, pavement, etc."""

    street_color = "#383838"
    pavement_color = "#6e6362"
    lines_color = "#c3dedd"
    pavement_width = 90
    parking_width = 250
    traffic_line_width = 260

    def __init__(self, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width

    def draw_dashed_line(self, line_len, line_width, space_len, position_y):
        offset_x = space_len // 2
        while offset_x < self.screen_width:
            pygame.draw.rect(self.screen, self.lines_color,
                             pygame.Rect(offset_x, position_y, line_len, line_width))
            offset_x += line_len + space_len

    def draw_center_line(self):
        self.draw_dashed_line(200, 25, 200, 
                              self.screen_height - self.parking_width - self.pavement_width - self.traffic_line_width)

    def draw_side_line(self):
        self.draw_dashed_line(100, 50, 100, self.screen_height - self.parking_width - self.pavement_width)      

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(self.street_color)
        pygame.draw.rect(self.screen, self.pavement_color, 
                         pygame.Rect(0, self.screen_height-self.pavement_width, self.screen_width, self.pavement_width))
        self.draw_side_line()
        self.draw_center_line()
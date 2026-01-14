import pygame

# Constants matching environment
BLOCK_SIZE = 20


class Snake:
    def __init__(self, start_x=300, start_y=300):
        self.segments = []
        self.create_snake(start_x, start_y)
        self.heading_angle = 0

    def create_snake(self, start_x, start_y):
        self.segments = [
            pygame.Rect(start_x, start_y, BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(start_x - BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(start_x - 2 * BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE)
        ]

    @property
    def head(self):
        return self.segments[0]

    # --- Compatibility Methods for Environment ---
    def get_head_x(self):
        return self.head.x

    def get_head_y(self):
        return self.head.y

    def get_heading(self):
        return self.heading_angle


    def reset(self):
        self.segments.clear()
        self.create_snake(300, 300)
        self.heading_angle = 0

    def extend(self):
        last_seg = self.segments[-1]
        self.segments.append(pygame.Rect(last_seg.x, last_seg.y, BLOCK_SIZE, BLOCK_SIZE))

    def move(self):
        # Move body segments
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i - 1].x
            self.segments[i].y = self.segments[i - 1].y

        # Move head based on current heading
        x = self.head.x
        y = self.head.y

        if self.heading_angle == 0:  # Right
            x += BLOCK_SIZE
        elif self.heading_angle == 90:  # Up (Negative Y in Pygame)
            y -= BLOCK_SIZE
        elif self.heading_angle == 180:  # Left
            x -= BLOCK_SIZE
        elif self.heading_angle == 270:  # Down (Positive Y in Pygame)
            y += BLOCK_SIZE

        self.head.x = x
        self.head.y = y

    def set_direction(self, angle):
        # Prevent 180 degree turns
        if angle == 0 and self.heading_angle != 180:
            self.heading_angle = 0
        elif angle == 90 and self.heading_angle != 270:
            self.heading_angle = 90
        elif angle == 180 and self.heading_angle != 0:
            self.heading_angle = 180
        elif angle == 270 and self.heading_angle != 90:
            self.heading_angle = 270

    def draw(self, surface):
        for segment in self.segments:
            pygame.draw.rect(surface, (255, 255, 255), segment)  # White snake
            # Optional: Draw a border for clarity
            pygame.draw.rect(surface, (0, 0, 0), segment, 1)
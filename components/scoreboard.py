import pygame

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.game_over_font = pygame.font.SysFont("Arial", 40)

    def update_scoreboard(self, surface):
        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        rect = text.get_rect(center=(300, 20)) # Top center
        surface.blit(text, rect)

    def add_score(self):
        self.score += 1

    def draw_game_over(self, surface):
        text = self.game_over_font.render("GAME OVER!", True, (255, 255, 255))
        rect = text.get_rect(center=(300, 300))
        surface.blit(text, rect)


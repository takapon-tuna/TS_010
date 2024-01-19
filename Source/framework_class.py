import pygame
import pygame_gui
from title_screen import show_title_screen
from game_play import show_game_screen
from game_over import show_game_over
from score_screen import show_score_screen


class Framework:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.manager = pygame_gui.UIManager(
            pygame.display.get_surface().get_size())
        self.clock = pygame.time.Clock()
        self.game_state = 'title'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

            self.manager.process_events(event)

            if self.game_state == 'title':
                if show_title_screen(self.screen, event):
                    self.game_state = 'game_play'
            elif self.game_state == 'game_play':
                result = show_game_screen(self.screen, event)
                if result == True:
                    self.game_state = 'game_over'
                elif result == 'quit':
                    pygame.quit()
                    return False
            elif self.game_state == 'game_over':
                if show_game_over(self.screen, event):
                    self.game_state = 'score_screen'
            elif self.game_state == 'score_screen':
                if show_score_screen(self.screen, event):
                    self.game_state = 'title'

        return True

    def update(self):
        time_delta = self.clock.tick(60)/1000.0
        self.manager.update(time_delta)

    def draw(self):
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def run(self):
        while self.handle_events():
            self.update()
            self.draw()


if __name__ == "__main__":
    framework = Framework()
    framework.run()

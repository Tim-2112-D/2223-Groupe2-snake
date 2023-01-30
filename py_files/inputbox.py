### thanks to skrx on stackoverflow
### https://stackoverflow.com/questions/46390231/
### how-can-i-create-a-text-input-box-with-pygame/46390412#46390412

import pygame
import py_files.constants as const


class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, text: str = ""):
        self.rect: pygame.Rect = pygame.Rect(x, y, w, h)
        self.color: str | pygame.Color = const.COLORS["INACTIVE"]
        self.text = text
        self.txt_surface: pygame.Surface = const.FONTS["LARGE"].render(
            text, True, self.color
        )
        self.active: bool = False

    def handle_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (
                const.COLORS["ACTIVE"] if self.active else const.COLORS["INACTIVE"]
            )
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = const.FONTS["LARGE"].render(
                    self.text, True, self.color
                )

    def update(self):
        width: int = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

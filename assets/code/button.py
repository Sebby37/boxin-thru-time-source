from . import spritesheet as spr
import pygame

class Button:
    def __init__(self, window: pygame.Surface, x: int, y: int):
        self.window = window
        self.x = x
        self.y = y
        self.ss = spr.Spritesheet(spr.resource_path("assets/images/button"))
        self.rect = pygame.Rect(self.x, self.y, 96, 32)
        self.on = False
    def update(self, time, boxes, future_boxes):
        # Code here
        for box in boxes:
            # If the box is in the current time
            if box.time_in == time:
                self.on = False
                if box.rect.colliderect(self.rect) and box.state != "grabbed":
                    self.on = True
                    break
        for box in future_boxes:
            if box.time_in == time:
                if not self.on:
                    self.on = False  # This line scuffs it if it's on on the above line 
                if box.rect.colliderect(self.rect) and box.state != "grabbed":
                    self.on = True
                    break
        # Code there
        self.window.blit(
            pygame.transform.scale(
                self.ss[f"{time}_{'pressed' if self.on else 'normal'}"][0], self.rect.size
            ), self.rect.topleft
        )

def all_buttons_pressed(buttons, time):
    if time != "present":
        return False
    for button in buttons:
        if not button.on:
            return False
    return True
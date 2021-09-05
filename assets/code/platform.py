from . import spritesheet as spr
import pygame

class Platform:
    def __init__(self, window, x, y, width, type=2):  # 1: yellow, 2: beam, width will be 1 unit per section
        self.window = window
        self.rect = pygame.Rect(x, y, 24*(width+2), 32)
        self.top_rect = pygame.Rect(x, y, 24*(width+2), 1)
        if type == 1:
            self.ss = spr.Spritesheet(spr.resource_path(f"assets/images/platform"))
        elif type == 2:
            self.ss = spr.Spritesheet(spr.resource_path(f"assets/images/platform2"))
        self.width = width

        # Loading the present images
        self.present_images = []
        self.present_images.append(self.ss["present_side"][0])
        for i in range(width):
            self.present_images.append(self.ss["present_body"][0])
        self.present_images.append(
            pygame.transform.flip(self.ss["present_side"][0], True, False)
        )

        # Loading the future images
        self.future_images = []
        self.future_images.append(self.ss["future_side"][0])
        for i in range(width):
            self.future_images.append(self.ss["future_body"][0])
        self.future_images.append(
            pygame.transform.flip(self.ss["future_side"][0], True, False)
        )

    def update(self, time):
        if time == "present":
            for i, platform in enumerate(self.present_images):
                self.window.blit(
                    pygame.transform.scale(
                        platform, (round(8*3), round(16*2))
                    ), (
                        self.rect.left + round(self.rect.width / (self.width+2)) * i, 
                        self.rect.top
                    )
                )
        elif time == "future":
            for i, platform in enumerate(self.future_images):
                self.window.blit(
                    pygame.transform.scale(
                        platform, (round(8*3), round(16*2))
                    ), (
                        self.rect.left + round(self.rect.width / (self.width+2)) * i, 
                        self.rect.top
                    )
                )
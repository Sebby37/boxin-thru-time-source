from . import spritesheet as spr
import pygame
from math import floor

'''
time: the time that is used for the box's sprite
timefrom: still figuring out exactly why I added this, however I believe it may have something to do with the below var
currentime: used for logic between moving it between present and future
'''

class Box:
    def __init__(self, window: pygame.Surface, x: int, y: int, time: str):
        self.window = window
        self.rect = pygame.Rect(x, y, 52, 52)
        self.ss = spr.Spritesheet(spr.resource_path("assets/images/box"))
        self.gravity = 0.5
        self.state = "grounded"  # Floor is at 518 pixels from top
        self.y_vel = 0
        self.time = time
        self.platform = None
        self.time_in = self.time
        #self.timefrom = self.time  # still figuring out why i added this, it may still be important
    def update(self, player, platforms):
        # Non-grabbed state handling
        if self.state != "grabbed":
            if self.rect.bottom < 518 or self.platform == None:
                self.state = "falling"
            if self.rect.bottom >= 518 or self.platform != None:
                self.state = "grounded"
            if self.state == "falling":
                self.y_vel -= self.gravity
                self.rect.top -= self.y_vel
            if self.state == "grounded":
                self.y_vel = 0
                if self.platform == None:
                    self.rect.bottom = 518
                else:
                    self.rect.bottom = self.platform.rect.top
        
        # Checking if the box is still colliding with the platform
        if self.platform != None:
            if (not self.rect.colliderect(self.platform.rect)) or (not self.rect.colliderect(self.platform.top_rect)):
                self.platform = None
        # Checking if the box collides with a platform
        for platform in platforms:
            if self.rect.colliderect(platform.top_rect):
                self.rect.bottom = platform.rect.top
                self.platform = platform
                break

        # Grabbed state handling
        if self.state == "grabbed" and player.grabbed_box == self:
            self.rect.center = (player.rect.centerx, player.rect.centery + 10)
        if player.rect.colliderect(self.rect):
            if player.grabbing and not player.has_box and player.grabbed_box != self:
                player.has_box = True
                self.state = "grabbed"
                player.grabbing = False
                player.grabbed_box = self
                spr.play_sfx(spr.resource_path("assets/sfx/grab_box.wav"))

        if player.grabbing and player.has_box and self.state == "grabbed" and player.grabbed_box == self:
            self.state = "falling"
            player.has_box = False
            player.grabbing = False
            player.grabbed_box = None

        # Blitting the box
        self.window.blit(
            pygame.transform.scale(
                self.ss[self.time][0], self.rect.size
            ), (self.rect.left, floor(self.rect.top))
        )

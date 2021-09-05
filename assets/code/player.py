from . import spritesheet as spr
import pygame
from math import floor

class Player:
    def __init__(self, window: pygame.Surface, x = 100, y = 426):
        self.window = window
        self.ss = spr.Spritesheet(spr.resource_path("assets/images/player"))
        self.keys = {
            "left" : False,
            "down" : False,
            "up" : False,
            "right" : False
        }
        self.player_index = 0
        self.player_state = "idle"
        self.rect = pygame.Rect(
            x,
            y,
            72,
            92
        )
        self.jumping_state = 0  # 0 for not jumping, 1 for pre jump, 2 for falling
        self.jumping = False
        self.gravity = 0.5
        self.y_vel = 0
        self.speed = 5
        self.prev_player_state = self.player_state
        self.facing_left = False

        # Box vars
        self.grabbing = False
        self.has_box = False
        self.grabbed_box = None
        self.on_platform = False
        self.platform = None
    def update(self, events, elapsed, platforms):
        # Updating the held keys
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.keys["left"] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.keys["down"] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.keys["up"] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.keys["right"] = True
                if event.key == pygame.K_e:
                    self.grabbing = True
                else:
                    self.grabbing = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.keys["left"] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.keys["down"] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.keys["up"] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.keys["right"] = False
        
        # Handling animation timing
        if self.player_state == "idle":
            if elapsed % 30 == 0:
                self.player_index += 1
        elif self.player_state == "run":
            if elapsed % 7 == 0:
                self.player_index += 1
        elif self.player_state == "pre-jump":
            if elapsed % 5 == 0:
                self.player_index += 1
            if self.player_index >= len(self.ss[self.player_state]):
                self.player_state = "jump"
        elif self.player_state == "jump" or self.player_state == "falling":
            if elapsed % 5 == 0:
                self.player_index += 1
        if self.player_index >= len(self.ss[self.player_state]) and self.player_state != "pre-jump":
            self.player_index = 0

        # Handling key press states
        if self.keys["left"] or self.keys["right"] and not self.jumping:
            self.player_state = "run"
        if not self.keys["left"] and not self.keys["down"] and not self.keys["up"] and not self.keys["right"] and not self.jumping:
            self.player_state = "idle"
        if self.keys["up"] and not self.jumping:
            self.player_state = "pre-jump"
            self.jumping = True
            self.y_vel = 10
            spr.play_sfx(spr.resource_path("assets/sfx/jump.wav"))
        
        # Edge of map handling
        if self.rect.left < 0:
            self.rect.left += self.speed
        if self.rect.right > 800:
            self.rect.right -= self.speed

        # Falling handling
        if not self.on_platform and self.rect.top < 426 and not self.jumping:
            self.jumping = True

        # Platform handling
        if self.platform != None:
            if self.on_platform and (self.rect.centerx < self.platform.rect.left or self.rect.centerx > self.platform.rect.right):
                self.on_platform = False
                self.falling = True
                self.platform = None
        for platform in platforms:
            # Handling platform exit conditions
            if self.rect.colliderect(platform.rect):
                # Handling collision similar to the ground, but with more pizas!
                if self.rect.bottom >= platform.rect.top and self.rect.top < platform.top_rect.bottom:
                    self.jumping = False
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_platform = True
                    self.platform = platform
                    continue
                # If the player is not on a platform, then we do some alternate collision handling
                if not self.on_platform:  # if NOT on platform
                    # Handling bottom collision
                    if self.rect.top < platform.rect.bottom and self.rect.top > platform.rect.centery:
                        self.y_vel = -10
                    # Handling side collision
                    if self.rect.right > platform.rect.left and self.rect.right < platform.rect.centerx: # Left side 
                        self.rect.left -= self.speed
                    if self.rect.left < platform.rect.right and self.rect.left > platform.rect.centerx: # Right side
                        self.rect.left  += self.speed
                break

        # Movement handling
        if self.keys["right"]:
            self.rect.left += self.speed
            self.facing_left = False
        elif self.keys["left"]:
            self.rect.left -= self.speed
            self.facing_left = True

        ''' Jump handling '''
        if self.jumping:
            self.rect.top -= self.y_vel
            self.y_vel -= self.gravity
        if self.rect.top >= 426:
            self.jumping = False
            self.rect.top = 426
            self.y_vel = 0
        #if self.on_platform:
        #    self.jumping = False
        #    self.y_vel
        if self.y_vel < 0:
            self.player_state = "falling"

        # Bliting the sprite
        if self.prev_player_state != self.player_state:  # Handling animation changes as to not cause index out of range errors
            self.player_index = 0
        self.window.blit(
            pygame.transform.scale(
                pygame.transform.flip (  # Flipping it every frame lags, consider replacing
                    self.ss[self.player_state][self.player_index], self.facing_left, False
                ), self.rect.size
            ), (self.rect.left, floor(self.rect.top))
        )
        self.prev_player_state = self.player_state
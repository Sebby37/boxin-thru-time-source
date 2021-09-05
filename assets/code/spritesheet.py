import pygame, sys
from json import load as json_load
from os import path

'''
The structure I have in mind:
{
    "idle" : [
        pygame.image,
        ect
    ]
}
'''

def Spritesheet(path): # path is the path to the image and json, without the file extension
    _orig_json = json_load(open(path + ".json"))
    _spritesheet = pygame.image.load(path + ".png")
    json = {}
    # Setting up the json
    for anim in _orig_json["frames"]:
        temp_data = [item for item in anim["filename"].split(" ")]  # Formatted as [anim_name, anim_index]
        json[temp_data[0]] = []
        
    # Adding the animations to the json
    for anim in _orig_json["frames"]:
        temp_data = [item for item in anim["filename"].split(" ")]  # Formatted as [anim_name, anim_index]
        json[
            temp_data[0]
        ].append(
            _spritesheet.subsurface(
                pygame.Rect(
                    anim["frame"]["x"],
                    anim["frame"]["y"],
                    anim["frame"]["w"],
                    anim["frame"]["h"]
                )
            )
        )
        
    return json

def draw_rect_alpha(window, rect=(0, 0, 800, 600), alpha=0.5, colour=(255, 255, 255)):  # Alpha is from 0 to 1
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    s.fill((colour[0], colour[1], colour[2], round(alpha*255)))
    window.blit(s, (rect[0], rect[1]))

# Currently unused, as most text has to be constantly changed
class Text:
    def __init__(self, window, x, y, text, user_font="Comic sans MS", size=15, colour=(0, 0, 0)):
        self.window = window
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(user_font, size)
        self.surface = self.font.render(text, False, colour)
    def update(self):
        self.window.blit(self.surface, (self.x, self.y))
        
def disp_text(window, x, y, text, user_font="Arial", size=35, colour=(0, 0, 0)):
    font = pygame.font.SysFont(user_font, size)
    surface = font.render(text, False, colour)
    window.blit(surface, (x, y))

def play_sfx(file: str):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Pyinstaller stuff
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)
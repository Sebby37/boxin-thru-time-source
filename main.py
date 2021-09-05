from traceback import format_exc
from datetime import datetime
from sys import exit as sys_exit

# Traceback stuff
try:
    import pygame
    from assets.code.spritesheet import Spritesheet, draw_rect_alpha, disp_text, resource_path
    from assets.code.player import Player
    from assets.code.box import Box
    from assets.code.button import Button, all_buttons_pressed
    from assets.code.platform import Platform
    from json import load as json_load
    pygame.init()
    pygame.mixer.init()

    bg = Spritesheet(resource_path("assets/images/background"))

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Boxin' Thru Time")
    pygame.display.set_icon(pygame.image.load(resource_path("assets/images/icon.png")))
    clock = pygame.time.Clock()
    elapsed = 0

    def level(data: dict):
        global elapsed
        # Background stuff
        bg_index = 0
        current_state = "present"
        switching = False
        alpha = 0
        alpha_increasing = True

        # Loading player
        player = Player(window, data["player"]["x"], data["player"]["y"])

        # Loading the boxes
        present_boxes = []
        for box in data["boxes"]:
            present_boxes.append(Box(window, box["x"], box["y"], "present"))
        future_boxes = []
        for box in present_boxes:
            future_boxes.append(Box(box.window, box.rect.left, box.rect.top, "future"))
        
        # Loading the buttons
        buttons = []
        for button in data["buttons"]:
            buttons.append(Button(window, button["x"], button["y"]))
        
        # Loading the platforms
        platforms = []
        for platform in data["platforms"]:
            platforms.append(Platform(window, platform["x"], platform["y"], platform["width"], platform["type"]))
        
        # Loading the text
        text_to_disp = data["text"]

        ms_from_last_frame = 0.0
        deltatime = ms_from_last_frame / (60/1000)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys_exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        switching = True

            # Background animation handling
            if elapsed % 20 == 0:
                bg_index += 1
            if bg_index >= len(bg[current_state]):
                bg_index = 0
            
            # Background switch handling
            if switching:
                alpha += 0.05 if alpha_increasing else -0.05
            if alpha > 1:
                alpha_increasing = False
                if current_state == "present":
                    current_state = "future"
                elif current_state == "future":
                    current_state = "present"
                bg_index = 0
                for box in future_boxes:
                    if box.state == "grabbed":
                        box.time_in = current_state
            if alpha < 0:
                switching = False
                alpha = 0
                alpha_increasing = True
            
            # Background blit
            window.blit(pygame.transform.scale(bg[current_state][bg_index], (800, 600)), (0, 0))
            # Player update
            player.update(events, elapsed, platforms)
            # Platform update
            for platform in platforms:
                platform.update(current_state)
            # Buttons update
            for button in buttons:
                button.update(current_state, present_boxes, future_boxes)
            if len(buttons) >= 1:
                if all_buttons_pressed(buttons, current_state):
                    return True
            # Boxes update
            if current_state == "present":
                for index, box in enumerate(present_boxes):
                    box.time = "present"
                    box.update(player, platforms)
                    # If the box is grabbed, then we alter the rect of the future box, otherwise do nothing
                    if box.state == "grabbed":
                        future_boxes[index].time_in = "future"
                        future_boxes[index].rect = pygame.Rect(box.rect.left, box.rect.top, box.rect.width, box.rect.height)

            for box in future_boxes:
                    box.time = "future"
                    # If we are in the future, or the box was moved to the present, update the box
                    if current_state == "future" or box.time_in == "present":
                        box.update(player, platforms)
                    
            # Alpha rect update
            draw_rect_alpha(window, alpha=alpha)

            # Text updates
            #disp_text(window, 0, 0, "FPS: " + str(round(clock.get_fps())), size=40, user_font="Arial")  # For FPS
            for txt in text_to_disp:
                disp_text(window, txt["x"], txt["y"], txt["text"], user_font=txt["font"], size=txt["size"], colour=tuple(txt["colour"]))
            

            # Final window updates
            ms_from_last_frame = clock.tick(60)
            deltatime = ms_from_last_frame / (1000/60)
            pygame.display.update()
            window.fill((0, 0, 0))
            elapsed += 1

    if __name__ == "__main__":
        for i in range(4):
            level(json_load(open(resource_path(f"assets/levels/level{i+1}.json"))))
        sys_exit(0)
except Exception as e:
    if e == SystemExit:
        sys_exit(0)
    current_time = datetime.now()
    current_time = current_time.strftime("%a, %d %b %Y %H;%M;%S")
    with open(f"Traceback {current_time}.txt", "w+") as traceback_file:
        traceback_file.write(f"Traceback {current_time}:\n{format_exc()}")
        traceback_file.close()
    sys_exit(1)
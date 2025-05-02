import pygame
import sys, time
import components, webcam, goober_selector, os
import goober



pygame.init()

# This is so that if you get rid of New Piskel.png the game crashes
guy = pygame.image.load("New Piskel.png")

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 1080
HEIGHT = 720
window = pygame.display.set_mode([WIDTH, HEIGHT])
c = pygame.time.Clock()

# A soup is a list of clickable objects (It stands for sprite group)
# soap stands for sprite Ohwow AwesomePicture
# CINEMA
# I could just use normal Pygame sprite groups but sunk cost fallacy or whatever
soup = []


guy = pygame.transform.scale(guy,(400,400))

# HELP ME! HEEELP!
def main_menu():
    window.fill((0, 0, 0))
    main_menu_soap = []
    window.blit(guy,(300,100))

    #b = components.generate_window(WIDTH / 2, 300, "Woke")

    #Make buttons
    x = 100
    y = 100
    width = 800
    height = 100

    play_button = components.Button(x, y, width, height, "gameplay loop", "Play", 3, main_menu_soap, 50)
    tutorial_button = components.Button(x, y + 250, width, height, "tutorial loop", "Tutorial", 3 ,main_menu_soap, 50 )

    main_menu_soap += [play_button,tutorial_button]


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for clickable in main_menu_soap:
                    response = clickable.mouse_click_behavior(x, y)
                    match response:
                        case "gameplay loop":
                            prelude_loop()

                        case "tutorial loop":
                            print("YAYY")

                    if response is not None:
                        break

        for thing in main_menu_soap:
            thing.render(window)

        pygame.display.flip()
        c.tick(30)

def prelude_loop():
    running = True
    dialogue = ["I heard you're the new Identifier.",
                "There's an Anomaly in my attic...",
                "Help me get it out!"]
    window_width = 350
    window_height = 350
    dialogue_window = components.generate_window_sprite(window_width, window_height, "INCOMING MESSAGE")
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))
    index = 0
    index_max = len(dialogue)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if index < index_max:
                    print(dialogue[index])
                    index += 1
                else:
                    running = False


        window.fill((0,0,0))
        window.blit(dialogue_window, (300,200))
        window.blit(sprite, (300,220))
        pygame.display.flip()
    game_loop()

def funeral(solution):
    return ["HE DIED LMAO!",
            "Trying to.." + solution,
            "What in tarnation. Why."]

def end_loop(solution, correct):
    running = True
    dialogue = ["You want me to " + solution + "..what..",
                "If you say so.",
                "I'll check in with you tomorrow."]
    if correct:
        response = ["Wow! It worked.",
                    "I'll come back to you if there's another.."]
    else:
        response = funeral(solution)

    window_width = 350
    window_height = 350
    dialogue_window = components.generate_window_sprite(window_width, window_height, "INCOMING MESSAGE")
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))
    index = 0
    response_index = 0
    index_max = len(dialogue)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if index < index_max:
                    print(dialogue[index])
                    index += 1
                else:
                    if response_index < len(response):
                        print(response[response_index])
                        response_index += 1
                    else:
                        running= False


        window.fill((0,0,0))
        window.blit(dialogue_window, (300,200))
        window.blit(sprite, (300,220))
        pygame.display.flip()
    main_menu()

def game_loop():
    soup = []
    window.fill((0,0,0))
    webcam_window = webcam.Webcam((WIDTH / 2, 20), window, soup)

    active_goober = webcam_window.display.active_goober

    start_frame_time = time.time()

    running = True
    while running:

        delta_time = time.time() - start_frame_time
        start_frame_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for clickable in soup:
                    response = clickable.mouse_click_behavior(x, y)

                    match response:
                        case "live":
                            solution = active_goober.solution
                            end_loop(solution, True)
                        case "die":
                            solution = active_goober.solution
                            end_loop(solution, False)

                    if response is not None:
                        break

        window.fill((33, 75, 65))
        webcam_window.render(window)


        # FPS counter
        components.TF_HEADER.render_to(window, (0, 0), str(int(1 / max(0.00001, delta_time))))

        pygame.display.flip()
        c.tick(30)




main_menu()

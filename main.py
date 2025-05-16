import pygame
import sys, time
import components, webcam, os
from dialogue_window import DialogueWindow



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

#creates main menu
def main_menu():
    window.fill((0, 0, 0))
    main_menu_soap = []
    window.blit(guy,(300,100))


    #Make buttons
    x = 100
    y = 100
    width = 800
    height = 100

    play_button = components.Button(x, y, width, height, "gameplay loop", "Play", 3, main_menu_soap, 50)

    main_menu_soap += [play_button]

    #running loop
    running = True
    while running:

        #if exited, close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #if one of the button is pressed, run the corresponding function
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for clickable in main_menu_soap:
                    response = clickable.mouse_click_behavior(x, y)
                    match response:
                        case "gameplay loop":
                            prelude_loop()

                    if response is not None:
                        break
        #render the maim menu
        for thing in main_menu_soap:
            thing.render(window)

        pygame.display.flip()
        c.tick(30)


# Loop for the opening cutscene
def prelude_loop():
    running = True

    # Dialogue, which the game iterates through
    dialogue = [""]
    window_width = 350
    window_height = 350

    dialogue_window = DialogueWindow((WIDTH/2, HEIGHT/2), dialogue)
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))

    # Determines which line of dialogue is the current one
    index = 0
    index_max = len(dialogue)
    while running:

        window.fill((33, 75, 90))
        dialogue_window.render((WIDTH/2, HEIGHT/2), window)
        dialogue_window.update()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Increments the text if the mouse is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = dialogue_window.mouse_click_behavior()

        # Renders everything
        pygame.display.flip()
        c.tick(30)

    # Begins the game loop once the introduction is finished
    game_loop()


#run the function if the user submitted wrong
def funeral(solution):
    return ["HE DIED LMAO!",
            "Trying to.." + solution,
            "What in tarnation. Why."]

#after the solution is submitted, see if the user is right
def end_loop(solution, correct):
    running = True
    dialogue = ["You want me to " + solution + "..what..",
                "If you say so.",
                "I'll check in with you tomorrow."]
    if correct:
        dialogue += ["Wow! It worked.",
                    "I'll come back to you if there's another.."]
    else:
        dialogue += funeral(solution)

    #create the dialogue window the person is talking through
    window_width = 350
    window_height = 350
    dialogue_window = DialogueWindow((WIDTH / 2, HEIGHT / 2), dialogue)
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))


    index = 0
    #run the dialogue loop
    index_max = len(dialogue)
    while running:

        window.fill((33, 75, 90))
        dialogue_window.render((WIDTH / 2, HEIGHT / 2), window)
        dialogue_window.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = dialogue_window.mouse_click_behavior()

        #update the window
        pygame.display.flip()
        c.tick(30)
    #go back to the main menu
    main_menu()

def game_loop():

    # Loop for clickable objects
    soup = []
    window.fill((0,0,0))
    webcam_window = webcam.Webcam((WIDTH / 2, 20), window, soup)

    active_goober = webcam_window.display.active_goober

    start_frame_time = time.time()

    running = True
    while running:

        # Controls the change in time for the debug frame rate renderer
        delta_time = time.time() - start_frame_time
        start_frame_time = time.time()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Checking for clickables if the player clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for clickable in soup:
                    response = clickable.mouse_click_behavior(x, y)

                    # Gets the response to the player's click
                    match response:

                        # If the player submits an anomaly, runs the ending cutscene
                        case "live":
                            solution = active_goober.solution
                            end_loop(solution, True)
                        case "die":
                            solution = active_goober.solution
                            end_loop(solution, False)

                    if response is not None:
                        break

        # Rendering
        window.fill((33, 75, 90))
        webcam_window.render(window)


        # FPS counter
        components.TF_HEADER.render_to(window, (0, 0), str(int(1 / max(0.00001, delta_time))))

        pygame.display.flip()
        c.tick(30)



# Starts the game in the main menu loop
main_menu()

import pygame
import sys, time
import components, webcam, os, json
from dialogue_window import DialogueWindow

MOUSE_DOWN = pygame.mixer.Sound(os.path.join("Assets", "Audio", "MouseDown.mp3"))
MOUSE_UP = pygame.mixer.Sound(os.path.join("Assets", "Audio", "MouseUp.mp3"))

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
with open("AnomalyData.json") as file:
    anomaly_data = json.load(file)

guy = pygame.transform.scale(guy,(400,400))


# HELP ME! HEEELP!

#creates main menu
def main_menu():
    main_menu_soap = []


    #Make buttons
    x = 100
    y = 100
    width = 800
    height = 100

    bg_window = components.generate_window_sprite(WIDTH - 50, HEIGHT - 70, "MAIN MENU")
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
                MOUSE_DOWN.play()
                x, y = pygame.mouse.get_pos()
                for clickable in main_menu_soap:
                    MOUSE_DOWN.play()
                    response = clickable.mouse_click_behavior(x, y)
                    match response:
                        case "gameplay loop":
                            prelude_loop()

                    if response is not None:
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                MOUSE_UP.play()
        #render the maim menu
        window.fill((33, 75, 90))
        window.blit(bg_window, (25, 25))
        for thing in main_menu_soap:
            thing.render(window)

        pygame.display.flip()
        c.tick(30)


# Loop for the opening cutscene
def prelude_loop():
    running = True

    # Dialogue, which the game iterates through
    dialogue = ["Hello? You there?",
                "Hi pookie!! I heard you got a job as an Identifier at that... whatever corporation you work at! Right?",
                "Well, uh, funny story, I've been hearing some scratching or something coming from my attic. It's getting really annoying.",
                "I heard you're trained on, like... identifying these \"anomaly\" things that keep appearing in people's houses just from their reaction to sound cues and things like that.",
                "So I got a camera and hooked up some stuff to it so you could, I dunno, do whatever you do in my house.",
                "Just, like, play whatever sound or whatever you gotta do in there, and tell me how to get rid of it. I'll pay you later.",
                "Thanks a bunch! Bye pookie!!!"]

    dialogue_window = DialogueWindow((WIDTH/2, HEIGHT/2), dialogue)
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))

    # Determines which line of dialogue is the current one
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
                MOUSE_DOWN.play()
                running = dialogue_window.mouse_click_behavior()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                MOUSE_UP.play()

        # Renders everything
        pygame.display.flip()
        c.tick(30)

    # Begins the game loop once the introduction is finished
    game_loop()


#run the function if the user submitted wrong
def funeral(goober):
    return ["(...)",
            "(The receiver is silent.)",
            goober.death_quote]

#after the solution is submitted, see if the user is right
def end_loop(goober, solution, correct):
    running = True
    dialogue = ["Hey, I read over the instructions you sent me, and this makes no sense at all.",
                "So I'm calling you about some noise in my attic, and then you tell me you want me to " + solution + "? What does that have to do with anything??",
                "I'm gonna go do whatever you said, but if it doesn't work, I'm never calling you again.",
                "(...)"]
    if correct:
        dialogue += ["Wow! It worked.",
                    "Thanks a bunch. I don't know how you came up with... THAT solution, but it worked, so whatever.",
                    "I'll call you back if anything else comes up, okay? Thanks!"]
    else:
        dialogue += funeral(goober)

    #create the dialogue window the person is talking through
    dialogue_window = DialogueWindow((WIDTH / 2, HEIGHT / 2), dialogue)
    sprite = pygame.image.load(os.path.join("Assets", "Sprites", "People", "the greechure.png"))
    sprite = pygame.transform.scale(sprite, (50,50))

    while running:

        window.fill((33, 75, 90))
        dialogue_window.render((WIDTH / 2, HEIGHT / 2), window)
        dialogue_window.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                MOUSE_DOWN.play()
                running = dialogue_window.mouse_click_behavior()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                MOUSE_UP.play()


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
                MOUSE_DOWN.play()
                x, y = pygame.mouse.get_pos()
                for clickable in soup:
                    response = clickable.mouse_click_behavior(x, y)

                    # Gets the response to the player's click
                    match response:

                        # If the player submits an anomaly, runs the ending cutscene
                        case "live":
                            solution = anomaly_data[webcam_window.anomaly_selector.selected_option]["Solution"]
                            end_loop(active_goober, solution, True)
                        case "die":
                            solution = anomaly_data[webcam_window.anomaly_selector.selected_option]["Solution"]
                            end_loop(active_goober, solution, False)

                    if response is not None:
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                MOUSE_UP.play()

        # Rendering
        window.fill((33, 75, 90))
        webcam_window.render(window)


        # FPS counter
        components.TF_HEADER.render_to(window, (0, 0), str(int(1 / max(0.00001, delta_time))))

        pygame.display.flip()
        c.tick(30)



# Starts the game in the main menu loop
main_menu()

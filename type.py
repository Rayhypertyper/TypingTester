import pygame # type: ignore
import random
import time
import sys

pygame.init()

#declaring basics
width, height = 1000, 600
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Typing Tester!")
surface = pygame.Surface((width, height), pygame.SRCALPHA)
timer = pygame.time.Clock()

text = open('sentences.txt', "r").read().split("\n")

#game variables
fps = 60
wpm = 0
accuracy = 100
high_score = 0
current_text = random.choice(text)
typed_text = ''
start_time = None
game_active = False

#fonts and images
bigfont = pygame.font.Font('Square.ttf', 100)
header_font = pygame.font.Font('Square.ttf', 50)
banner_font = pygame.font.Font('Square.ttf', 28)
gfont = pygame.font.Font('RobotoMono-Light.ttf', 21)
back_image = pygame.image.load('output-onlinepngtools.png')
back_image = pygame.transform.scale(back_image, (50, 50))
background_image = pygame.image.load('cluemoon.png')
background_image = pygame.transform.scale(background_image, (width, height))

#gui
def draw_screen():
    screen.fill('black')
    pygame.draw.rect(screen, (32, 42, 68), [0, height - 100, width, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, width, height], 5)
    pygame.draw.line(screen, 'white', (250, height - 100), (250, height), 2)
    pygame.draw.line(screen, 'white', (700, height - 100), (700, height), 2)
    pygame.draw.line(screen, 'white', (0, height - 100), (width, height - 100), 2)

    #displaying stats
    screen.blit(header_font.render(f'WPM: {wpm}', True, 'white'), (10, height - 75))
    screen.blit(header_font.render(f'Accuracy: {accuracy}%', True, 'white'), (270, height - 75))
    screen.blit(banner_font.render(f'Best: {high_score}WPM', True, 'white'), (400, 10))

    #displaying input
    screen.blit(gfont.render(current_text, True, 'white'), (50, 200))
    screen.blit(gfont.render(typed_text, True, 'green'), (50, 300))
    
#calculates words per minute
def calculate_wpm(typed_text, start_time):
    if start_time is None:
        return 0
    elapsed_time = time.time() - start_time
    word_count = len(typed_text.split())
    if elapsed_time == 0:
        return 0
    wpm = (word_count / elapsed_time) * 60
    return round(wpm)

#calculates accuracy
def calculate_accuracy(typed_text, current_text, correct, mistake):
    # correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(current_text) and c == current_text[i])
    # accuracy = (correct_chars / len(typed_text)) * 100 if typed_text else 100
    if mistake == 0:
        return 100
    accuracy = (correct/(correct+mistake)) * 100
    return round(accuracy)

#instructions
def instructions_menu():
    instructions = True
    while instructions:
        screen.fill((50, 50, 50))
        title_surface = header_font.render("Instructions", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(width // 2, 50))
        screen.blit(title_surface, title_rect)

        instructions_text = ["1. Type the displayed text as quickly and accurately as possible.",
            "2. As soon as a character is typed, the test begins.",
            "3. Your WPM (Words Per Minute) and accuracy is shown at the bottom.",
            "4. Press 'Enter' to submit your input and get a new text.",
            "5. Press 'Backspace' to correct mistakes.",
            "6. Click 'Reset' to start over.",
            "7. To return to menu, click the menu icon on the top right.",
            "8. Don't forget about capitals and punctuation!",
            "9. Have fun!"]
        
        #uniformly places each new element in list instructions_text into a new line in gui
        for i, line in enumerate(instructions_text):
            line_surface = gfont.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(topleft=(50, 150 + i * 30))
            screen.blit(line_surface, line_rect)


        #back button mechanics
        back_button = draw_button(screen, "Back", (width // 2 - 100, height - 100), (200, 50), (255, 255, 255), (200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return "menu"

        pygame.display.flip()
        timer.tick(fps)

#main menu
def main_menu():
    menu = True
    while menu:
        #main menu gui
        screen.blit(background_image, (0, 0))
        title_surface = bigfont.render("Typing Tester", True, (119,136,153))
        title_rect = title_surface.get_rect(center=(width // 2, height // 2 - 100))
        screen.blit(title_surface, title_rect)

        start_button = draw_button(screen, "Start", (width // 2 - 100, height // 2), (200, 50), (255, 255, 255), (200, 200, 200))
        instructions_button = draw_button(screen, "Instructions", (width // 2 - 200, height // 2 + 60), (400, 50), (255, 255, 255), (200, 200, 200))
        quit_button = draw_button(screen, "Quit", (width // 2 - 100, height // 2 + 120), (200, 50), (255, 255, 255), (200, 200, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        return "game"
                    elif instructions_button.collidepoint(event.pos):
                        return "instructions"
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        timer.tick(fps)

def draw_button(surface, text, position, size, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_surface = pygame.Surface(size)
    
    if pygame.Rect(position, size).collidepoint(mouse_pos):
        button_surface.fill(hover_color)  #hover color
    else:
        button_surface.fill(color)  #regular color
        
    pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, size[0], size[1]), 2)  #button border
    text_surface = header_font.render(text, True, (0, 0, 0)) #change font color for reset
    text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
    button_surface.blit(text_surface, text_rect)
    screen.blit(button_surface, position)
    return pygame.Rect(position, size)

main_menu()
# Main loop
state = "menu"
mistake = 0
correct = 0
while True:
    
        if state == "menu":
            state = main_menu()
        elif state == "instructions":
            state = instructions_menu()
        elif state == "game":
            run = True
            while run:
                timer.tick(fps)
                draw_screen()
                reset_button = draw_button(screen, "Reset", (750, height - 75), (200, 50),(255,255,255),(192,192,192))
                back_button_rect = screen.blit(back_image, (width - 60, 10))
                #red text for error and green text for correct
                if typed_text == current_text[:len(typed_text)]:
                    screen.blit(gfont.render(typed_text, True, 'green'), (50, 300))
                    correct+=1
                else:
                    screen.blit(gfont.render(typed_text, True, 'red'), (50, 300))
                    mistake+=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.KEYDOWN:
                        #if enter is pressed, a new text is displayed, program restarts without the program restarting
                        if event.key == pygame.K_RETURN:
                            current_text = random.choice(text)
                            typed_text = ""
                            start_time = None
                            typed_text = ""
                            current_text = random.choice(text)
                            start_time = None
                            wpm = 0
                            accuracy = 100
                            mistake = 0
                            correct = 0
                        #backspacing
                        elif event.key == pygame.K_BACKSPACE:
                            typed_text = typed_text[:-1]
                        else:
                            if start_time is None:
                                start_time = time.time()
                            typed_text += event.unicode
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and reset_button.collidepoint(event.pos):
                            #reset the game state
                            typed_text = ""
                            current_text = random.choice(text)
                            start_time = None
                            wpm = 0
                            accuracy = 100
                            mistake = 0
                            correct = 0
                        #working menu logo
                        elif back_button_rect.collidepoint(event.pos):
                            run = False
                            state = "menu"
                #tracking highest wpm
                if typed_text == current_text:
                    if wpm>high_score:
                        high_score = wpm  
                #displays stats
                elif typed_text:
                    wpm = calculate_wpm(typed_text, start_time)
                    accuracy = calculate_accuracy(typed_text, current_text, correct, mistake)
                pygame.display.flip()
            if state != "menu":
                break
pygame.quit()

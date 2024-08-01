"""
This program is responsible for displaying all of the graphics in the movie questionnaire
and returning the user inputs.
"""

import pygame

# Constants
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (3, 34, 105)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

SCREEN_X = 800
SCREEN_Y = 800
size = (800, 800)


def blit_text(surface: pygame.Surface, txt: str, start_point: tuple[int, int],
              font: pygame.font.Font, color=WHITE) -> None:
    """A function that puts words on the screen in lines. This way, no lines will
    run off the page.

    Preconditions:
        - 0 < start_point[0] < surface.get_width()
        - 0 < start_point[1] < surface.get_height()
    """
    words = [individual_word.split(' ') for individual_word in txt.splitlines()]
    space_character = font.size(' ')[0]
    max_width = surface.get_width()
    x, y = start_point
    line_height = 0
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color, BACKGROUND_COLOR)
            word_width, line_height = word_surface.get_size()
            if x + word_width >= max_width - SCREEN_X // 50:
                x = start_point[0]
                y += line_height
            surface.blit(word_surface, (x, y))
            x += word_width + space_character
        x = start_point[0]
        y += line_height


def age() -> int:
    """Create a pygame window that collects the user's age."""
    text = "How Old Are You?"
    pygame.init()
    smaller_size = (800, 200)

    screen = pygame.display.set_mode(smaller_size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 22)
    user_text = ''

    input_rect = pygame.Rect(SCREEN_X // 11, SCREEN_Y // 10, SCREEN_X - SCREEN_X // 5.5, SCREEN_Y // 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.isdigit() and 0 < int(user_text) <= 120:
                        pygame.quit()
                        return int(user_text)
                    else:
                        text = 'Enter A Valid Age In Years'
                else:
                    user_text += event.unicode

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, WHITE, input_rect, 2)

        title = my_font.render(text, True, WHITE, BACKGROUND_COLOR)
        screen.blit(title, (SCREEN_X // 11, SCREEN_Y // 22))

        typing_font = pygame.font.SysFont('timesnewroman', SCREEN_Y // 25)
        text_box = typing_font.render(user_text, True, WHITE)
        screen.blit(text_box, (SCREEN_X // 10, SCREEN_Y // 10))

        input_rect.width = max(text_box.get_width() + 10, SCREEN_X - SCREEN_X // 5.5)

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def movie_runtime() -> str:
    """Create a pygame window that collects the user's preferred movie runtime."""
    text = 'On Average, What Is Your Preferred Film Runtime?'
    pygame.init()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 18)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)
        image_background = pygame.Rect(SCREEN_X // 50, SCREEN_Y // 6, SCREEN_X - SCREEN_X // 25,
                                       SCREEN_Y - SCREEN_Y // 6 - SCREEN_Y // 9)
        pygame.draw.rect(screen, WHITE, image_background)
        blit_text(screen, text, (SCREEN_X // 50, SCREEN_Y // 50), my_font)

        button_y = SCREEN_Y - SCREEN_Y // 3
        button_width = SCREEN_X // 5
        button_height = SCREEN_Y // 10

        button1_x = SCREEN_X // 50 + SCREEN_X // 10
        button3_x = SCREEN_X - button1_x - button_width
        button2_x = (button1_x + button3_x) // 2

        button_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 50)
        mouse = pygame.mouse.get_pos()

        button1_color = GREEN if button1_x + button_width > mouse[0] > button1_x and button_y + button_height > mouse[1] > button_y else BACKGROUND_COLOR
        button2_color = GREEN if button2_x + button_width > mouse[0] > button2_x and button_y + button_height > mouse[1] > button_y else BACKGROUND_COLOR
        button3_color = GREEN if button3_x + button_width > mouse[0] > button3_x and button_y + button_height > mouse[1] > button_y else BACKGROUND_COLOR

        pygame.draw.rect(screen, button1_color, (button1_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, button2_color, (button2_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, button3_color, (button3_x, button_y, button_width, button_height))

        button1_text = button_font.render('< 80 Minutes', True, WHITE, button1_color)
        button2_text = button_font.render('In Between', True, WHITE, button2_color)
        button3_text = button_font.render('> 120 Minutes', True, WHITE, button3_color)

        button1_text_x = (button1_x + button1_x + button_width) // 2
        button2_text_x = (button2_x + button2_x + button_width) // 2
        button3_text_x = (button3_x + button3_x + button_width) // 2
        button_text_y = (button_y + button_y + button_height) // 2

        screen.blit(button1_text, button1_text.get_rect(center=(button1_text_x, button_text_y)))
        screen.blit(button2_text, button2_text.get_rect(center=(button2_text_x, button_text_y)))
        screen.blit(button3_text, button3_text.get_rect(center=(button3_text_x, button_text_y)))

        poster_1 = pygame.image.load('Images/Before_Sunset.jpeg').convert_alpha()
        poster_1 = pygame.transform.smoothscale(poster_1, (button_width, round(button_width * 1.5)))

        poster_2 = pygame.image.load('Images/Brooklyn.jpg').convert_alpha()
        poster_2 = pygame.transform.smoothscale(poster_2, (button_width, round(button_width * 1.5)))

        poster_3 = pygame.image.load('Images/Titanic.jpeg').convert_alpha()
        poster_3 = pygame.transform.smoothscale(poster_3, (button_width, round(button_width * 1.5)))

        screen.blit(poster_1, (button1_x, SCREEN_Y // 4))
        screen.blit(poster_2, (button2_x, SCREEN_Y // 4))
        screen.blit(poster_3, (button3_x, SCREEN_Y // 4))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_x + button_width > mouse[0] > button1_x and button_y + button_height > mouse[1] > button_y:
                    pygame.quit()
                    return 'short'
                elif button2_x + button_width > mouse[0] > button2_x and button_y + button_height > mouse[1] > button_y:
                    pygame.quit()
                    return 'medium'
                elif button3_x + button_width > mouse[0] > button3_x and button_y + button_height > mouse[1] > button_y:
                    pygame.quit()
                    return 'long'

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def oldest_years() -> int:
    """Create a pygame window that collects the user's preferred earliest movie release year."""
    text = 'Input The Earliest Possible Year of Release For A Movie You\'d Like To See'
    pygame.init()
    smaller_size = (800, 200)
    screen = pygame.display.set_mode(smaller_size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 25)
    user_text = ''

    input_rect = pygame.Rect(SCREEN_X // 11, SCREEN_Y // 7.5, SCREEN_X - SCREEN_X // 5.5, SCREEN_Y // 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.isdigit() and int(user_text) <= 2021:
                        pygame.quit()
                        return int(user_text)
                    else:
                        text = 'Please Enter A Valid Year of Release'
                else:
                    user_text += event.unicode

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, WHITE, input_rect, 2)

        blit_text(screen, text, (SCREEN_X // 22, SCREEN_Y // 50), my_font)

        typing_font = pygame.font.SysFont('timesnewroman', SCREEN_Y // 25)
        text_box = typing_font.render(user_text, True, WHITE)
        screen.blit(text_box, (SCREEN_X // 10, SCREEN_Y // 7.5))

        input_rect.width = max(text_box.get_width() + 10, SCREEN_X - SCREEN_X // 5.5)

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def newest_years(older_year: int) -> int:
    """Create a pygame window that collects the user's preferred latest movie release year."""
    text = 'Input The Newest Possible Year of Release For A Movie You\'d Like To See'
    pygame.init()
    smaller_size = (800, 200)
    screen = pygame.display.set_mode(smaller_size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 25)
    user_text = ''

    input_rect = pygame.Rect(SCREEN_X // 11, SCREEN_Y // 7.5, SCREEN_X - SCREEN_X // 5.5, SCREEN_Y // 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.isdigit() and 1900 <= int(user_text) <= 2021 and int(user_text) >= older_year:
                        pygame.quit()
                        return int(user_text)
                    else:
                        text = 'Please Enter A Possible Year of Release' if int(user_text) > 2021 or int(user_text) < 1900 else 'Year Entered Must Be Later Than The Earlier Year of Release Input'
                else:
                    user_text += event.unicode

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        blit_text(screen, text, (SCREEN_X // 22, SCREEN_Y // 50), my_font)

        typing_font = pygame.font.SysFont('timesnewroman', SCREEN_Y // 25)
        text_box = typing_font.render(user_text, True, WHITE)
        screen.blit(text_box, (SCREEN_X // 10, SCREEN_Y // 7.5))

        input_rect.width = max(text_box.get_width() + 10, SCREEN_X - SCREEN_X // 5.5)

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def languages() -> str:
    """Determine whether or not non-English films should be included in the final return value."""
    text = 'Are You Interested In Films Not In The English Language?'
    pygame.init()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 18)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)
        blit_text(screen, text, (SCREEN_X // 50, SCREEN_Y // 50), my_font)

        button_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 40)
        button1_text = 'YES'
        button2_text = 'NO'
        button1 = button_font.render(button1_text, True, BACKGROUND_COLOR)
        button2 = button_font.render(button2_text, True, BACKGROUND_COLOR)

        button1_x = SCREEN_X // 5
        button2_x = SCREEN_X * 3 // 5
        button_y = int(SCREEN_Y // 1.6)
        button_width = SCREEN_X // 5
        button_height = SCREEN_Y // 15

        button1_rect = button1.get_rect(center=((button1_x + button1_x + button_width) // 2,
                                                (button_y + button_y + button_height) // 2))

        button2_rect = button2.get_rect(center=((button2_x + button2_x + button_width) // 2,
                                                (button_y + button_y + button_height) // 2))

        mouse = pygame.mouse.get_pos()

        if button1_x + button_width > mouse[0] > button1_x and button_y + button_height > mouse[1] > button_y:
            pygame.draw.rect(screen, GREEN, (button1_x, button_y, button_width, button_height))
        else:
            pygame.draw.rect(screen, WHITE, (button1_x, button_y, button_width, button_height))

        if button2_x + button_width > mouse[0] > button2_x and button_y + button_height > mouse[1] > button_y:
            pygame.draw.rect(screen, GREEN, (button2_x, button_y, button_width, button_height))
        else:
            pygame.draw.rect(screen, WHITE, (button2_x, button_y, button_width, button_height))

        screen.blit(button1, button1_rect)
        screen.blit(button2, button2_rect)

        poster_1 = pygame.image.load('Images/Roma.jpg').convert_alpha()
        poster_1 = pygame.transform.smoothscale(poster_1, (button_width, round(button_width * 1.5)))

        poster_2 = pygame.image.load('Images/Amour.jpg').convert_alpha()
        poster_2 = pygame.transform.smoothscale(poster_2, (button_width, round(button_width * 1.5)))

        poster_3 = pygame.image.load('Images/8_half.jpeg').convert_alpha()
        poster_3 = pygame.transform.smoothscale(poster_3, (button_width, round(button_width * 1.5)))

        screen.blit(poster_1, (SCREEN_X // 50 + SCREEN_X // 10, SCREEN_Y // 4))
        screen.blit(poster_2, ((SCREEN_X - SCREEN_X // 50 - button_width) // 2, SCREEN_Y // 4))
        screen.blit(poster_3, (SCREEN_X - SCREEN_X // 50 - button_width - SCREEN_X // 10, SCREEN_Y // 4))

        caption_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 50)
        caption1_text = 'Roma (Spanish)'
        caption2_text = 'Amour (French)'
        caption3_text = '8 1/2 (Italian)'

        caption1 = caption_font.render(caption1_text, True, WHITE)
        caption1_square = caption1.get_rect(center=((SCREEN_X // 50 + SCREEN_X // 10 + (SCREEN_X // 50 + SCREEN_X // 10 + button_width)) // 2, SCREEN_Y // 1.75))

        caption2 = caption_font.render(caption2_text, True, WHITE)
        caption2_square = caption2.get_rect(center=(((SCREEN_X - SCREEN_X // 50 - button_width) // 2 + ((SCREEN_X - SCREEN_X // 50 - button_width) // 2 + button_width)) // 2, SCREEN_Y // 1.75))

        caption3 = caption_font.render(caption3_text, True, WHITE)
        caption3_square = caption3.get_rect(center=((SCREEN_X - SCREEN_X // 50 - button_width - SCREEN_X // 10 + (SCREEN_X - SCREEN_X // 50 - button_width - SCREEN_X // 10 + button_width)) // 2, SCREEN_Y // 1.75))

        screen.blit(caption1, caption1_square)
        screen.blit(caption2, caption2_square)
        screen.blit(caption3, caption3_square)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_x + button_width > mouse[0] > button1_x and button_y + button_height > mouse[1] > button_y:
                    pygame.quit()
                    return 'YES'
                elif button2_x + button_width > mouse[0] > button2_x and button_y + button_height > mouse[1] > button_y:
                    pygame.quit()
                    return 'NO'

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def genres(possible_genres: set[str]) -> set[str]:
    """Create a pygame window that collects the user's preferred movie genres.
    Number of clicks should be between 3 and 7.

    Preconditions:
        - 3 <= len(possible_genres) <= 30
    """
    text = 'Select Between 3 and 7 Genres You Like Below'
    pygame.init()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 25)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()

    returned_genres = set()
    box_width = SCREEN_X // 5
    box_height = SCREEN_Y // 10
    button_list = []
    button_coords_list = []
    button_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 40)

    while True:
        screen.fill(BACKGROUND_COLOR)
        blit_text(screen, text, (SCREEN_X // 50, SCREEN_Y // 25), my_font)

        box_x_start = 0
        box_y_start = SCREEN_Y * 2 // 10

        for genre in possible_genres:
            pygame.draw.rect(screen, WHITE, (box_x_start, box_y_start, box_width, box_height), 2)

            button_text = genre
            button = button_font.render(button_text, True, WHITE)
            button_box = button.get_rect(center=((box_x_start + box_x_start + box_width) // 2,
                                                 (box_y_start + box_y_start + box_height) // 2))
            screen.blit(button, button_box)

            button_list.append(button_text)
            button_coords_list.append((box_x_start, box_x_start + box_width, box_y_start, box_y_start + box_height))

            box_x_start += box_width
            if box_x_start == screen.get_width():
                box_x_start = 0
                box_y_start += box_height

        done_box_x_start = SCREEN_X // 2 - SCREEN_X // 8
        done_box_x_width = SCREEN_X // 4
        done_box_y_start = SCREEN_Y - SCREEN_Y // 10
        done_box_y_height = SCREEN_Y // 10

        if len(returned_genres) > 2:
            pygame.draw.rect(screen, WHITE, (done_box_x_start, done_box_y_start, done_box_x_width, done_box_y_height), 2)
            done_button_text = 'DONE'
            done_button = button_font.render(done_button_text, True, WHITE)
            done_button_box = done_button.get_rect(center=((done_box_x_start + done_box_x_start + done_box_x_width) // 2,
                                                           (done_box_y_start + done_box_y_start + done_box_y_height) // 2))
            screen.blit(done_button, done_button_box)

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(returned_genres) < 7:
                    for i in range(len(button_list)):
                        if button_coords_list[i][0] < mouse[0] < button_coords_list[i][1] and \
                                button_coords_list[i][2] < mouse[1] < button_coords_list[i][3]:
                            returned_genres.add(button_list[i])

                if len(returned_genres) > 2:  # this means the DONE button has shown up
                    if done_box_x_start < mouse[0] < done_box_y_start + done_box_x_width and \
                            done_box_y_start < mouse[1] < done_box_y_start + done_box_y_height:
                        pygame.quit()
                        return returned_genres

        # Refresh display
        pygame.display.flip()
        clock.tick(60)


def no_movies() -> None:
    """Display a message if no movies are found based on user preferences."""
    text = 'Sorry, but there were no movies found. Please try broadening your search requirements next time. Press "X" to close this window.'
    pygame.init()
    my_font = pygame.font.SysFont('couriernewbold', SCREEN_Y // 25)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Movie Questionnaire')
    clock = pygame.time.Clock()
    active = True

    while active:
        screen.fill(BACKGROUND_COLOR)
        blit_text(screen, text, (SCREEN_X // 10, SCREEN_Y // 3), my_font)

        # Refresh display
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                active = False

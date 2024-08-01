"""
This file is for the first part of our program where it displays 32 movies, and you
can click whether you like or dislike the movie. These liked movies are used to
calculate the recommended movies.
"""
from typing import Optional, Tuple, List
import pygame
from pygame.colordict import THECOLORS
import os
import scrape

# Constants
SCREEN_SIZE = (800, 800)  # (width, height)
GRID_SIZE = 8
NODE_HEIGHT = int(SCREEN_SIZE[0] / 20)
NODE_WIDTH = int(SCREEN_SIZE[0] / 10)
NODE_COLOR = (0, 0, 255)
LINE_COLOR = (255, 0, 0)

# Lists to store movie preferences
list_of_movies_like = []
list_of_movies_dislike = []
clicked = []
draw_lines_location = []
close = []
file_path = ['Google-Image-Scraper-master/photos/', 'Google-Image-Scraper-master/fastphotos/']
marked = []


def handle_mouse_click(done: bool, list_of_movies: List[str], event: pygame.event.Event,
                       screen_size: Tuple[int, int], clicked: List[int],
                       draw_lines_location: List[Tuple[Tuple[int, int], Tuple[int, int], bool]]) -> Tuple[List[str], List[str]]:
    """
    Handle mouse click events to rate movies as liked or disliked.
    Preconditions:
        - len(list_of_movies) > 0
        - clicked >= 0
        - screen_size[0] > 0 and screen_size[1] > 0
    """
    event_x = int(event.pos[0] // (screen_size[0] / GRID_SIZE))
    event_y = int(event.pos[1] // (screen_size[1] / GRID_SIZE))
    grid_number = (event_x + 1) + (event_y * 8)

    # If the Done button is clicked
    if (7 > event_x > 0 and 7 > event_y > 4) and (len(list_of_movies_like) >= 10 or done):
        pygame.display.quit()
        pygame.quit()
        close.append('close')
        return list_of_movies_like, list_of_movies_dislike
    elif done or event_y > 3:
        return list_of_movies_like, list_of_movies_dislike

    if grid_number not in clicked:
        clicked.append(grid_number)
        if event.button == 1:
            list_of_movies_like.append(list_of_movies[grid_number - 1])
            which_click = True
        elif event.button == 3:
            list_of_movies_dislike.append(list_of_movies[grid_number - 1])
            which_click = False

        x_coord = (event_x * screen_size[0] / 8) + 5
        y_coord = (event_y * screen_size[1] / 8) + 5
        draw_lines_location.extend([
            [(x_coord, y_coord), (x_coord - 5 + screen_size[0] / 8, y_coord), which_click],
            [(x_coord, y_coord), (x_coord, y_coord - 5 + screen_size[1] / 8), which_click],
            [(x_coord, y_coord - 5 + screen_size[1] / 8),
             (x_coord - 5 + screen_size[0] / 8, y_coord - 5 + screen_size[1] / 8), which_click],
            [(x_coord - 5 + screen_size[0] / 8, y_coord - 5 + screen_size[1] / 8),
             (x_coord - 5 + screen_size[0] / 8, y_coord), which_click]
        ])
    return list_of_movies_like, list_of_movies_dislike


def draw_done_button(done: bool, screen: pygame.Surface, pos: Tuple[int, int], pos2: Tuple[int, int],
                     screen_size: Tuple[int, int], finish: bool) -> None:
    """
    Draw the done button which allows users to finish rating movies after rating at least 10 movies.
    Preconditions:
        - pos[0] > 0 and pos[1] > 0
        - pos2[0] > 0 and pos2[1] > 0
        - screen_size[0] > 0 and screen_size[1] > 0
    """
    txt_x_pos, txt_y_pos = pos
    txt_x_pos2, txt_y_pos2 = pos2
    if done:
        poster_1 = pygame.image.load('Google-Image-Scraper-master/other_photos/finish.jpg').convert_alpha()
        poster_2 = pygame.image.load('Google-Image-Scraper-master/other_photos/recommended.png').convert_alpha()
    elif finish:
        poster_1 = pygame.image.load('Google-Image-Scraper-master/other_photos/done.jpg').convert_alpha()
        poster_2 = None
    else:
        poster_1 = pygame.image.load('Google-Image-Scraper-master/other_photos/notdone.jpg').convert_alpha()
        poster_2 = None

    poster_1 = pygame.transform.smoothscale(poster_1, (int(screen_size[0] / 8) * 6, int(screen_size[1] / 8) * 2))
    if done:
        poster_2 = pygame.transform.smoothscale(poster_2, (int(screen_size[0] / 8) * 4, int(screen_size[1] / 8) * 2))
    screen.blit(poster_1, [txt_x_pos, txt_y_pos])
    if done:
        screen.blit(poster_2, [txt_x_pos2, txt_y_pos2])


def draw_list(file: bool, draw_lines_location: List[Tuple[Tuple[int, int], Tuple[int, int], bool]],
              list_of_movies: List[str], done: bool, recommended_movies: List[Optional[str]],
              screen: pygame.Surface, screen_size: Tuple[int, int], show_grid: bool = False) -> None:
    """
    Draw the list of movies on the screen and handle the display of green/red boxes around rated movies.
    Preconditions:
        - len(draw_lines_location) >= 0
        - screen_size[0] > 0 and screen_size[1] > 0
    """
    list_of_posters = []
    path = file_path[1] if file else file_path[0]
    counter = 0

    if not close:
        string_filename = [filename.split(' movie')[0] for filename in os.listdir(path)]
        if not list_of_movies_like and not list_of_movies_dislike:
            temp_list = list_of_movies.copy()
            for _ in range(len(list_of_movies)):
                if not any(list_of_movies[_] in x or x in list_of_movies[_] for x in string_filename):
                    if list_of_movies[_] not in marked:
                        marked.append(list_of_movies[_])
                        temp_list.remove(list_of_movies[_])
            list_of_movies[:] = temp_list

        for filename in os.listdir(path):
            size_x = int(screen_size[0] / 8)
            size_y = int(screen_size[1] / 8)
            if done:
                size_x = int(screen_size[0] / 4)
                size_y = int(screen_size[1] / 4 * 1.5)
            if len(list_of_posters) == 32:
                break
            elif filename.endswith((".jpg", ".png")):
                poster_1 = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                poster_1 = pygame.transform.smoothscale(poster_1, (size_x, size_y))
                list_of_posters.append(poster_1)
            else:
                if filename not in marked:
                    marked.append(filename)
                counter += -1
            counter += 1

        picture_coords = [0, (screen_size[1] / 8) * 2] if done else [0, 0]
        for poster in list_of_posters:
            screen.blit(poster, picture_coords)
            picture_coords[0] += screen_size[0] / (4 if done else 8)
            if picture_coords[0] >= screen_size[0]:
                picture_coords[0] = 0
                picture_coords[1] += screen_size[1] / (4 * 1.5 if done else 8)

        if done:
            draw_done_button(True, screen, (int((screen_size[0] / 8) * 2), int((screen_size[1] / 8) * 8)),
                             (800 - int((screen_size[0] / 8) * 6), 0), screen_size, True)
        elif len(list_of_movies_like) >= 10:
            draw_done_button(False, screen, (int((screen_size[0] / 8)), int((screen_size[1] / 8) * 5)),
                             (int((screen_size[0] / 8)), 0), screen_size, True)
        else:
            draw_done_button(False, screen, (int((screen_size[0] / 8)), int((screen_size[1] / 8) * 5)),
                             (int((screen_size[0] / 8)), 0), screen_size, False)

        if not done:
            for coords in draw_lines_location:
                color = THECOLORS['green'] if coords[2] else THECOLORS['red']
                pygame.draw.line(screen, color, coords[0], coords[1], 5)

        if show_grid:
            draw_grid(screen)


def run_visualization(file: bool, draw_lines_location: List[Tuple[Tuple[int, int], Tuple[int, int], bool]],
                      list_of_movies: List[str], screen_size: Tuple[int, int],
                      show_grid: bool = False) -> Tuple[List[str], List[str]]:
    """
    Run the movie rating visualization.
    Preconditions:
        - len(list_of_movies) >= 0
        - len(draw_lines_location) >= 0
        - screen_size[0] > 0 and screen_size[1] > 0
    """
    screen = initialize_screen(screen_size, [pygame.MOUSEBUTTONDOWN])

    while True:
        draw_list(file, draw_lines_location, list_of_movies, False, [], screen, SCREEN_SIZE, show_grid)
        if not close:
            pygame.display.flip()
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(False, list_of_movies, event, screen.get_size(), clicked, draw_lines_location)
            elif event.type == pygame.QUIT:
                break
        else:
            break

    pygame.display.quit()
    return list_of_movies_like, list_of_movies_dislike


def show_movies(file: bool, draw_lines_location: List[Tuple[Tuple[int, int], Tuple[int, int], bool]],
                screen_size: Tuple[int, int], recommended_movies: List[Optional[str]],
                show_grid: bool = False) -> Tuple[List[str], List[str]]:
    """
    Display the recommended movies.
    Preconditions:
        - len(recommended_movies) >= 0
        - len(draw_lines_location) >= 0
        - screen_size[0] > 0 and screen_size[1] > 0
    """
    screen = initialize_screen(screen_size, [pygame.MOUSEBUTTONDOWN])

    while True:
        draw_list(False, draw_lines_location, recommended_movies, True, recommended_movies, screen, SCREEN_SIZE, show_grid)
        if not close:
            pygame.display.flip()
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(True, recommended_movies, event, screen.get_size(), clicked, draw_lines_location)
            elif event.type == pygame.QUIT:
                break
        else:
            break

    pygame.display.quit()
    return list_of_movies_like, list_of_movies_dislike


def run_function(list_of_movies: List[str], list_of_movies_search: List[str]) -> List[List[str]]:
    """
    Runs the program displaying a bunch of movies, where you click on the ones you like and dislike.
    """
    path = os.path.normpath(os.getcwd() + "\\Google-Image-Scraper-master\\photos")
    scrape.run_scrapy(list_of_movies_search, 1, (0, 0), (10000, 10000), path)
    run_visualization(False, draw_lines_location, list_of_movies, SCREEN_SIZE)
    close.pop()
    return [list_of_movies_like.copy(), list_of_movies_dislike.copy()]


def display_movies(recommended_movies: List[str], recommended_movies_search: List[str]) -> None:
    """
    Displays the recommended movies.
    """
    file_path.pop()
    file_path.insert(0, 'Google-Image-Scraper-master/final_images/')
    path = os.path.normpath(os.getcwd() + "\\Google-Image-Scraper-master\\final_images")
    scrape.run_scrapy(recommended_movies_search, 1, (0, 0), (10000, 10000), path)
    show_movies(False, draw_lines_location, SCREEN_SIZE, recommended_movies)


def run_function_fast(list_of_movies: List[str]) -> List[List[str]]:
    """
    Runs the program displaying a bunch of movies, where you click on the ones you like and dislike.
    This version doesn't include scraping, so it's faster.
    """
    run_visualization(True, draw_lines_location, list_of_movies, SCREEN_SIZE)
    close.pop()
    return [list_of_movies_like.copy(), list_of_movies_dislike.copy()]


################################################################################
# From here on, everything is from A1
################################################################################

def initialize_screen(screen_size: Tuple[int, int], allowed: List[int]) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill((3, 34, 105))
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: Tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 20)
    text_surface = font.render(text, True, THECOLORS['white'])
    width, height = text_surface.get_size()
    screen.blit(text_surface, pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_grid(screen: pygame.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    You can use this to help you check whether you are drawing nodes and edges in the right spots.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pygame.draw.line(screen, color, (0, y), (width, y))

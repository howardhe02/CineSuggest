"""
This file contains the MovieTree class which is used to recommend movies.
"""
from __future__ import annotations
from typing import Optional, List, Set
import csv


class MovieTree:
    """A subtree for a Movie Tree.

    Each node in the tree stores the kind of the node and the name of it.
    The kind of node is either a filter or a movie.
    The name of the node represents what is being filtered or the name of the movie.

    Instance Attributes:
        - kind: the type of this node, either a filter or a movie
        - name: the title of the filter or movie
        - score: the score of the movie

    Representation Invariants:
        - self.kind in {'filter', 'movie'}
        - self.name not in self._subtrees
        - 0.0 <= self.score <= 1.0
    """
    kind: str
    name: str
    score: Optional[float]

    # Private Instance Attributes:
    #   - _subtrees: the subtrees of this tree which represent another filter or movie recommendations
    _subtrees: List[MovieTree]

    def __init__(self, kind: str, name: str, score: float = 0.0) -> None:
        """Initialize a new game tree."""
        self.kind = kind
        self.name = name
        self.score = score
        self._subtrees = []

    def get_subtrees(self) -> List[MovieTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def add_subtree(self, subtree: MovieTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)

    def find_subtree_by_name(self, name: str) -> Optional[MovieTree]:
        """Return the subtree corresponding to the given name.

        Return None if no subtree corresponds to that name.
        """
        for subtree in self._subtrees:
            if subtree.name == name:
                return subtree
        return None

    def remove_subtrees(self, target: str) -> None:
        """Remove all nodes and their subtrees in the tree that have a name that is the same as the target.

        This checks all nodes of the tree.
        """
        self._subtrees = [subtree for subtree in self._subtrees if subtree.name != target]
        for subtree in self._subtrees:
            subtree.remove_subtrees(target)

    def new_score(self) -> float:
        """Update all the scores of the tree.

        If the node is a movie, return its score value. Otherwise, the score is equal to the sum of
        all child scores divided by the total number of children nodes.
        """
        if self.kind == "filter":
            if not self._subtrees:
                return self.score
            total_score = sum(subtree.new_score() for subtree in self._subtrees)
            self.score = total_score / len(self._subtrees)
        return self.score

    def find_best_movies(self, curr_list: List[str], total_movies: int, user_list: List[str],
                         depth: int = 0) -> List[str]:
        """Find the highest scoring subtrees and return a list of movies equal to the length of total_movies."""
        if depth == 5:
            return [movie.name for movie in self._subtrees]

        sorted_subtrees = sorted(self._subtrees, key=lambda subtree: subtree.score, reverse=True)
        movies_so_far = curr_list[:]
        final_list = []

        for subtree in sorted_subtrees:
            movies_so_far += subtree.find_best_movies(movies_so_far, total_movies, user_list, depth + 1)
            final_list.extend([x for x in movies_so_far if x not in final_list and x not in user_list])

            if len(final_list) >= total_movies:
                break
        return final_list[:total_movies]

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        indent = '  ' * depth
        if not self._subtrees:
            return f"{indent}{self.name}\n"
        return f"{indent}{self.name}\n" + ''.join(subtree._str_indented(depth + 1) for subtree in self._subtrees)

    def movie_filter(self, age: int, runtime: str, early_year: int, later_year: int,
                     genres: Set[str], non_english_languages: str, all_genres: Set[str],
                     all_languages: Set[str]) -> None:
        """Does all the necessary tree pruning given the user inputs.

        Preconditions:
            - 0 < age < 130
            - 3 <= len(genres) <= 7
            - runtime in {'short', 'medium', 'long'}
            - 1900 < early_year <= 2021
            - 1900 <= later_year <= 2021
            - non_english_languages in {'yes', 'no'}
        """
        if age < 18:
            self.remove_subtrees('18+')
        if age < 16:
            self.remove_subtrees('16+')
        if age < 13:
            self.remove_subtrees('13+')
        if age < 7:
            self.remove_subtrees('7+')

        if runtime == 'short':
            self.remove_subtrees('medium')
            self.remove_subtrees('long')
        elif runtime == 'medium':
            self.remove_subtrees('short')
            self.remove_subtrees('long')
        elif runtime == 'long':
            self.remove_subtrees('short')
            self.remove_subtrees('medium')

        for year in range(1900, early_year):
            self.remove_subtrees(str(year))
        for year in range(later_year + 1, 2022):
            self.remove_subtrees(str(year))

        if non_english_languages == 'no':
            all_languages.remove('English')
            for language in all_languages:
                self.remove_subtrees(language)

        for genre in all_genres:
            if genre not in genres:
                self.remove_subtrees(genre)


def load_movietree(read_file: str, liked_movies: List[str]) -> MovieTree:
    """Return a movie tree that is organized. The organization is defined in the add_subtree() function.

    The dataset must match the format on MoviesOnStreamingPlatforms_updated.csv.

    The nodes on the tree are either a filter or a movie. All movies are leaf nodes and all filters
    are parents, including the root.
    """
    root = MovieTree('filter', 'root')

    with open(read_file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            add_subtree(root, 0, row, liked_movies)
    return root

def add_subtree(curr_tree: MovieTree, depth: int, row: list, liked_movies: list) -> None:
    """Add the subtree based on the depth.

    If the subtree is not at depth 6, then the function adds a filter, otherwise, a movie is added.

    The function will check if a subtree with the filter name exists first; if it does, recurse into
    that subtree and check if the next filter exists and so on.

    If at any point, a filter does not exist with the name given by row[x], create a new subtree
    and recurse using that new subtree.

    The following tree should be organized as follows:
    depth 0: root
    depth 1: age (index[4])
    depth 2: duration (index[16])
    depth 3: genres (index[13])
    depth 4: year (index[3])
    depth 5: language (index[15])
    depth 6: movie (index[2])
    """
    if depth == 0:
        age_filter = row[4]
        if age_filter not in [title.name for title in curr_tree.get_subtrees()]:
            new_tree = MovieTree('filter', age_filter)
            curr_tree.add_subtree(new_tree)
        new_subtree = curr_tree.find_subtree_by_name(age_filter)
        add_subtree(new_subtree, 1, row, liked_movies)

    elif depth == 1:
        duration = 'unlisted'
        if row[16]:
            duration = 'short' if int(row[16]) <= 80 else 'medium' if int(row[16]) <= 120 else 'long'

        if duration not in [title.name for title in curr_tree.get_subtrees()]:
            new_tree = MovieTree('filter', duration)
            curr_tree.add_subtree(new_tree)
        new_subtree = curr_tree.find_subtree_by_name(duration)
        add_subtree(new_subtree, 2, row, liked_movies)

    elif depth == 2:
        genres = row[13].split(',')
        for genre in genres:
            if genre not in [title.name for title in curr_tree.get_subtrees()]:
                new_tree = MovieTree('filter', genre)
                curr_tree.add_subtree(new_tree)
        for genre in genres:
            new_subtree = curr_tree.find_subtree_by_name(genre)
            add_subtree(new_subtree, 3, row, liked_movies)

    elif depth == 3:
        year = row[3]
        if year not in [title.name for title in curr_tree.get_subtrees()]:
            new_tree = MovieTree('filter', year)
            curr_tree.add_subtree(new_tree)
        new_subtree = curr_tree.find_subtree_by_name(year)
        add_subtree(new_subtree, 4, row, liked_movies)

    elif depth == 4:
        languages = row[15].split(',')
        for language in languages:
            if language not in [title.name for title in curr_tree.get_subtrees()]:
                new_tree = MovieTree('filter', language)
                curr_tree.add_subtree(new_tree)
        for language in languages:
            new_subtree = curr_tree.find_subtree_by_name(language)
            add_subtree(new_subtree, 5, row, liked_movies)

    else:
        movie_title = row[2]
        if movie_title not in [title.name for title in curr_tree.get_subtrees()]:
            new_tree = MovieTree('movie', movie_title)
            if movie_title in liked_movies:
                new_tree.score = 1.0
            curr_tree.add_subtree(new_tree)


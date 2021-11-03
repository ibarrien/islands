"""
Given a 2-d binary square matrix "islands", find area of a given location.
Interpret 1 entries as valid and 0 invalid.
Area of location = size of location's component given by the equivalence relation:
whether up/down/left/right neighbor is valid.


Notes:
    Current approach is union find.
    Needs fix when (0,0) entry is 0.
    
@author: ibarrien
"""
from typing import Union, List
import pdb


class IslandsUF(object):
    """Weighted union find on islands matrix

    Notes
    -----
    This implementation asssumes square island matrix.
    """
    def __init__(self, islands: List[List[int]] = [[0]], valid_tile_val: int = 1):
        self.islands = islands
        self.N_dim = len(self.islands)  # assume square islands
        self.num_sites = self.N_dim**2 
        self.valid_tile_val = valid_tile_val  # i.e. valid site val
        self.uf_graph = list(range(self.num_sites))  # forest of trees
        self.uf_sizes = [0 for _ in range(self.num_sites)]
        self.already_counted_set = set([])

    def xy_to_1d(self, x: int, y: int) -> int:
        """Map 2d coords to 1d coord."""
        coord_in_1d = (self.N_dim * x) + y

        return coord_in_1d

    def is_tile(self, x: int, y: int) -> bool:
        """Check whether island location is valid."""
        if x >= self.N_dim or y >= self.N_dim:
            raise Exception("x=%d, y=%d pair out of bounds" % (x, y))
        return self.islands[x][y] == self.valid_tile_val

    def root(self, p: int) -> int:
        """Find root operation."""
        while p != self.uf_graph[p]:
            self.uf_graph[p] = self.uf_graph[self.uf_graph[p]]  # grandparent trick
            p = self.uf_graph[p]

        return self.uf_graph[p]

    def union(self, p: int, q: int) -> None:
        """Weighted union operation.
        
        ToDo: fix -- updating sizes not currently working for 0s leading upper diagonal
        """
        root_p = self.root(p)
        root_q = self.root(q)
        # pdb.set_trace()
        if self.uf_sizes[root_p] >= self.uf_sizes[root_q]:
            self.uf_graph[root_q] = root_p
            if root_q not in self.already_counted_set:
                self.uf_sizes[root_p] += self.uf_sizes[root_q]
                self.already_counted_set.update([root_q])
        else:
            self.uf_graph[root_p] = root_q
            if root_p not in self.already_counted_set:
                self.uf_sizes[root_q] += self.uf_sizes[root_p]
                self.already_counted_set.update([root_p])

        return None

    def _initialize_sizes(self):
        for r in range(self.N_dim):
            for c in range(self.N_dim):
                this_p = self.xy_to_1d(x=r, y=c)
                if not self.is_tile(x=r, y=c):
                    continue
                else:
                    self.uf_sizes[this_p] = 1
        return None

    def compute_island_areas(self) -> None:
        """Compute areas via union-find algo + join condition"""
        self._initialize_sizes()
        for r in range(self.N_dim):
            for c in range(self.N_dim):
                if not self.is_tile(x=r, y=c):
                    continue
                this_p = self.xy_to_1d(x=r, y=c)
                self.already_counted_set.update([this_p])

                # check up
                if r > 0:
                    if self.is_tile(x=r-1, y=c):
                        this_q = self.xy_to_1d(x=r-1, y=c)
                        self.union(p=this_p, q=this_q)
                # check down
                if r < self.N_dim - 1:
                    if self.is_tile(x=r+1, y=c):
                        this_q = self.xy_to_1d(x=r+1, y=c)
                        self.union(p=this_p, q=this_q)
                # check left
                if c > 0:
                    if self.is_tile(x=r, y=c-1):
                        this_q = self.xy_to_1d(x=r, y=c-1)
                        self.union(p=this_p, q=this_q)
                # check right
                if c < self.N_dim - 1:
                    if self.is_tile(x=r, y=c + 1):
                        this_q = self.xy_to_1d(x=r, y=c + 1)
                        self.union(p=this_p, q=this_q)

        return None

    def get_area(self, x: int, y: int) -> int:
        """Area of a location on island."""
        coord_1d = self.xy_to_1d(x=x, y=y)
        this_root = self.uf_graph[coord_1d]
        return self.uf_sizes[this_root]

    def print_all_areas(self) -> None:
        """Print each location's area computed by union find.
        Notes:
            Useful for testing
        """
        for r in range(self.N_dim):
            for c in range(self.N_dim):
                print("Area of (%d, %d): %d" % (r, c, self.get_area(r, c)))
        
        return None



# TEST CASES
islands_1 = [[1, 0],
             [1, 0]]

islands_2 = [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]]

islands_3 = [[0, 1],
             [1, 1]]

islands_4 = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]

islands_5 = [[1, 0, 1],
             [1, 0, 0],
             [1, 1, 1]]

islands_6 = [[0, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]

test_islands = islands_5
iuf = IslandsUF(islands=test_islands)
iuf.compute_island_areas()
print(iuf.print_all_areas())


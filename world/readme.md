* Author: Peter Hofland *
* Date: 12-9-2021       *
* Time: 03:00 AM        *
* File: Hashmaps.py     *

Hashmaps are setup like this: (hashmaps form the world/grid of the world)

    - Basic grid dictionary containing all the cells as values and their location as keys 
        - Basic cell dictionary containing each entitytype as key and a list of entities as value
            - Basic entity list containing all the entities of a specific entitytype in a specific cell in the grid

The grid is setup like this so it doesnt require as much iteration as a nested list/array (it uses O(n) ) and is very easy to manage


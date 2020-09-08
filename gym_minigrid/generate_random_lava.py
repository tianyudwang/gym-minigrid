import sys, os
import random
import argparse
import yaml

import numpy as np

dir_to_dis = {
    0:      np.array([1, 0]),        # down
    1:      np.array([0, 1]),        # right
    2:      np.array([-1, 0]),       # up
    3:      np.array([0, -1]),       # left
}


def gen_random_grid(grid_size, objects, max_objects=10, max_length=6):
    """
    Generate a random grid with the list of objects
    Grid will be padded with walls on its perimeter in gym-minigrid
    Objects will have width = 1, random length, placed horizontally or vertically
    """

    object_dict = {obj: [] for obj in objects}
    
    for i in range(max_objects):
        obj = random.choice(objects) 
        obj_dir = np.random.randint(4)
        obj_start = np.random.randint(grid_size, size=2)
        obj_len = np.random.randint(1, max_length+1)
        obj_end = obj_start + obj_len * dir_to_dis[obj_dir]
        if (obj_end[0] < 0 or obj_end[0] >= grid_size or
            obj_end[1] < 0 or obj_end[1] >= grid_size):
            continue

        for step in range(obj_len+1):
            object_dict[obj].append(obj_start + step * dir_to_dis[obj_dir])

    # to do: check there is a feasible path
    goal_pos = np.random.randint(1, grid_size-1, size=2)
    object_dict["Goal"] = [goal_pos]

    return object_dict

def main():

    # Parameters
    grid_size = 9
    num_grids = 100
    objects = ['Lawn', 'Lava', 'Wall']

    for n in range(num_grids):
        object_dict = gen_random_grid(grid_size, objects)
        if object_dict is not None:
            with open(os.path.join(args.out_dir, 
                      "grid_{0:04}.yml".format(n)), 'w') as outfile:
               yaml.dump(object_dict, outfile)  


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--out_dir',
        type=str,
        default="./envs/random_grid_configs/",
        help="Directory to save the generated grids")
    args = parser.parse_args()
    main()

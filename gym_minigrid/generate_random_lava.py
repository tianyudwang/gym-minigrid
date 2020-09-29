import sys, os
from os.path import dirname, abspath
import logging
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


def gen_random_grid(grid_size, objects, max_objects=16, max_length=6):
    """
    Generate a random grid with the list of objects
    Grid will be padded with walls on its perimeter in gym-minigrid
    Objects will have width = 1, random length, placed horizontally or vertically
    """

    object_dict = {obj: [] for obj in objects}
    
    num_objects = np.random.randint(max_objects // 2, max_objects)
    for i in range(num_objects):
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
    
    args.out_dir = dirname(dirname(dirname(abspath(__file__)))) + "/data_{}/grid_configs/".format(args.grid_size)
    if not os.path.exists(os.path.join(args.out_dir, 'train/')):
        os.makedirs(os.path.join(args.out_dir, 'train/'))
    if not os.path.exists(os.path.join(args.out_dir, 'valid/')):
        os.makedirs(os.path.join(args.out_dir, 'valid/'))
    if not os.path.exists(os.path.join(args.out_dir, 'test/')):
        os.makedirs(os.path.join(args.out_dir, 'test/'))

    # Parameters
    train_num_grids = 10000
    valid_num_grids = 1000
    test_num_grids = 1000
    objects = ['Lawn', 'Lava', 'Wall']

    logging.basicConfig(level=logging.INFO)
    logging.info("Start generating training grid configurations ...")
    for n in range(train_num_grids):
        object_dict = gen_random_grid(
            args.grid_size, objects, 
            max_objects=args.max_objects,
            max_length=args.max_length
        )
        if object_dict is not None:
            with open(os.path.join(args.out_dir, 
                      "train/grid_{0:04}.yml".format(n)), 'w') as outfile:
               yaml.dump(object_dict, outfile)  

    logging.info("Start generating validation grid configurations ...")
    for n in range(valid_num_grids):
        object_dict = gen_random_grid(
            args.grid_size, objects, 
            max_objects=args.max_objects,
            max_length=args.max_length
        )
        if object_dict is not None:
            with open(os.path.join(args.out_dir, 
                      "valid/grid_{0:04}.yml".format(n)), 'w') as outfile:
               yaml.dump(object_dict, outfile) 

    logging.info("Start generating testing grid configurations ...")
    for n in range(test_num_grids):
        object_dict = gen_random_grid(
            args.grid_size, objects, 
            max_objects=args.max_objects,
            max_length=args.max_length
        )
        if object_dict is not None:
            with open(os.path.join(args.out_dir, 
                      "test/grid_{0:04}.yml".format(n)), 'w') as outfile:
               yaml.dump(object_dict, outfile) 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--grid_size', type=int, default=16,
        help='Size of the minigrid environment')
    parser.add_argument(
        '--max_objects', type=int, default=32,
        help='Maximum number of objects in each map')
    parser.add_argument(
        '--max_length', type=int, default=8,
        help='Maximum length of each object')
    args = parser.parse_args()
    main()

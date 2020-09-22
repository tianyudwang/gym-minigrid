from gym_minigrid.minigrid import *
from gym_minigrid.register import register

import sys, os
from os.path import dirname, abspath
import logging
import glob
import yaml

class RandomLava(MiniGridEnv):
    """
    Environment constructed from randomly generate obstacles
    """
    def __init__(self, size, objects_dir):
        self._objects_files = sorted(glob.glob(objects_dir + 'grid_*.yml')) 
        self._idx = 0
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            see_through_walls=False,
            seed=0
        )

        np.random.seed(0)

    def _load_objects(self):
        try:
            object_file = self._objects_files[self._idx]
            self._idx += 1
            with open(object_file, 'r') as f:
                object_dict = yaml.load(f, Loader=yaml.Loader)
            return object_dict

        except IndexError:
            logging.warning("All grid configs consumed ...")
            sys.exit()

    def _gen_grid(self, width, height):
        assert width >= 5 and height >= 5

        objects = {'Lava': Lava, 'Lawn': Lawn, 'Wall': Wall, 'Goal': Goal}

        # Create an empty grid
        self.grid = Grid(width, height)

        # Place obstacles
        object_dict = self._load_objects() 
        for obj, pos_list in object_dict.items():
            if obj != "Goal" and pos_list:
                for pos in pos_list:
                    self.grid.set(*pos, objects[obj]())

        # Place goal
        self.goal_pos = object_dict['Goal'][0]
        self.put_obj(Goal(), *self.goal_pos)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place agent randomly
        set_start = True
        while set_start: 
            self.agent_pos = np.random.randint(1, width-1, 2)
            self.agent_dir = np.random.randint(4)
            set_start = self.grid.get(*self.agent_pos)

        self.mission = (
            "Prefer grass, avoid lava, and get to goal"
        )
    
class RandomLavaS9EnvTrain(RandomLava):
    def __init__(self):
        super().__init__(
            size=9, 
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data/grid_configs/train/'
        )

class RandomLavaS9EnvValid(RandomLava):
    def __init__(self):
        super().__init__(
            size=9, 
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data/grid_configs/valid/'
        )

class RandomLavaS9EnvTest(RandomLava):
    def __init__(self):
        super().__init__(
            size=9, 
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data/grid_configs/test/'
        )

class RandomLavaS16EnvTrain(RandomLava):
    def __init__(self):
        super().__init__(
            size=16,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_16/grid_configs/train/')

class RandomLavaS16EnvValid(RandomLava):
    def __init__(self):
        super().__init__(
            size=16,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_16/grid_configs/valid/')

class RandomLavaS16EnvTest(RandomLava):
    def __init__(self):
        super().__init__(
            size=16,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_16/grid_configs/test/')

class RandomLavaS64EnvTrain(RandomLava):
    def __init__(self):
        super().__init__(
            size=64,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_64/grid_configs/train/')

class RandomLavaS64EnvValid(RandomLava):
    def __init__(self):
        super().__init__(
            size=64,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_64/grid_configs/valid/')

class RandomLavaS64EnvTest(RandomLava):
    def __init__(self):
        super().__init__(
            size=64,
            objects_dir=dirname(dirname(dirname(dirname(abspath(__file__)))))
                + '/data_64/grid_configs/test/')
register(
    id='MiniGrid-RandomLavaS9-train-v0',
    entry_point='gym_minigrid.envs:RandomLavaS9EnvTrain')
   
register(
    id='MiniGrid-RandomLavaS9-valid-v0',
    entry_point='gym_minigrid.envs:RandomLavaS9EnvValid')

register(
    id='MiniGrid-RandomLavaS9-test-v0',
    entry_point='gym_minigrid.envs:RandomLavaS9EnvTest')

register(
    id='MiniGrid-RandomLavaS16-train-v0',
    entry_point='gym_minigrid.envs:RandomLavaS16EnvTrain')
   
register(
    id='MiniGrid-RandomLavaS16-valid-v0',
    entry_point='gym_minigrid.envs:RandomLavaS16EnvValid')

register(
    id='MiniGrid-RandomLavaS16-test-v0',
    entry_point='gym_minigrid.envs:RandomLavaS16EnvTest')
 
register(
    id='MiniGrid-RandomLavaS64-train-v0',
    entry_point='gym_minigrid.envs:RandomLavaS64EnvTrain')
   
register(
    id='MiniGrid-RandomLavaS64-valid-v0',
    entry_point='gym_minigrid.envs:RandomLavaS64EnvValid')

register(
    id='MiniGrid-RandomLavaS64-test-v0',
    entry_point='gym_minigrid.envs:RandomLavaS64EnvTest')
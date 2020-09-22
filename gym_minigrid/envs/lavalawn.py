from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class LavaLawnEnv(MiniGridEnv):
    """
    Environment with one wall one lawn and one lava
    """

    def __init__(self, size, obstacle_type=Lawn, seed=None):
        self.obstacle_type = obstacle_type
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls=False,
            seed=None
        )

    def _gen_grid(self, width, height):
        assert width >= 5 and height >= 5

        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.agent_pos = (1, 1)
        self.agent_dir = 0

        # Place a goal square in the bottom-right corner
        self.goal_pos = np.array((width - 2, height - 2))
        self.put_obj(Goal(), *self.goal_pos)

        # Place the horizontal lava
        self.grid.horz_wall(2, 2, 5, Wall)

        # Place the horizontal lawn
        self.grid.horz_wall(2, 4, 5, Lawn)

        # Place the horizontal wall
        self.grid.horz_wall(2, 6, 5, Lava)
        
        self.mission = (
            "prefer the lawn, avoid the lava, and get to the goal"
        )



class LavaLawnS9Env(LavaLawnEnv):
    def __init__(self):
        super().__init__(size=9)

register(
    id='MiniGrid-LavaLawnS9-v0',
    entry_point='gym_minigrid.envs:LavaLawnS9Env'
)

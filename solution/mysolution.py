from airlift.solutions import Solution
from airlift.envs import ActionHelper

class MySolution(Solution):
    """
    You are encouraged to utilize this class to submit your solutions. The primary solution algorithm will go inside the
    policy function. It is not a requirement to utilize this approach.
    """
    def __init__(self):
        super().__init__()

    def reset(self, obs, observation_spaces=None, action_spaces=None, seed=None):
        # Currently, the evaluator will NOT pass in an observation space or action space (they will be set to None)
        super().reset(obs, observation_spaces, action_spaces, seed)

        # Create an action helper using our random number generator
        self._action_helper = ActionHelper(self._np_random)

    def policies(self, obs, dones):
        # Use the acion helper to generate an action
        return self._action_helper.sample_valid_actions(obs)


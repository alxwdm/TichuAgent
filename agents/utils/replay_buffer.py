""" Utility replay buffer classes for RL Agents. """

from collections import namedtuple, deque

import numpy as np
import torch
import random

from agents.utils.segment_tree import SumSegmentTree, MinSegmentTree

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class DequeReplayBuffer:
    """ Fixed-size buffer to store experience tuples in a deque. """

    def __init__(self, action_size, buffer_size, batch_size, seed):
        """Initialize a ReplayBuffer object.
        Parameters
        ----
        action_size: int
          dimension of each action
        buffer_size: int
          maximum size of buffer
        batch_size: int
          size of each training batch
        seed: int
          random seed
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state",
            "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
    
    def sample(self, *args, **kwargs):
        """ Randomly sample a batch of experiences from memory. """
        experiences = random.sample(self.memory, k=self.batch_size)
        states = torch.from_numpy(np.vstack([e.state for e in
          experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in
          experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in
          experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in
          experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in
          experiences if e is not None]).astype(np.uint8)).float().to(device)
        # Match experiences shape for PER
        weights = 1
        idxes = 0
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """ Return the current size of internal memory. """
        return len(self.memory)

# OpenAI version with slight modifications
# >> github.com/openai/baselines/blob/master/baselines/deepq/replay_buffer.py
        
class HelperReplayBuffer(object):
    def __init__(self, size):
        """
        Creates a replay buffer.

        This class serves as a helper class when using
        prioritized experience replay (PER.

        Parameters
        ----------
        size: int
          Max number of transitions to store in the buffer. 
          When the buffer overflows the old memories are dropped.
        """
        self._storage = []
        self._maxsize = size
        self._next_idx = 0

    def __len__(self):
        return len(self._storage)

    def add(self, obs_t, action, reward, obs_tp1, done):
        data = (obs_t, action, reward, obs_tp1, done)

        if self._next_idx >= len(self._storage):
            self._storage.append(data)
        else:
            self._storage[self._next_idx] = data
        self._next_idx = (self._next_idx+1) % self._maxsize

    def _encode_sample(self, idxes):
        obses_t, actions, rewards, obses_tp1, dones = [], [], [], [], []
        for i in idxes:
            data = self._storage[i]
            obs_t, action, reward, obs_tp1, done = data
            obses_t.append(np.array(obs_t, copy=False))
            actions.append(np.array(action, copy=False))
            rewards.append(reward)
            obses_tp1.append(np.array(obs_tp1, copy=False))
            dones.append(done)
        return np.array(obses_t), np.array(actions), np.array(rewards), \
               np.array(obses_tp1), np.array(dones)

    def sample(self, batch_size):
        """
        Sample a batch of experiences.

        Parameters
        ----------
        batch_size: int
            How many transitions to sample.

        Returns
        -------
        obs_batch: np.array
            batch of observations
        act_batch: np.array
            batch of actions executed given obs_batch
        rew_batch: np.array
            rewards received as results of executing act_batch
        next_obs_batch: np.array
            next set of observations seen after executing act_batch
        done_mask: np.array
            done_mask[i] = 1 if executing act_batch[i] resulted in
            the end of an episode and 0 otherwise.
        """
        idxes = [random.randint(0, len(self._storage)-1)
                   for _ in range(batch_size)]
        return self._encode_sample(idxes)

class PrioritizedReplayBuffer(HelperReplayBuffer):
    def __init__(self, size, alpha):
        """
        Creates Prioritized Experience Replay (PER) buffer.

        Parameters
        ----------
        size: int
          Max number of transitions to store in the buffer. When the buffer
          overflows the old memories are dropped.
        alpha: float
          how much prioritization is used
          (0 - no prioritization, 1 - full prioritization)

        See Also
        --------
        HelperReplayBuffer.__init__
        """
        super(PrioritizedReplayBuffer, self).__init__(size)
        assert alpha >= 0
        self._alpha = alpha

        it_capacity = 1
        while it_capacity < size:
            it_capacity *= 2

        self._it_sum = SumSegmentTree(it_capacity)
        self._it_min = MinSegmentTree(it_capacity)
        self._max_priority = 1.0

    def add(self, *args, **kwargs):
        """ See HelperReplayBuffer.store_effect """
        idx = self._next_idx
        super().add(*args, **kwargs)
        self._it_sum[idx] = self._max_priority ** self._alpha
        self._it_min[idx] = self._max_priority ** self._alpha

    def _sample_proportional(self, batch_size):
        res = []
        p_total = self._it_sum.sum(0, len(self._storage)-1)
        every_range_len = p_total / batch_size
        for i in range(batch_size):
            mass = random.random() * every_range_len + i * every_range_len
            idx = self._it_sum.find_prefixsum_idx(mass)
            res.append(idx)
        return res

    def sample(self, batch_size, beta):
        """
        Sample a batch of experiences.

        compared to ReplayBuffer.sample
        it also returns importance weights and idxes
        of sampled experiences.

        Parameters
        ----------
        batch_size: int
          How many transitions to sample.
        beta: float
          To what degree to use importance weights
          (0 - no corrections, 1 - full correction)

        Returns
        -------
        obs_batch: np.array
          batch of observations
        act_batch: np.array
          batch of actions executed given obs_batch
        rew_batch: np.array
          rewards received as results of executing act_batch
        next_obs_batch: np.array
          next set of observations seen after executing act_batch
        done_mask: np.array
          done_mask[i] = 1 if executing act_batch[i] resulted in
          the end of an episode and 0 otherwise.
        weights: np.array
          Array of shape (batch_size,) and dtype np.float32
          denoting importance weight of each sampled transition
        idxes: np.array
          Array of shape (batch_size,) and dtype np.int32
          idexes in buffer of sampled experiences
        """
        assert beta > 0

        idxes = self._sample_proportional(batch_size)

        weights = []
        p_min = self._it_min.min() / self._it_sum.sum()
        max_weight = (p_min * len(self._storage)) ** (-beta)

        for idx in idxes:
            p_sample = self._it_sum[idx] / self._it_sum.sum()
            weight = (p_sample * len(self._storage)) ** (-beta)
            weights.append(weight / max_weight)
        weights = np.array(weights)
        encoded_sample = self._encode_sample(idxes)
        experiences = tuple(list(encoded_sample) + [weights, idxes])
        # Unpack experiences for conversion to torch tensors
        states, actions, rewards, next_states, dones, weights, idxes = \
            experiences
        states = torch.from_numpy(states).float().to(device)
        actions = torch.from_numpy(actions).unsqueeze(1).long().to(device)
        rewards = torch.from_numpy(rewards).float().unsqueeze(1).to(device)
        next_states = torch.from_numpy(next_states).float().to(device)
        dones = torch.from_numpy(dones.astype(np.uint8)).unsqueeze(1) \
                                                        .float().to(device)
        weights = torch.from_numpy(weights).unsqueeze(1).float().to(device)
        return (states, actions, rewards, next_states, dones, weights, idxes)

    def update_priorities(self, idxes, priorities):
        """
        Update priorities of sampled transitions.

        sets priority of transition at index idxes[i] in buffer
        to priorities[i].

        Parameters
        ----------
        idxes: [int]
          List of idxes of sampled transitions
        priorities: [float]
          List of updated priorities corresponding to
          transitions at the sampled idxes denoted by
          variable `idxes`.
        """
        assert len(idxes) == len(priorities)
        for idx, priority in zip(idxes, priorities):
            assert priority > 0
            assert 0 <= idx < len(self._storage)
            self._it_sum[idx] = priority ** self._alpha
            self._it_min[idx] = priority ** self._alpha

            self._max_priority = max(self._max_priority, priority)

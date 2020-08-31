"""
DDPG Agent for Reinforcement Learning

Modified version for TichuAgent project
>> Paper: https://arxiv.org/abs/1509.02971
>> Source: https://github.com/alxwdm/DRLND_projects
"""

import numpy as np
import random
import copy
from collections import namedtuple, deque
import torch
import torch.nn.functional as F
import torch.optim as optim

from model import Actor, Critic
from ./utils/replay_buffer import DequeReplayBuffer

# Hyperparameter
# -- Replay Buffer ------
BUFFER_SIZE = int(1e6)  # replay buffer size
BATCH_SIZE = 128        # minibatch size
# -- Update Settings ---
TAU = 1e-3              # for soft update of target parameters
LEARN_EVERY = 20        # learn every x timesteps
LEARN_STEP_N = 10       # learn x samples for every learning step
# -- Model --------------
GAMMA = 0.99            # discount factor
LR_ACTOR = 1e-3         # learning rate of the actor 
LR_CRITIC = 1e-3        # learning rate of the critic
WEIGHT_DECAY = 0        # L2 weight decay
FC_UNITS_1 = 128        # Units of first hidden layer (both actor and critic)
FC_UNITS_2 = 128        # Units of second hidden layer (both actor and critic)
# -- Noise Settings -----
EPSILON = 1.0           # noise factor 
EPSILON_DECAY = 0.999   # noise decay rate 
NOISE_SIGMA = 0.1       # sigma parameter for Ornstein-Uhlenbeck noise
NOISE_THETA = 0.15      # theta parameter for Ornstein-Uhlenbeck noise

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class DDPGAgent():
    """ An agent that interacts with and learns from the environment. """
    
    def __init__(self, state_size, action_size, random_seed):
        """
        Initializes an Agent object.
        
        Parameters
        ----------
        state_size: int
          dimension of each state
        action_size: int
          dimension of each action
        random_seed: int
          random seed
        """
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(random_seed)

        # Actor Network (w/ Target Network)
        self.actor_local = Actor(state_size, action_size, random_seed,
                                 FC_UNITS_1, FC_UNITS_2).to(device)
        self.actor_target = Actor(state_size, action_size, random_seed,
                                  FC_UNITS_1, FC_UNITS_2).to(device)
        self.actor_optimizer = optim.Adam(self.actor_local.parameters(),
                                          lr=LR_ACTOR)

        # Critic Network (w/ Target Network)
        self.critic_local = Critic(state_size, action_size, random_seed,
                                   FC_UNITS_1, FC_UNITS_2).to(device)
        self.critic_target = Critic(state_size, action_size, random_seed,
                                    FC_UNITS_1, FC_UNITS_2).to(device)
        self.critic_optimizer = optim.Adam(self.critic_local.parameters(),
                                           lr=LR_CRITIC,
                                           weight_decay=WEIGHT_DECAY)

        # Replay memory
        self.memory = DequeReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE,
                                        random_seed)
    
    def step(self, state, action, reward, next_state, done, timestep):
        """
        Saves experience in memory, uses sample from buffer to learn. 

        Parameters
        ----------
        state:
          observed state vector of this step
        action:
          action vector taken in this step
        reward:
          rewards recieved this step
        next_state:
          observed state vector of next state
        done:
          whether episode is finished
        timestep:
          timestep of this episode
        """
        # Save experience (state, action, reward, next_state, done) tuple
        self.memory.add(state, action, reward, next_state, done)

        # Learning process:
        # >> 1) learn if enough samples are available in memory
        # >> 2) learn every LEARN_EVERY timesteps
        # >> 3) learn for LEARN_STEP_N steps
        if len(self.memory) > BATCH_SIZE and timestep % LEARN_EVERY == 0:
            for _ in range(LEARN_STEP_N):
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def act(self, state):
        """ Returns actions for given state as per current policy. """
        state = torch.from_numpy(state).float().to(device)
        self.actor_local.eval()
        with torch.no_grad():
            action = self.actor_local(state).cpu().data.numpy()
        self.actor_local.train()
        return np.rint(action)

    def reset(self):
        """ Resets UO-noise process. """
        self.noise.reset()

    def learn(self, experiences, gamma):
        """
        Update policy and value parameters using batch of experiences.

        Q_target = r + γ * critic_target(next_state, actor_target(next_state))
        where:
          actor_target(state) -> action
          critic_target(state, action) -> Q-value

        Parameters
        ----------
        experiences: Tuple[torch.Tensor]
          batch of (s, a, r, s', done) tuples
        gamma: float
          discount factor
        """
        states, actions, rewards, next_states, dones = experiences
        # -------------------------- update critic ---------------------------
        # Get predicted next-state actions and Q values from target models
        actions_next = self.actor_target(next_states)
        Q_targets_next = self.critic_target(next_states, actions_next)
        # Compute Q targets for current states (y_i)
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
        # Compute critic loss
        Q_expected = self.critic_local(states, actions)
        critic_loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss (with gradient clipping)
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.critic_local.parameters(), 1)
        self.critic_optimizer.step()
        # -------------------------- update actor ----------------------------
        # Compute actor loss
        actions_pred = self.actor_local(states)
        actor_loss = -self.critic_local(states, actions_pred).mean()
        # Minimize the loss
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        # ----------------- (soft) update target networks --------------------
        self.soft_update(self.critic_local, self.critic_target, TAU)
        self.soft_update(self.actor_local, self.actor_target, TAU)

    def soft_update(self, local_model, target_model, tau):
        """
        Soft update model parameters.

        θ_target = τ*θ_local + (1-τ)*θ_target

        Parameters
        ----------
        local_model:
          PyTorch model (weights will be copied from)
        target_model:
          PyTorch model (weights will be copied to)
        tau: float
          interpolation parameter
        """
        for target_param, local_param in zip(target_model.parameters(),
                                             local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + 
                                    (1.0-tau)*target_param.data)

    def save_checkpoint(self, filename='checkpoint'):
        checkpoint = {'action_size': self.action_size,
                      'state_size': self.state_size,
                      'current_epsilon': self.epsilon,
                      'actor_state_dict': self.actor_local.state_dict(),
                      'critic_state_dict': self.critic_local.state_dict()}
        filepath = filename + '.pth'
        torch.save(checkpoint, filepath)
        print(filepath + ' succesfully saved.')

    def load_checkpoint(self, filepath='checkpoint.pth'):
        checkpoint = torch.load(filepath)
        state_size = checkpoint['state_size']
        action_size = checkpoint['action_size']
        self.actor_local = Actor(state_size, action_size, 
                                 seed=42).to(device)
        self.critic_local = Critic(state_size, action_size, 
                                   seed=42).to(device)
        self.actor_local.load_state_dict(checkpoint['actor_state_dict'])
        self.critic_local.load_state_dict(checkpoint['critic_state_dict'])
        self.epsilon = checkpoint['current_epsilon']
        print(filepath + ' successfully loaded.')

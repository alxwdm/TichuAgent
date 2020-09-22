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
from itertools import compress
import torch
import torch.nn.functional as F
import torch.optim as optim

from agents.ddpg.model import Actor, Critic
from agents.utils.replay_buffer import DequeReplayBuffer

from env.cards import Cards
from env.deck import Deck

# Hyperparameter
# -- Replay Buffer ------
BUFFER_SIZE = int(1e6)  # replay buffer size
BATCH_SIZE = 128        # minibatch size
# -- Update Settings ---
TAU = 1e-3              # for soft update of target parameters
LEARN_EVERY = 4         # learn every x timesteps
LEARN_STEP_N = 2        # learn x samples for every learning step
# -- Model --------------
GAMMA = 0.99            # discount factor
LR_ACTOR = 1e-3         # learning rate of the actor 
LR_CRITIC = 1e-3        # learning rate of the critic
WEIGHT_DECAY = 0        # L2 weight decay
FC_UNITS_1 = 256        # Units of first hidden layer (both actor and critic)
FC_UNITS_2 = 256        # Units of second hidden layer (both actor and critic)
FC_UNITS_3 = 128        # Units of third hidden layer (both actor and critic)
FC_UNITS_4 = 64         # Units of 4th hidden layer (both actor and critic)

# State and action type setting
STATE_STYLE = 'suitless'
ACTION_STYLE = 'binary'
ACTION_DIMS = {'default': 56, 'suitless': 17, 'combination': 9, 'binary': 1}
STATE_DIMS = {'default': 256, 'suitless': 39}

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class DDPGAgent():
    """ An agent that interacts with and learns from the environment. """
    
    def __init__(self, state_size=STATE_DIMS[STATE_STYLE], 
                  action_size=ACTION_DIMS[ACTION_STYLE], 
                  random_seed, heuristic_agent):
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
        self.heuristic_agent = heuristic_agent

        # Actor Network (w/ Target Network)
        self.actor_local = Actor(state_size, action_size, random_seed,
                                 FC_UNITS_1, FC_UNITS_2, FC_UNITS_3, 
                                 FC_UNITS_4, ACTION_STYLE).to(device)
        self.actor_target = Actor(state_size, action_size, random_seed,
                                  FC_UNITS_1, FC_UNITS_2, FC_UNITS_3, 
                                  FC_UNITS_4, ACTION_STYLE).to(device)
        self.actor_optimizer = optim.Adam(self.actor_local.parameters(),
                                          lr=LR_ACTOR)

        # Critic Network (w/ Target Network)
        self.critic_local = Critic(state_size, action_size, random_seed,
                                   FC_UNITS_1, FC_UNITS_2, FC_UNITS_3, 
                                   FC_UNITS_4).to(device)
        self.critic_target = Critic(state_size, action_size, random_seed,
                                   FC_UNITS_1, FC_UNITS_2, FC_UNITS_3, 
                                   FC_UNITS_4).to(device)
        self.critic_optimizer = optim.Adam(self.critic_local.parameters(),
                                           lr=LR_CRITIC,
                                           weight_decay=WEIGHT_DECAY)

        # Replay memory
        self.memory = DequeReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE,
                                        random_seed)
    
        # State and action augmentation to simplify/accelerate learning
        self.dispatch_state = {
                        'default': self._flatten_state,
                        'suitless': self._state_conv_suitless
                        }
        self.dispatch_action_out = {
                        'default': self._default_action,
                        'suitless': self._action_suitless_to_default,
                        'combination': self._action_comb_to_default,
                        'binary': self._action_binary_to_default
                        }
        self.dispatch_action_in = {
                        'default': self._default_action,
                        'suitless': self._action_default_to_suitless,
                        'combination': self._action_default_to_combination,
                        'binary': self._action_default_to_binary
                        }

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
        # augmentation of states and action
        raw_state = state
        state = self.dispatch_state[STATE_STYLE](state)
        next_state = self.dispatch_state[STATE_STYLE](next_state)
        action = self.dispatch_action_in[ACTION_STYLE](action)
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

    def act(self, state, eps=0, debug=False):
        """ Returns actions for given state as per current policy. """
        if random.random() > eps:
            np_state = self.dispatch_state[STATE_STYLE](state)
            torch_state = torch.from_numpy(np_state).float().to(device)
            self.actor_local.eval()
            with torch.no_grad():
                action = self.actor_local(torch_state).cpu().data.numpy()
            self.actor_local.train()
            # print N.N. output for debugging
            if debug:
                print('action (before conversion): ', action)
            # convert action to env format if necessary
            action = self.dispatch_action_out[ACTION_STYLE](action, state)
            if debug:
                print('action (after conversion): ', np.rint(action))            
            eps_move = False
        else:
            action = self.heuristic_agent.act(state)
            eps_move = True
            if debug:
                print('eps move!')
        return np.rint(action), eps_move

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
        print(filepath + ' successfully loaded.')

    def _flatten_state(self, state):
        """ A state flattening function. (TODO: make more pythonic) """
        flattened_list = [item for sublist in state for item in sublist]
        flattened_state = []
        for elem in flattened_list:
            if type(elem) != list:
                flattened_state.append(elem)
            else:
                for e in elem:
                    flattened_state.append(e)
        return np.asarray(flattened_state, dtype='int32')

    def _state_conv_suitless(self, state_vec):
        """
        An alternative state with reduced state space size.
        
        state design:
        [hand_size, tichu_flag, suitless_cards] of active player
        [is_opponent, hand_size, tichu_flag, suitless_cards] of stack leader

        returns state vector in flattened format
        """

        def suitless_enc(crd_state):
            """ Changes state to suitless encoding. """
            suitless_cards = np.zeros(17, int).tolist()
            for i in range(13):
                suitless_cards[i] = sum(crd_state[i*4:i*4+4])
            suitless_cards[13] = crd_state[13]
            suitless_cards[14] = crd_state[14]
            suitless_cards[15] = crd_state[15]
            suitless_cards[16] = crd_state[16]
            return suitless_cards

        def _flatten_conv_state(state):
            """ flattens suitless state. """
            flattened_list = state
            flattened_state = []
            for elem in flattened_list:
                if type(elem) != list:
                    flattened_state.append(elem)
                else:
                    for e in elem:
                        flattened_state.append(e)
            return np.asarray(flattened_state, dtype='int32')
        # get infos from default_state vector
        leading_idx, is_opponent, leading_cards, leading_type = \
          self._get_info_from_state(default_state)
        # get first part of state: self perspective
        conv_state = []
        conv_state.append(state_vec[0][0]) # Hand Size
        conv_state.append(state_vec[0][1]) # Tichu Flag
        conv_state.append(suitless_enc(state_vec[0][2])) # suitless hand
        # get second part of state: leading player perspective
        if leading_idx == 0:
            leading_size = 0
            leading_tichu = 0
            leading_suitless = np.zeros(17, int).tolist()
        else:
            leading_size = leading_cards.size
            leading_tichu = state_vec[leading_idx][1]
            leading_suitless = suitless_enc(state_vec[leading_idx][2])
        conv_state.append(is_opponent) # opponent yes/no
        conv_state.append(leading_size) # hand size
        conv_state.append(leading_tichu) # tichu flag
        conv_state.append(leading_suitless) # suitless encoded leading cards

        return _flatten_conv_state(conv_state)

    def _default_action(self, action, default_state):
        """ Returns action for default action type. """
        action = np.rint(np.clip(action, 0, 1))
        return action

    def _action_suitless_to_default(self, suitless_action, default_state):
        """
        Converts a "suitless" action into action vector expected by env.

        Example:
        suitless_action: [2, 2, 0, 0, ...] for a 2-3-pair sequence
        action_vector: [1, 1, 0, 0, 1, 1, 0, 0, ...] acc. on available cards
        """
        # convert output from actor
        suitless_action = np.rint(np.clip(suitless_action, 0, 4))
        action_vec = np.zeros(56, int)
        # encode regular cards:
        for i in range(13):
            card_count = suitless_action[i]
            available_cards = default_state[0][2][i*4:i*4+4]
            if card_count == 0:
                pass
            elif sum(available_cards) < card_count:
                suc = False
                break
            else:
                for j in range(4):
                    if available_cards[j] == 1 and card_count > 0:
                        action_vec[i*4+j] = 1
                        card_count -= 1
                    else:
                        pass
        # encode special cards
        action_vec[-4] = suitless_action[13]
        action_vec[-3] = suitless_action[14]
        action_vec[-2] = suitless_action[15]
        action_vec[-1] = suitless_action[16]
        return action_vec

    def _action_comb_to_default(self, comb_action, default_state):
        """
        Converts a "combination" action into action vector expected by env.

        Based on the input state, the lowest action that beats the currently
        highest combination is retuned.

        Example:
        comb_action: [0, 1, 0, 0, ...] for a solo card
        action_vector: binary encoded action vector that beats leading player.
        """
        hand_cards = _vec_to_cards(state_vec[0][2])
        leading_idx, is_opponent, leading_cards, leading_type = \
          self._get_info_from_state(default_state)
        raise NotImplementedError

    def _action_binary_to_default(self, binary_action, default_state):
        """
        Converts a "binary" action into action vector expected by env.

        Binary action is just pass or beat. If the action is "beat", then the
        lowest available combination that beats the currently highest
        combination is returned.

        Example:
        binary_action: [1] in order to beat the leading player
        action_vector: binary encoded action vector that beats leading player.
        """
        comb_types = {'solo': 0, 'pair': 1, 'triple': 2, 'four_bomb': 3,
                      'full': 4, 'straight': 5, 'straight_bomb': 6, 
                      'pair_seq': 7}
        # pass if action is "pass"
        if binary_acton == 0:
            action = self._cards_to_vec(Cards([]))
            return action
        # try to beat if action is "beat"
        hand_cards = self._vec_to_cards(state_vec[0][2])
        available_combs = hand_cards.get_available_combinations()
        leading_idx, is_opponent, leading_cards, leading_type = \
          self._get_info_from_state(default_state)
        if leading_type == 'pass':
            # TODO: what action to take if stack is empty?
            raise NotImplementedError
        type_index = comb_types[leading_type]
        # check if leading type combination is available and can be beaten
        if available_comb[type_index]:
            phoenix_buffer = None
            for crds in available_comb[type_index]:
                if crds.cards[0].name == 'Dog': # Dog can only be played alone
                    pass
                elif crds.power > leading_power and crds.size == leading_size:
                    # try to avoid using phoenix if possible
                    if crds.phoenix_flag and not(phoenix_buffer):
                        phoenix_buffer = crds
                    else:
                        action = self._cards_to_vec(crds)
                        return action
            if phoenix_buffer:
                action = self._cards_to_vec(phoenix_buffer)
                return action
            # pass if no higher combination available
            action = self._cards_to_vec(Cards([]))
            return action
        # if no combination exists, try to four bomb or straight bomb
        elif available_comb[comb_types['four_bomb']] and 
              not(leading_type == 'straight_bomb'):
            bomb = available_comb[comb_types['four_bomb']][0]
            action = self._cards_to_vec(bomb)
            return action
        elif available_comb[comb_types['straight_bomb']]:
            bomb = available_comb[comb_types['straight_bomb']][0]
            action = self._cards_to_vec(bomb)
            return action
        # pass if opponent cannot be beaten
        else:
            action = self._cards_to_vec(Cards([]))
            return action

    def _action_default_to_suitless(self, default_action):
        """ Converts an action expeced by the env to "suitless" action. """
        action_vec = np.zeros(17, int)
        for i in range(13):
            action_vec[i] = sum(default_action[i*4:i*4+4])
        action_vec[13] = default_action[-4]
        action_vec[14] = default_action[-3]
        action_vec[15] = default_action[-2]
        action_vec[16] = default_action[-1]
        return action_vec

    def _action_default_to_combination(self, default_action):
        """ Converts an action expeced by the env to "combination" action. """
        comb_types = {'solo': 0, 'pair': 1, 'triple': 2, 'four_bomb': 3,
                      'full': 4, 'straight': 5, 'straight_bomb': 6, 
                      'pair_seq': 7}
        action = np.zeros(9, int)
        action_type = self._vec_to_cards(default_action).type
        if action_type == 'pass':
            action[0] = 1
        else:
            action[comb_types[action_type]+1] = 1
        return action

    def _action_default_to_binary(self, default_action):
        """ Converts an action expeced by the env to "binary" action. """
        crds = self._vec_to_cards(default_action)
        if crd.type == 'pass':
            action = 0
        else:
            action = 1
        return action

    def _get_info_from_state(self, default_state):
        """
        Interprets the default state for state and action augmentation.
        """
        state_vec = default_state
        # get info from full state
        hand_cards = self._vec_to_cards(state_vec[0][2])
        opp_cards_0 = self._vec_to_cards(state_vec[1][2])
        teammate_cards = self._vec_to_cards(state_vec[2][2])
        opp_cards_1 = self._vec_to_cards(state_vec[3][2])
        # determine leading cards
        # new stack
        if (teammate_cards.type == 'pass' and opp_cards_0.type == 'pass' and 
                opp_cards_1.type == 'pass'):
            leading_idx = 0
            is_opponent = 0
            leading_cards = Cards([])
        # teammate leading
        elif teammate_cards.power > max(opp_cards_0.power, opp_cards_1.power):
            leading_idx = 2
            is_opponent = 0
            leading_cards = teammate_cards
        # opponent 0 leading
        elif ((opp_cards_0.power > opp_cards_1.power) or 
                (opp_cards_1.type == 'pass')):
            leading_idx = 1
            is_opponent = 1
            leading_cards = opp_cards_0
        # opponent 1 leading
        else:
            leading_idx = 3
            is_opponent = 1
            leading_cards = opp_cards_1
        leading_type = leading_cards.type
        return leading_idx, is_opponent, leading_cards, leading_type

    def _cards_to_vec(self, cards):
        vec = np.zeros(len(self.all_cards), int)
        for i in range(len(self.all_cards)):
            crd = Cards([self.all_cards[i]])
            if cards.contains(crd):
                vec[i] = 1
        return vec.tolist()

    def _vec_to_cards(self, vec):
        return Cards(list(compress(self.all_cards, vec)))

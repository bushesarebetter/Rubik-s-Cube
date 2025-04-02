import torch.nn as nn
import torch.optim as optim
import torch
from collections import deque
import random
import numpy as np
    
class RubiksBot(nn.Module):
    def __init__(self, state_size=54, action_size=28):
        super().__init__()
        self.q_net = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, action_size)
        )

        self.target_net = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, action_size)
        )

        self.target_net.load_state_dict(self.q_net.state_dict())

        self.memory = deque(maxlen=100000)
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.optimizer = torch.optim.RAdam(self.q_net.parameters(), lr=0.001)
        self.target_update_freq = 100
        self.train_step_count = 0

        self.criterion = nn.MSELoss()
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            state = torch.FloatTensor(state).unsqueeze(0)
            return torch.argmax(self.q_net(state)).item()
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states))
        next_states = torch.FloatTensor(np.array(next_states))
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)

        current_q = self.q_net(states).gather(1, actions.unsqueeze(1))

        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0].detach()
            target_q = rewards + (1 - dones) * self.gamma * next_q
            target_q = torch.clamp(target_q, -10, 10)

        loss = nn.HuberLoss()(current_q.squeeze(), target_q)
        
        self.train_step_count += 1
        if self.train_step_count % self.target_update_freq == 0:
            self.update_target() 
        
        self.optimizer.zero_grad()
        loss.backward()

        nn.utils.clip_grad_norm_(
            self.q_net.parameters(),
            max_norm=1.0,
            norm_type=2
        )

        self.optimizer.step()
        
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        return loss
    def update_target(self):
        self.target_net.load_state_dict(self.q_net.state_dict())

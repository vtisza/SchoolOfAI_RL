
# coding: utf-8
import time

import gym
import matplotlib.pyplot as plt
import numpy as np


def run_episode(env, parameters):
    observation = env.reset()
    totalreward = 0
    for _ in range(200):
        action = 0 if np.matmul(parameters,observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        env.render()
        totalreward += reward
        if done:
            break
    return totalreward


def train(submit):
    env = gym.make('CartPole-v0')
    if submit:
        env.render()
        time.sleep(0.1)

    episodes_per_update = 5
    noise_scaling = 0.1
    parameters = np.random.rand(4) * 2 - 1
    bestreward = 0
    counter = 0

    for _ in range(10000):
        counter += 1
        newparams = parameters + (np.random.rand(4) * 2 - 1)*noise_scaling
        # print newparams
        # reward = 0
        # for _ in xrange(episodes_per_update):
        #     run = run_episode(env,newparams)
        #     reward += run
        reward = run_episode(env,newparams)
        # print "reward %d best %d" % (reward, bestreward)
        if reward > bestreward:
            # print "update"
            bestreward = reward
            parameters = newparams
            if reward == 200:
                break

    if submit:
        for _ in range(100):
            run_episode(env,parameters)
        env.close()

    return counter


results = []
for _ in range(10):
    results.append(train(submit=True))

plt.hist(results,50,normed=1, facecolor='g', alpha=0.75)
plt.xlabel('Episodes required to reach 200')
plt.ylabel('Frequency')
plt.title('Histogram of Random Search')
plt.show()

print(np.sum(results) / 1000.0)

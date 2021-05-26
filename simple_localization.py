#!/usr/bin/env python
import numpy as np


def world(world_observations=[0, 1], world_observation_probability=[0.8, 0.2], world_size=5):
  return np.random.choice(world_observations, world_size, p=world_observation_probability)

def sense1d(probability, observation, world, prob_hit=0.6, prob_miss=0.2):
  new_prob = np.array([p*((observation==w)*prob_hit + (1-(observation==w))*prob_miss) for w, p in zip(world, probability)])
  return (new_prob / sum(new_prob)).tolist()

def slideArray(arr, n):
  if n < 0:
    return arr[abs(n):] + arr[:abs(n)]
  else:
    return arr[len(arr)-abs(n):] + arr[:len(arr)-abs(n)]

def move1d(probabilities, movement, prob_exact=0.8, prob_over=0.1, prob_under=0.1):
  if not movement:
    return probabilities
  
  # negative = left
  if movement < 0:
    under_shot = movement + 1
    over_shot = movement - 1
  else:
    under_shot = movement - 1
    over_shot = movement + 1
  
  probabilities_exact = np.array(slideArray(probabilities, movement)) * prob_exact
  probabilities_under = np.array(slideArray(probabilities, under_shot)) * prob_under
  probabilities_over = np.array(slideArray(probabilities, over_shot)) * prob_over
  return (probabilities_exact + probabilities_under + probabilities_over).tolist()

if __name__ == "__main__":
  w = world(world_size=10)
  # w = [0, 1, 1, 0, 0]

  # starting with equal probability
  position_probability = [1/len(w) for _ in range(len(w))]
  bot_position = np.random.randint(len(w))

  print("world:\n{}".format(w))

  position_probability = sense1d(position_probability, w[bot_position], w)
  for i in range(len(w)):
    print("position_probability: {}\n\tReal_position: {} predictied: {}".format(position_probability, bot_position, [i for i, v in enumerate(position_probability) if max(position_probability) == v] ))
    position_probability = move1d(position_probability, 1)
    bot_position = (bot_position + 1) % len(w)
    position_probability = sense1d(position_probability, w[bot_position], w)

  print("position_probability: {}\n\tReal_position: {} predictied: {}".format(position_probability, bot_position, [i for i, v in enumerate(position_probability) if max(position_probability) == v] ))



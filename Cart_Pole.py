import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
import time


def run_simulation(args):

    env = gym.make('CartPole-v1', render_mode=None)
    # Wenn visualisierung relevant ist
    # env = gym.make('CartPole-v1', render_mode='human' if not args.train else None)

    with open('config_files/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    if not args.train:
        file = "training_q_tables/" + args.run
        args.cut_not_zero = args.run[args.run.index('Z')+1]
        args.cut_close_zero = args.run[args.run.index('Z')+2]
        args.linear = args.run[args.run.find("L", args.run.find("l")+1)+1]
        args.geom = args.run[args.run.index('G')+1]


    pos_space = make_space(2.4, config['LINEAR_STATE_SPACE_NUMBER'], args)
    vel_space = make_space(4, config['LINEAR_STATE_SPACE_NUMBER'], args)
    ang_space = make_space(0.2095, config['LINEAR_STATE_SPACE_NUMBER'], args)
    ang_vel_space = make_space(4, config['LINEAR_STATE_SPACE_NUMBER'], args)
    space_bins = [pos_space, vel_space, ang_space, ang_vel_space]

    rng = np.random.default_rng()

    epsilon = config["EPSILON"]
    learning_rate_a = config["LEARNING_RATE"]
    discount_factor_g = config["DISCOUNT_FACTOR"]
    epsilon_decay_rate = config["EPSILON_DECAY_RATE"]

    if args.train:
        q_table = np.zeros((len(pos_space) + 1, len(vel_space) + 1, len(ang_space) + 1, len(ang_vel_space) + 1,
                            env.action_space.n))
        q_table_count = q_table.copy()
    else:
        q_table = np.load(file)
        q_table_count = np.zeros(q_table.shape)

    rewards_per_episode = []
    total_rewards = total_avg_reward = i = 0

    while True:
        start_time = time.time()
        state = env.reset()[0]
        state = [np.digitize(np.array([item]), bin_list)[0] for item, bin_list in zip(state, space_bins)]
        terminated = truncated = False
        rewards = 0

        if args.test_metric1: # Pushes cart in one direction as metric 1
            for _ in range(6):
                new_state, reward, terminated, truncated, info = env.step(0)
                state = [np.digitize(np.array([item]), bin_list)[0] for item, bin_list in zip(new_state, space_bins)]

        while not terminated and not truncated:
            if (args.train and rng.random() < epsilon) or (args.test_metric2 and rewards% 5) == 0:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state[0], state[1], state[2], state[3], :])

            new_state, reward, terminated, truncated, info = env.step(action)
            if args.test_metric3:
                state = state + np.multiply([rng.random() for i in range(4)], [0.01, 0.1, 0.0001, 0.1])
            new_state = [np.digitize(np.array([item]), bin_list)[0] for item, bin_list in zip(new_state, space_bins)]

            if args.train:
                q_table[state[0], state[1], state[2], state[3], action] += learning_rate_a * (
                            float(reward) + discount_factor_g * np.max(
                        q_table[new_state[0], new_state[1], new_state[2], new_state[3], :]) - q_table[
                                state[0], state[1], state[2], state[3], action])
                q_table_count[state[0], state[1], state[2], state[3], action] += + 1

            state = new_state

            rewards += reward
            total_rewards += reward

        run_time = time.time() - start_time
        rewards_per_episode.append(rewards)
        total_avg_reward = total_avg_reward + ((rewards - total_avg_reward) / (i + 1))

        if args.verbose:
            print(
                f'Episode: {i} Rewards: {rewards} Avg Rewards: {total_avg_reward} Total Rewards: {total_rewards} Time: {run_time} ')
        else:
            print(f'{i},{rewards},{total_avg_reward},{total_rewards},{run_time}')

        if np.mean(rewards_per_episode[-50:]) >= config['REWARD_THRESHOLD'] and args.train:
            plot_and_save_learning(q_table, q_table_count, rewards_per_episode, args)
            break

        if not args.train and i >= 99:
            break

        epsilon = epsilon - epsilon_decay_rate if epsilon > 0.01 else 0.01
        i += 1
    env.close()

def make_space(end, num, args):
    if args.geom:
        space = np.geomspace(1, end + 1, num=num) - 1
    else:
        space = np.linspace(0, end, num=num)

    if args.cut_not_zero:
        space = np.append(space - (space[1] / 2), end)
        return np.concatenate((space[::-1] * -1, space[2:]))

    if args.cut_close_zero:
        distance = 0.000001
        space0 = space + distance
        space1 = (space + (space[1] - distance)) * -1
        return np.concatenate((space1[::-1], space0))

    return np.concatenate((space[::-1] * -1, space[1:]))

def plot_and_save_learning(q_table, q_table_count, rewards_per_episode, args):
    j = 0

    file_infos = f"_Z{int(args.cut_not_zero)}{int(args.cut_close_zero)}L{int(args.linear)}G{int(args.geom)}"
    while True:

        file_name_png = Path(f"training_png\\training{j}"+ file_infos + ".png")
        file_name_npy = Path(f"training_q_tables\\Q_table{j}"+ file_infos + ".npy")
        file_name_npy2 = Path(f"training_q_tables\\Q_table_count{j}" + file_infos + ".npy")
        if not (file_name_png.is_file() or file_name_npy.is_file() or file_name_npy2.is_file()):
            break
        j += 1

    np.save(file_name_npy, q_table)
    np.save(file_name_npy2, q_table_count)

    plt.plot(rewards_per_episode)
    plt.xlabel("Episoden")
    plt.ylabel("Durchschnittlicher Reward")
    title = "Trainieren"
    plt.title(title)
    plt.grid()
    plt.savefig(file_name_png)
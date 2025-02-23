import math
import random
from itertools import combinations

from scipy.stats import norm


def run_s_simulations(s0, paths, delaysProb):
    count_success = 0

    # Run s0 simulations
    for sim in range(s0):
        # Create a copy of the paths for independent simulation
        paths_copy = {agent: list(path) for agent, path in paths.items()}
        # Initialize the set of active agents (agents that have not finished their path)
        active_agents = {agent for agent, path in paths_copy.items() if len(path) > 1}
        # Flag to indicate if a collision occurs
        collision = False

        while active_agents:
            # Set to track current agent locations
            locsAndEdge = set()
            # Set to track agents that have completed their paths
            agents_to_remove = set()

            for agent in list(active_agents):
                # Current path of the agent
                path = paths_copy[agent]
                lastLoc = path[0][0]

                # Simulate agent movement with a delay probability
                if random.random() > delaysProb[agent]:
                    # Remove the first step if the agent moves
                    path.pop(0)

                # Current location of the agent
                loc = path[0][0]
                # Check for collision
                if loc in locsAndEdge or (loc, lastLoc) in locsAndEdge:
                    collision = True
                    break
                locsAndEdge.add(loc)
                locsAndEdge.add((lastLoc, loc))

                # If the agent has reached its destination, mark it for removal
                if len(path) == 1:
                    agents_to_remove.add(agent)

            # Stop the simulation if a collision occurs
            if collision:
                break

            # Remove agents that have completed their paths
            active_agents -= agents_to_remove

        # Increment success count if no collision occurred
        if not collision:
            count_success += 1

    # Return the number of successful simulations
    return count_success


def verify(paths, delaysProb, no_collision_prob, verifyAlpha):
    # Calculate initial simulations size (s0) based on the desired confidence level
    z1SubAlphaSquare = (norm.ppf(1 - verifyAlpha)) ** 2
    s0 = max(30, math.ceil(z1SubAlphaSquare * (no_collision_prob / (1 - no_collision_prob))))

    # Initial simulation run
    count_success = run_s_simulations(s0, paths, delaysProb)
    # Additional simulations performed iteratively
    more_simulation = 0

    while True:
        # Calculate the estimated probability of no collision (P0)
        P0 = count_success / (s0 + more_simulation)
        # Upper confidence bound (c1)
        c1 = no_collision_prob + norm.ppf(1 - verifyAlpha) * math.sqrt((no_collision_prob * (1 - no_collision_prob)) / s0)
        # Lower confidence bound (c2)
        c2 = no_collision_prob - norm.ppf(1 - verifyAlpha) * math.sqrt((no_collision_prob * (1 - no_collision_prob)) / s0)

        # If P0 is greater than or equal to the upper bound, the solution is likely p-robust
        if P0 >= c1:
            return True
        # If P0 is less than the lower bound, the solution is not p-robust
        if P0 < c2:
            return False

        # If no decision, add one more simulation
        more_simulation += 1
        count_success += run_s_simulations(more_simulation, paths, delaysProb)


def verifyOriginal(paths, delaysProb, no_collision_prob, verifyAlpha):
    for agent1, agent2 in combinations(paths.keys(), 2):
        path1 = paths[agent1]
        path2 = paths[agent2]

        # Create loc-time dictionaries
        locTimes1 = {}
        for i, (loc, _) in enumerate(path1):
            if loc not in locTimes1:
                locTimes1[(i, loc)] = (i, loc)

        locTimes2 = {}
        for i, (loc, _) in enumerate(path2):
            if loc not in locTimes2:
                locTimes2[(i, loc)] = (i, loc)

        # Detect location conflicts
        common_locs = locTimes1.keys() & locTimes2.keys()
        if len(common_locs) != 0:
            return False

        # Create edge-time dictionaries
        edgeTimes1 = {}
        for i in range(len(path1) - 1):
            edge = (path1[i][0], path1[i + 1][0])
            if edge not in edgeTimes1:
                edgeTimes1[(i + 1, edge)] = (i + 1, edge)

        edgeTimes2 = {}
        for i in range(len(path2) - 1):
            edge = (path2[i][0], path2[i + 1][0])
            if edge not in edgeTimes2:
                edgeTimes2[(i + 1, edge)] = (i + 1, edge)

        # Detect edge conflicts, including reversed edges
        for time1, edge1 in edgeTimes1.values():
            reversed_edge1 = (edge1[1], edge1[0])
            if (time1, reversed_edge1) in edgeTimes2:
                return False

    return True


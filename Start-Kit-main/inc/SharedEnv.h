#pragma once
#include "States.h"
#include "Grid.h"
#include "nlohmann/json.hpp"
#include "Tasks.h"


class SharedEnvironment
{
public:
    int num_of_agents;
    int rows;
    int cols;
    std::string map_name;
    std::vector<int> map;
    std::string file_storage_path;

    vector< vector< tuple<int, int, int> > > goal_locations;

    int curr_timestep = 0;
    vector<State> curr_states;

    std::vector<std::pair<int, double>> manufacturerDelay_FailureProbability;
    std::vector<std::pair<double, int>> observationDelay_TotalMoves;
    int timeToDiagnosis;
    double makeSpanForCurPlan;
    std::vector<int> curAgents;
    std::vector<int> lastTimeMove;
    std::vector<Task> unfinishedTasks;


    SharedEnvironment(){}
};

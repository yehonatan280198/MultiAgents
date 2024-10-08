"""
Author: Zhongqiang (Richard) Ren
Version@2021-07
ABOUT: this file constains CBSS-MSMP, which is derived from CBSS (framework).
Oeffentlich fuer: RSS22
"""

from CBSS.libmcpf import cbss, seq_msmp

class CbssMSMP(cbss.CbssFramework):
    """
    """

    def __init__(self, grids, starts, goals, configs, delays):
        """
    """
        mtsp_solver = seq_msmp.SeqMSMP(grids, starts, goals, configs, delays)
        super(CbssMSMP, self).__init__(mtsp_solver, grids, starts, goals, dict(), configs, delays)
        return


def RunCbssMSMP(grids, starts, goals, configs, delays):
    """
    starts, goals  are all node ID.
    heu_weight and prune_delta are not in use. @2021-05-26
    """
    ccbs_planner = CbssMSMP(grids, starts, goals, configs, delays)
    path_set, search_res = ccbs_planner.Search_ml()
    res_dict = dict()
    res_dict["path_set"] = path_set
    res_dict["round"] = search_res[0]  # = num of high level nodes closed.
    res_dict["best_g_value"] = search_res[1]
    res_dict["open_list_size"] = search_res[3]
    res_dict["num_low_level_expanded"] = search_res[4]
    res_dict["search_success"] = search_res[5]
    res_dict["search_time"] = search_res[6]
    res_dict["n_tsp_call"] = search_res[7]
    res_dict["n_tsp_time"] = search_res[8]
    res_dict["n_roots"] = search_res[9]
    res_dict["assignGoals"] = ccbs_planner.mtsp.assignGoals
    return res_dict

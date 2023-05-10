from src.modules.obj.obj_wrapper import OBJ_SGL_FUNCS, OBJ_SGL_OPT_TARGET
from src.modules.opt_wrapper import SOEA_FUNCS, MOEA_FUNCS

import geatpy as ea
import numpy as np
from abc import abstractclassmethod
from typing import List, Dict, Sequence, Optional
from functools import partial


class SingleProblem(ea.Problem):
    def __init__(self, obj_func, obj_arg_info: Dict, name, M, maxormin, Dim, varTypes, lb, ub, lbin=None, ubin=None, aimFunc=None, evalVars=None, calReferObjV=None):
        super().__init__(name, M, maxormin, Dim, varTypes, lb, ub, lbin, ubin, aimFunc, evalVars, calReferObjV)
        self.obj_func = partial(obj_func, **obj_arg_info)

    def evalVars(self, Vars):
        return np.apply_along_axis(self.obj_func, 1, Vars).reshape(-1, 1)



class MultiProblem(ea.Problem):
    def __init__(self, obj_funcs, obj_arg_info: Dict, name, M, maxormin, Dim, varTypes, lb, ub, lbin=None, ubin=None, aimFunc=None, evalVars=None, calReferObjV=None):
        self.obj_funcs = [partial(obj_func, **obj_arg_info) for obj_func in obj_funcs]
        super().__init__(name, M, maxormin, Dim, varTypes, lb, ub, lbin, ubin, aimFunc, evalVars, calReferObjV)

    def evalVars(self, Vars):
        ret = []
        for func in self.obj_funcs:
            ret.append(np.apply_along_axis(func, 1, Vars))
        return np.stack(ret, axis=0).reshape(-1, len(self.obj_funcs))


class SingleChromosome_GARunner:
    def __init__(self, encode_dim: int, max_encode: int, max_iters: int, max_early_stop: int, n_ind: int, fitness_threshold: float, obj_func_list: Sequence[str], opt_algorithm_name: Optional[str] = None, logTras: Optional[int] = None , **kwargs) -> None:
        '''Initialize a single chromosome GA runner

        Args:
            encode_dim (int): encode dimension
            max_encode (int): the upper bound of encoded element
            max_iters (int): maximum evolution iteration
            max_early_stop (int): early stop if the obj value does not change for max_early_stop times
            n_ind (int): number of the first generation
            fitness_threshold (float): trapped value
            obj_func_list (Sequence[str]): obj function list as the target
            opt_algorithm_name (Optional[str], optional): opt function from geatpy. Defaults to None (Use ea.soea_SEGA_templet/).
            logTras (Optional[int], optional): record information every logTras generations
        '''
        self.n_ind = n_ind
        self.max_iters = max_iters
        self.max_early_stop = max_early_stop
        self.fitness_threshold = fitness_threshold
        self.logTras = logTras

        obj_func_target_list = [OBJ_SGL_OPT_TARGET[obj_func_name] for obj_func_name in obj_func_list]
        obj_arg_info = {'fermata_code': max_encode, 'rest_code': 0}
        
        assert len(obj_func_list) > 0, 'obj_func_list should not be empty'
        self.problem = None
        if len(obj_func_list) == 1:
            self.problem = SingleProblem(obj_func=OBJ_SGL_FUNCS[obj_func_list[0]],
                                         obj_arg_info=obj_arg_info,
                                         name='GAComposer', 
                                         M=1, 
                                         maxormin=obj_func_target_list, 
                                         Dim=encode_dim,
                                         varTypes=[1] * encode_dim,
                                         lb=[0] * encode_dim,
                                         ub=[max_encode] * encode_dim,
                                         lbin=[1] * encode_dim,
                                         ubin=[1] * encode_dim)
            if opt_algorithm_name is None:
                self.opt_algorithm = ea.soea_SEGA_templet(self.problem, ea.Population(Encoding='RI', NIND=self.n_ind), trappedValue=self.fitness_threshold, MAXGEN=max_iters, logTras=self.logTras)
        else:
            self.problem = MultiProblem(obj_funcs=[OBJ_SGL_FUNCS[obj_func_name] for obj_func_name in obj_func_list],
                                        obj_arg_info=obj_arg_info,
                                        name='GAComposer', 
                                        M=len(obj_func_list), 
                                        maxormin=obj_func_target_list, 
                                        Dim=encode_dim,
                                        varTypes=[1] * encode_dim,
                                        lb=[0] * encode_dim,
                                        ub=[max_encode] * encode_dim,
                                        lbin=[1] * encode_dim,
                                        ubin=[1] * encode_dim)
            if opt_algorithm_name is None:
                self.opt_algorithm = ea.moea_NSGA2_templet(self.problem, ea.Population(Encoding='RI', NIND=self.n_ind), trappedValue=self.fitness_threshold, MAXGEN=max_iters, logTras=self.logTras)

    def run(self, seed: int = 7, verbose: bool = False, drawing: bool = False, outputMsg: bool = True, drawLog: bool = False, saveFlag: bool = True, dirName: str = 'result', **kwargs):
        solution = ea.optimize(self.opt_algorithm, seed=seed, verbose=verbose, drawing=drawing, outputMsg=outputMsg, drawLog=drawLog, saveFlag=saveFlag, dirName=dirName, **kwargs)
        return solution

from src.modules.obj.SingleFunc import *


# Register obj functions
OBJ_SGL_FUNCS = {
    'naive': naive_fitness,
    'continous': continous_fitness,
}

# Register obj functions' target, 1 for min, -1 for max
OBJ_SGL_OPT_TARGET = {
    'naive': 1,
    'continous': -1,
}

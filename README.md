## GA Composer

Hongfei Wu

An automatic composer  based on genetic algorithm (GA).

### Installation

The dependent packages could be installed in the following ways

```shell
conda install numpy
conda install matplotlib
conda install scikit-learn
conda install music21
pip install geatpy
```

### Usage

To compose a piece of music, simply run

```shell
python compose.py -c [config_file]
```

### Examples

An example in configs/test.json

```json
{   
    // Job Name Here, used as the save directory name
    "job_name": "test",
    // Output midi file path, a file path if sample_num is None else a directory path
    "out_midi_path": "out_midi",
    // encode type, only support single track now
    "code_type": "single",
    // sample from the last generation, sample_num must be no more than n_ind
    "sample_num": 10,
    
    // Translator encode/decode a music21 stream with notes only
    "translator_args_dict": 
    {
        "pitch_lowest": "F3", 
        "pitch_highest": "G5", 
        "bar_num": 4, 
        "signature": "4/4", 
        "min_quarter_duration": 0.5 // 1 for a quarter duration
    },
    
    // GA Runner run evolution algorithm
    "ga_args_dict":
    {
        "max_iters": 128,
        "max_early_stop": 10,
        "n_ind": 32, // # of the first generation
        "fitness_threshold":  1e-4, // convergence threshold
        "obj_func_list": ["continous"], // Registed obj_functions
        "opt_algorithm_name": null,
        "logTras": null
    },
    "compose_args_dict":
    {
        "seed": 7, 
        "verbose": false, 
        "drawing": false,
        "outputMsg": true,
        "drawLog": false,
        "saveFlag": false, 
        "dirName": "result"
    }
}
```

### Developer Guidance

To implement a self-defined obj (fitness) function in this project, following the scheme as below:

1. Implement a obj function in src/modules/obj/SingleFunc.py, e.g.

   ```python
   def my_fitness(x: np.ndarray, rest_code: int, fermata_code: int):
       score = 0
       '''
        THE ARGUMENTS NAMES ARE FIXED
        
        x is a 1D np_array and denotes the encoded music stream
        rest_code: code for rest, usually 0
        fermata_code code for fermata
        
        The code froe lowest pitch to highest pitch are from [rest_code+1, fermata_code-1]
       '''
       '''
        Your fitness here
       '''
       return score
   ```

   

2. Register this function in src/modules/obj/obj_wrapper.py, e.g.

   ```python
   # Register obj functions
   OBJ_SGL_FUNCS = {
       # This name is used in config file to trigger the obj function
       'my_fitness': my_fitness,
   }
   
   # Register obj functions' target, 1 for min, -1 for max
   OBJ_SGL_OPT_TARGET = {
       # The tag is used to determine whether to maximize or minimize the function
       'my_fitness': -1,
   }
   
   ```

   

3. Now your obj function is available. Modify or create your config file and run it as the way in **Usage**.

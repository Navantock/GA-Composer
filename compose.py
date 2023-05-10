from src.Composer.GAComposer import GAComposer
from configs import parse_command_args

import json

def std_output_info(string: str) -> str:
    return "\033[32m{}\033[0m".format(string)


if __name__ == '__main__':
    print(std_output_info("Running GA Composer"))
    cmd_args = parse_command_args()
    with open (cmd_args.config_file, 'r') as f:
        settings = json.load(f)
    composer = GAComposer(settings['code_type'], settings['translator_args_dict'], settings['ga_args_dict'])
    composer.compose(job_name=settings['job_name'], 
                     out_midi_path=settings['out_midi_path'], 
                     sample_num=settings['sample_num'],
                     **settings['compose_args_dict'])
    print(std_output_info("Normal Termination of GA Composer"))
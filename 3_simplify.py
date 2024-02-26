import os
import argparse
from pathlib import Path

import common
# import pymeshlab
from tqdm.auto import tqdm


class Simplification:
    """
    Perform simplification of watertight meshes.
    """

    def __init__(self):
        """
        Constructor.
        """

        parser = self.get_parser()
        self.options = parser.parse_args()
        self.simplification_script = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'simplification.mlx')

    def get_parser(self):
        """
        Get parser of tool.

        :return: parser
        """

        parser = argparse.ArgumentParser(description='Scale a set of meshes stored as OFF files.')
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--in_dir', type=str,
                                 help='Path to input directory.')
        input_group.add_argument('--in_file', type=str,
                                 help='Path to input directory.')
        parser.add_argument("--n_views", type=int, default=100, help="Number of views per model.")
        parser.add_argument('--out_dir', type=str,
                            help='Path to output directory; files within are overwritten!')

        return parser

    def read_directory(self, directory):
        """
        Read directory.

        :param directory: path to directory
        :return: list of files
        """

        return [file for file in Path(directory).glob("**/*fused_{}.obj".format(self.options.n_views))]

    def get_in_files(self):
        if self.options.in_dir is not None:
            assert os.path.exists(self.options.in_dir)
            common.makedir(self.options.out_dir)
            files = self.read_directory(self.options.in_dir)
        else:
            files = [self.options.in_file]

        return files
    
    def get_out_path(self, filepath):
        model_id = filepath.parts[-2]
        return os.path.join(self.options.out_dir, model_id, "model_simplified.obj")

    def run(self):
        """
        Run simplification.
        """

        common.makedir(self.options.out_dir)
        files = self.get_in_files()

        for filepath in tqdm(files, total=len(files)):
            os.system('meshlabserver -i %s -o %s -s %s' % (
                filepath,
                self.get_out_path(filepath),
                self.simplification_script
            ))


if __name__ == '__main__':
    app = Simplification()
    app.run()

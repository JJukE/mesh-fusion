import os
from pathlib import Path
import argparse

import trimesh
from jjuke.utils.vis3d import MeshObjectVisualizer
from tqdm.auto import tqdm


def parse_args(input_args=None):
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--num_objs", type=int, default=100, help="Number of objects to visualize.")
    parser.add_argument("--file_name", type=str, default="model_fused", help="File name or a part of it to recognize the specific obj file to visualize.")
    parser.add_argument("--input_dir", type=str, help="Input directory path to visualize.")
    parser.add_argument("--output_dir", type=str, help="Output directory path to save meshes.")
    args = parser.parse_args()
    
    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()
    
    return args


def main(args):
    visualizer = MeshObjectVisualizer()
    
    paths = list(Path(args.input_dir).glob(f"**/*{args.file_name}*.obj"))
    
    print("Number of files: ", len(paths))
    
    vertices = []
    faces = []
    num_err_objs = 0
    for i, path in tqdm(enumerate(paths), total=args.num_objs):
        if i >= args.num_objs:
            break
        try:
            mesh = trimesh.load(path)
            vertices.append(mesh.vertices)
            faces.append(mesh.faces)
        except AttributeError as e:
            print(f"Error occurerd while processing {i+1}.obj -> {e}")
            num_err_objs += 1
            continue
    print(f"There are {num_err_objs} weird objects.")
    
    os.makedirs(args.output_dir, exist_ok=True)
    visualizer.save(str(Path(args.output_dir) / f"{args.file_name}_visualization.obj"),
                    vertices=vertices, triangles=faces, num_in_row=10)


if __name__ == "__main__":
    args = parse_args()
    main(args)
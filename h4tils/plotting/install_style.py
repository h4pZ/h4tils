#!/usr/bin/python

import os
import sys
from shutil import copy


def install_hibm():
    style_path = os.path.join(os.path.dirname(__file__), "hibm.mplstyle")

    # Getting all the anaconda enviroments.
    home = os.getenv("HOME")
    envs_path = os.path.join(home, "anaconda3/envs/")
    envs = os.listdir(envs_path)
    envs = [env for env in envs if "." not in env]

    print(f"Found {len(envs)} environments:")
    for env in envs:
        print("  -", env)
    print("")

    # Constructing the matplotlib paths
    mpl_paths = [os.path.join(envs_path, env, "lib") for env in envs]
    mpl_paths

    for i, path in enumerate(mpl_paths):
        folders = os.listdir(path)

        for folder in folders:
            if "python" == folder[:6]:
                path = os.path.join(path, folder)
                mpl_paths[i] = path
                break

    mpl_paths = [os.path.join(path, "site-packages") for path in mpl_paths]

    # Start copying the styles into each env.
    print("Copying the style into each environment...")
    for i, path in enumerate(mpl_paths):
        path = os.path.join(path, "matplotlib/mpl-data/stylelib/")

        if os.path.exists(path):
            copy(style_path, path)
            print(f"Style copied into {envs[i]}")
        else:
            print(f"Error: matplotlib path not found in {envs[i]} env")

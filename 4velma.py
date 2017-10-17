# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT
import argparse
from src.viewer import Viewer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display pictures for your grandma.')
    parser.add_argument('--fullscreen', type=bool, default=False,
                        help='scale to use full screen')
    parser.add_argument('--input', required=True,
                        help='directory containing images')
    parser.add_argument('--duration', type=int, default=60, required=False,
                        help='display pictures for n seconds')

    args = parser.parse_args()
    viewer = Viewer(args.input, args.duration, full_screen=args.fullscreen)
    viewer.run()

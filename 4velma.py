# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT
import argparse
from src.viewer import Viewer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display pictures for your grandma.')
    parser.add_argument('--fullscreen', '-f', dest='fullscreen', action='store_true',
                        help='scale to use full screen')
    parser.add_argument('--input', '-i', required=True,
                        help='directory containing images')
    parser.add_argument('--duration', '-d', type=int, default=60, required=False,
                        help='display pictures for n seconds, default 60s')

    args = parser.parse_args()
    viewer = Viewer(args.input, args.duration, full_screen=args.fullscreen)
    viewer.run()

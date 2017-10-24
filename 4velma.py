# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT
from src.viewer import Viewer
from src.viewer.logging import init_logging


if __name__ == "__main__":
    init_logging()
    args = Viewer.parse_args()
    viewer = Viewer(args.input, args.duration, full_screen=args.fullscreen)
    viewer.run()

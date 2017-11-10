# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT
from src.viewer import Mover
from src.viewer.logging import init_logging


if __name__ == "__main__":
    init_logging()
    args = Mover.parse_args()
    mover = Mover(args.mountpoint, args.destination)
    mover.run()

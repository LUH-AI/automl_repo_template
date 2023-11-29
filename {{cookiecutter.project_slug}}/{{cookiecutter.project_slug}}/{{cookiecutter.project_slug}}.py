"""Main module."""

import os
import sys
import signal
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class HandleTermination:
    """This is a context manager that handles different termination signals. The comments show how to save a model and optimizer states even if there's an error in the code."""
    def __init__(self, directory):
        # self.model = model
        # self.optimizer = optimizer
        self.directory = Path(directory)

    def __enter__(self):
        self.old_sigterm_handler = signal.signal(signal.SIGTERM, self.handle_sigterm)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        signal.signal(signal.SIGTERM, self.old_sigterm_handler)

        # An exception was raised, so save the model and optimizer states with an exception tag before re-raising 
        if exc_type is not None:
            logger.info("Oh no, there was an exception!")
            #torch.save({
            #    'model_state_dict': self.model.state_dict(),
            #    'optimizer_state_dict': self.optimizer.state_dict(),
            #}, self.directory / f'checkpoint_exc.pth')

        # Everything ran perfectly, so save the final model and optimizer states
        if exc_type is None:
            logger.info("All clear!")
            #torch.save({
            #    'model_state_dict': self.model.state_dict(),
            #    'optimizer_state_dict': self.optimizer.state_dict(),
            #}, self.directory / f'checkpoint_final.pth')

        return False

    def handle_sigterm(self, signum, frame):
        # save the model and optimizer states before exiting
        logger.info(f"Saving checkpoint to {self.directory}/checkpoint_sigterm.pth")
        # torch.save({

        #     'model_state_dict': self.model.state_dict(),
        #     'optimizer_state_dict': self.optimizer.state_dict(),
        # }, self.directory / f'checkpoint_sigterm.pth')
        sys.exit(0)

def cool_things(cfg):
    with HandleTermination(os.getcwd()):
        print(f"Your current config is: {cfg}")
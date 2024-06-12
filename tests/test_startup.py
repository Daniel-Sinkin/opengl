"""
Runs the engine for some steps to make sure it doesn't immediately crash.
"""

import os
import shutil
import time

from src.graphics_engine import GraphicsEngine


def test_fresh_startup():
    """
    Wipes all files that aren't inherent to the repo to make sure the file and folder creation logic is stable.
    """
    folders_to_be_deleted = ["objects", "recordings", "logs"]
    for folder in folders_to_be_deleted:
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)
            print(f"Deleted directory: {folder}")
        else:
            print(f"Directory not found: {folder}")

    graphics_engine = GraphicsEngine(scene_id="DEBUG")
    graphics_engine.take_screenshot_after_render = True
    graphics_engine.screenshot_prefix = "test_fresh_startup_"

    graphics_engine.iteration()

import os

import numpy as np
import pygame as pg
from moderngl import Buffer, Context, Texture
from PIL import Image


class TextureHandler:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.texture_folderpath = "textures"
        self.textures: dict[int, Texture] = {
            i: self.get_texture(os.path.join(self.texture_folderpath, f"img_{i}.png"))
            for i in range(3)
        }

    def get_texture(self, filepath: str) -> Texture:
        image = Image.open(filepath)
        image = image.convert("RGB")

        data = np.array(image).tobytes()

        return self.ctx.texture(size=image.size, components=3, data=data)

    def destroy(self) -> None:
        for texture in self.textures.values():
            texture.release()

import os
import typing

import numpy as np
import pygame as pg
from moderngl import LINEAR, LINEAR_MIPMAP_LINEAR, Buffer, Context, Texture
from PIL import Image

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class TextureHandler:
    def __init__(self, app: "GraphicsEngine"):
        self.app = app
        self.ctx = app.ctx
        self.texture_folderpath = "textures"
        self.textures: dict[int, Texture] = {
            i: self.get_texture(
                os.path.join(self.texture_folderpath, f"img_{i}.png"), mode=0
            )
            for i in range(3)
        }
        self.textures["cat"] = self.get_texture(
            "objects/cat/20430_cat_diff_v1.jpg", mode=1
        )
        self.textures["skybox_debug"] = self.get_texture_cube(
            os.path.join(self.texture_folderpath, "skybox"), ext="png"
        )
        self.textures["skybox"] = self.get_texture_cube(
            os.path.join(self.texture_folderpath, "skybox1"), ext="png"
        )
        self.textures["depth_texture"] = self.get_depth_texture()

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.window_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, filepath: str, ext="png"):
        faces = ["right", "left", "top", "bottom", "back", "front"]

        textures = []
        for face in faces:
            texture = pg.image.load(os.path.join(filepath, f"{face}.{ext}"))
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        assert len(set([texture.get_size() for texture in textures])) == 1
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, filepath: str, mode=0) -> Texture:
        if mode == 0:
            image = Image.open(filepath)
            image = image.convert("RGB")

            data = np.array(image).tobytes()

            texture = self.ctx.texture(size=image.size, components=3, data=data)

            texture.filter = (LINEAR_MIPMAP_LINEAR, LINEAR)
            texture.build_mipmaps()

            texture.anisotropy = 16.0

            return texture
        else:
            texture = pg.image.load(filepath).convert()
            texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=3,
                data=pg.image.tostring(texture, "RGB"),
            )
            # mipmaps
            texture.filter = (LINEAR_MIPMAP_LINEAR, LINEAR)
            texture.build_mipmaps()
            # AF
            texture.anisotropy = 32.0
            return texture

    def destroy(self) -> None:
        for texture in self.textures.values():
            texture.release()

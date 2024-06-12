from . import *

""""""

from .settings import Folders

if TYPE_CHECKING:
    from .graphics_engine import GraphicsEngine


class TextureHandler:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        self.ctx: Context = app.ctx
        self.texture_folderpath: str = Folders.TEXTURES
        self.textures: dict[int, Texture] = {
            i: self.get_texture(
                os.path.join(self.texture_folderpath, f"img_{i}.png"), mode=0
            )
            for i in range(3)
        }
        self.textures["cat"] = self.get_texture(
            os.path.join(Folders.DATA_OBJ, "cat", "20430_cat_diff_v1.jpg"), mode=1
        )
        self.textures["skybox_debug"] = self.get_texture_cube(
            os.path.join(self.texture_folderpath, "skybox"), ext="png"
        )
        self.textures["skybox"] = self.get_texture_cube(
            os.path.join(self.texture_folderpath, "skybox1"), ext="png"
        )
        self.textures["depth_texture"] = self.get_depth_texture()

    def get_depth_texture(self) -> Texture:
        depth_texture: Texture = self.ctx.depth_texture(self.app.window_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, filepath: str, ext="png") -> TextureCube:
        faces = ["right", "left", "top", "bottom", "back", "front"]

        textures: list[pg.Surface] = []
        for face in faces:
            texture: pg.Surface = pg.image.load(os.path.join(filepath, f"{face}.{ext}"))
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        assert len(set([texture.get_size() for texture in textures])) == 1
        size: tuple[int] = textures[0].get_size()
        texture_cube: TextureCube = self.ctx.texture_cube(
            size=size, components=3, data=None
        )

        for i in range(6):
            texture_data: bytes = pg.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, filepath: str, mode=0) -> Texture:
        if mode == 0:
            image: Image.Image = Image.open(filepath)
            image = image.convert("RGB")

            data: bytes = np.array(image).tobytes()

            texture: Texture = self.ctx.texture(
                size=image.size, components=3, data=data
            )

            texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
            texture.build_mipmaps()

            texture.anisotropy = 16.0

            return texture
        else:
            texture: Texture = pg.image.load(filepath).convert()
            texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=3,
                data=pg.image.tostring(texture, "RGB"),
            )
            # mipmaps
            texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
            texture.build_mipmaps()
            # AF
            texture.anisotropy = 32.0
            return texture

    def destroy(self) -> None:
        for texture in self.textures.values():
            texture.release()

import os
import pygame

import engine.context as ctx

# ---------------------------- #
# util functions

WIDTH = "w"
HEIGHT = "h"
PADX = "padx"
PADY = "pady"
SPACINGX = "spacingx"
SPACINGY = "spacingy"
FRAMEDATA = "framedata"

HORIZONTAL_TILES = "horizontal_tiles"
VERTICAL_TILES = "vertical_tiles"

SPRITESHEET_PADDING = "||"

DEFAULT_CONFIG = {
    "w": 18,
    "h": 18,
    "padx": 0,
    "pady": 0,
    "spacingx": 0,
    "spacingy": 0,
    "framedata": False,
}


# ---------------------------- #
# sprite sheet object


class SpriteSheet:

    # ---------------------------- #

    def __init__(self, path: str, config: dict = DEFAULT_CONFIG, framedata: list = []):
        """
        Create a new spritesheet


        framedata = [
            {x: 0, y: 0, w: 18, h: 18, file: "sprite1"}, # names should follow format of: path-index.elemg
            {x: 18, y: 0, w: 18, h: 18, file: "sprite2"},
            {x: 36, y: 0, w: 18, h: 18, file: "sprite3"},
        ]
        """
        self._path = path
        self._json = None
        self._config = config.copy()
        self._frames = []
        self._framedata = framedata

        if path.endswith(".json"):
            self._json = path
            self._load_json_config(path)

        self.image = ctx.CTX_RESOURCE_MANAGER.load(self._path)
        self.sprites = []

        # load sprites
        self._load_sprites()

        # [print(entry) for entry in self.sprites]

    # ---------------------------- #
    # logic

    def _load_json_config(self, path: str):
        """Load a json config file"""
        data = io.json_to_dict(path)
        self._path = os.path.dirname(self._json) + "/" + data["meta"]["image"]

        # the aseprite files should NOT have padding/margins
        size = (data["frames"][0]["frame"]["w"], data["frames"][0]["frame"]["h"])
        self._frames = data["frames"]
        self._config[WIDTH] = size[0]
        self._config[HEIGHT] = size[1]
        self._config[HORIZONTAL_TILES] = data["meta"]["size"]["w"] // size[0]
        self._config[VERTICAL_TILES] = data["meta"]["size"]["h"] // size[1]

    def _load_sprites(self):
        """Loads all sprites from the spritesheet - including empty ones"""
        self.sprites.clear()

        # if its a json file, we follow the json config
        if self._json and not self._config[FRAMEDATA]:
            for framedata in self._frames:
                _frame = framedata["frame"]
                _fname = framedata["filename"]

                # get the snippet
                snip = self.image.subsurface(
                    (_frame["x"], _frame["y"], _frame["w"], _frame["h"])
                ).convert_alpha()
                self.sprites.append(
                    (
                        _fname,
                        snip,
                        pygame.Rect(_frame["x"], _frame["y"], _frame["w"], _frame["h"]),
                    )
                )

        # if its a spritesheet, we do default config
        elif not self._json and self._path and not self._config[FRAMEDATA]:
            left = 0
            top = 0

            max_width = self.image.get_width()
            max_height = self.image.get_height()

            padx = self._config[PADX]
            pady = self._config[PADY]
            spacingx = self._config[SPACINGX]
            spacingy = self._config[SPACINGY]
            width = self._config[WIDTH]
            height = self._config[HEIGHT]

            # load all the sprites
            left += self._config[PADX]
            while top <= max_height - pady - height:
                while left <= max_width - padx - width:
                    _cache_string = self.gen_sprite_str_id(len(self.sprites) - 1)
                    # get the snippet
                    snip = self.image.subsurface(
                        left, top, width, height
                    ).convert_alpha()
                    self.sprites.append(
                        (_cache_string, snip, pygame.Rect(left, top, width, height))
                    )
                    left += spacingx + width

                # reset left
                top += spacingy + height
                left = padx
        else:
            # load from framedata
            for framedata in self._framedata:
                _frame = framedata[0:4]
                _fname = framedata[4]

                # get snippet
                snip = self.image.subsurface(
                    (_frame[0], _frame[1], _frame[2], _frame[3])
                ).convert_alpha()
                self.sprites.append(
                    (
                        _fname,
                        snip,
                        pygame.Rect(_frame[0], _frame[1], _frame[2], _frame[3]),
                    )
                )

        # set other variables
        self._config[HORIZONTAL_TILES] = (
            self.image.get_size()[0] - self._config[SPACINGX]
        ) // (self._config[WIDTH] + self._config[SPACINGX])
        self._config[VERTICAL_TILES] = (
            self.image.get_size()[1] - self._config[SPACINGY]
        ) // (self._config[HEIGHT] + self._config[SPACINGY])

    def gen_sprite_str_id(self, index: int):
        """Generate the sprite uuid"""
        return f"{self._path}||{index}"

    def get_sprite_str_id(self, index: int):
        """Get the sprite uuid"""
        return self.sprites[index][0]

    # ---------------------------- #
    # utils

    def __getitem__(self, key: int):
        """Get the sprite"""
        return self.sprites[key][1]

    def __iter__(self):
        """Iterate over the sprites"""
        return iter(self.sprites)

    def __len__(self):
        """Get the number of sprites"""
        return len(self.sprites)

    def __hash__(self):
        """Hash the spritesheet"""
        hashable = tuple([self._path] + list(flatten_config_values(self._config)))
        return hash(hashable)

    def get_config(self):
        """Get the config"""
        return self._config


# ---------------------------- #
# functions


def __create_config(
    width: int,
    height: int,
    padx: int = 0,
    pady: int = 0,
    spacingx: int = 0,
    spacingy: int = 0,
    framedata: bool = False,
):
    return {
        "w": width,
        "h": height,
        "padx": padx,
        "pady": pady,
        "spacingx": spacingx,
        "spacingy": spacingy,
        "framedata": framedata,
    }


def flatten_config_values(config: dict = DEFAULT_CONFIG):
    """Flatten the config values"""
    return (
        config[WIDTH],
        config[HEIGHT],
        config[PADX],
        config[PADY],
        config[SPACINGX],
        config[SPACINGY],
        config[FRAMEDATA],
    )


def generate_config_from_json(json_path: str):
    """Generate a config from a json file"""
    data = io.json_to_dict(json_path)
    meta = data["meta"]
    frame = data["frames"][0]["frame"]
    return __create_config(
        frame["w"], frame["h"], padx=0, pady=0, spacingx=0, spacingy=0
    )


def load_spritesheet(
    image_path: str, config: dict = DEFAULT_CONFIG, framedata: list = []
):
    """Load a spritesheet"""
    # check if its a json
    _json_path = None
    if image_path.endswith(".json"):
        # load the json + find the image path
        data = io.json_to_dict(image_path)
        _json_path = image_path
        image_path = os.path.dirname(image_path) + "/" + data["meta"]["image"]
        config = generate_config_from_json(_json_path)
    # check if has framedata
    if framedata != []:
        config[FRAMEDATA] = True

    # create new spritesheet + cache it
    result = SpriteSheet(
        _json_path if _json_path else image_path, config, framedata=framedata
    )
    return result

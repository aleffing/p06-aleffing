# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def get_context():
    cfg = Config(SECURITY_KEY="ACME-SEC", ENGINE="thumbor.engines.pil")
    cfg.LOADER = "thumbor.loaders.file_loader"
    cfg.STORAGE = "thumbor.storages.no_storage"
    cfg.PILLOW_PRESERVE_INDEXED_MODE = True
    return Context(config=cfg)


def make_palette_gif_with_transparent_corner():
    source = Image.new("RGBA", (40, 40), (0, 0, 255, 255))
    for x in range(20):
        for y in range(20):
            source.putpixel((x, y), (0, 0, 0, 0))
    buffer = BytesIO()
    source.save(buffer, "GIF")
    return buffer.getvalue()


def test_resized_gif_keeps_transparency_index():
    engine = Engine(get_context())
    engine.load(make_palette_gif_with_transparent_corner(), ".gif")

    engine.resize(20, 20)
    img = Image.open(BytesIO(engine.read(".gif")))
    rgba = img.convert("RGBA")

    assert "transparency" in img.info
    assert rgba.getpixel((0, 0))[3] == 0
    assert rgba.getpixel((19, 19))[3] == 255

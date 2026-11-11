# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerTransparentEdgeTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_round_corner_edge_is_partly_transparent(self):
        image = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(50,255,0,0,1)",
            mode="RGBA",
        )

        # The 50px top-left corner box holds the arc. Its edge pixels must
        # fade through alpha, so some of them are neither 0 nor 255.
        corner = image.crop((0, 0, 50, 50))
        alphas = {pixel[3] for pixel in corner.getdata()}

        assert any(0 < alpha < 255 for alpha in alphas)

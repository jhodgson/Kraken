from kraken.tests.bob_rig import Rig
from kraken.core.builders.base_builder import BaseBuilder

bobRig = Rig("char_bob")

builder = BaseBuilder()
builder.build(bobRig)
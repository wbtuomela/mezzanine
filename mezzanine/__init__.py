# JJANJ: report the released base version instead of the semantic-release
# placeholder. Upstream's tag carries ``9999dev0`` and the release build stamps
# ``5.1.4``; keeping the placeholder makes this checkout fail Cartridge 1.0.0b1's
# ``mezzanine>=5.1.3,<6`` requirement, so pipenv cannot resolve the two forks.
__version__ = "5.1.4"

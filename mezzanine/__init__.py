# JJANJ: report a concrete 6.x version instead of the semantic-release
# placeholder. Upstream's unreleased master carries ``9999dev0`` and the release
# build stamps the real version; the placeholder parses as ``9999.dev0``, which
# falls outside Cartridge v1.3.4's ``mezzanine>=6,<7`` requirement, so pipenv
# cannot resolve the two forks into one lock. Step 7a targets the post-6.1.1
# master line, so stamp the next minor (6.2.0). Packaging only; no behaviour
# change. Ported from the step-6b fork commit 0611245d.
__version__ = "6.2.0"

local_n2g_sources = [
    'PyNotam/_abbr.py',
    'PyNotam/notam.py',
    'PyNotam/_parser.py',
    'PyNotam/timeutils.py',
    '__init__.py',
]

# I hate how this works with a firy passion. It took me like, 5 hours to find
# the note about `prefix` needing to be `usr` on Linux, and it requires root
# to install directly to the system. Maybe there's a way to do this with both
# meson and a python venv, but I'm too ficking pissed to figure it out right now
# https://mesonbuild.com/Builtin-options.html#python-module
if not pymod.find_installation(modules: 'PyNotam').found()
python_installation.install_sources( # Install_sources is for local stuff
	local_n2g_sources,
	subdir: 'PyNotam', # Not the same as subdir(); actually install_dir
)
endif

pip_modules = [
	'parsimonious',
	'timeutils',
]

pymod.find_installation(modules: pip_modules)

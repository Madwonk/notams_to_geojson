defs_conf = configuration_data()
defs_conf.set('DATADIR', datadir)
defs_conf.set('LIBEXECDIR', libexecdir)
defs_conf.set('VERSION', meson.project_version())

n2g_sources = [
  'converter.py',
]

# if not pymod.find_installation(modules: 'n2g', required:false).found()
	python_installation.install_sources(n2g_sources, subdir: 'n2g')
# endif

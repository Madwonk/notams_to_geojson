project('notams_to_geojson',
          version: '0.1.0',
    meson_version: '>= 0.60.0',
  default_options: [
    'warning_level=2',
    'python.platlibdir=/usr/lib/python3/dist-packages', # yes I know, this is slightly evil. but it works
    'python.purelibdir=/usr/lib/python3/dist-packages', # this too, even more so TBH
                   ],
)

pymod = import('python')
python_installation = pymod.find_installation('python3')
message( ' '.join( [ 'Installing python sector in', python_installation.get_install_dir() ] ) )

prefix = get_option('prefix')

bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
libexecdir = join_paths(prefix, get_option('libexecdir'))
pythondir = join_paths(prefix, python_installation.get_path('purelib'))

pkgdatadir = join_paths(datadir, meson.project_name())

appdatadir = join_paths(datadir, 'metainfo')
desktopdir = join_paths(datadir, 'applications')

# Since Python is interpreted, we use install_data pointed to the bindir
# instead of "executable()" or some similar thing.
install_data('notams_to_geojson', install_mode: 'rwxr-xr-x', install_dir: get_option('bindir'))

subdir('deps')
subdir('n2g')

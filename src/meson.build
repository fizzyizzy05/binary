pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'binary'
gnome = import('gnome')

gnome.compile_resources('binary',
  'binary.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'binary.in',
  output: 'binary',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

binary_sources = [
  '__init__.py',
  'main.py',
  'preferences.py',
  'window.py',
  'bitCount.py',
]

install_data(binary_sources, install_dir: moduledir)

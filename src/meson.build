pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'binary'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/help-overlay.blp',
    'preferences.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)


gnome.compile_resources('binary',
  'binary.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)
conf.set('app_id', app_id)
conf.set('profile', get_option('profile'))

configure_file(
  input: 'binary.in',
  output: 'binary',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

configure_file(
  input: 'profile.py.in',
  output: 'profile.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

binary_sources = [
  '__init__.py',
  'main.py',
  'preferences.py',
  'window.py',
]

binary_libs = [
  'lib/bit_count.py',
  'lib/get_answer.py',
]

binary_sources += binary_libs

install_data(binary_sources, install_dir: moduledir)

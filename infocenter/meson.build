pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/action-row.blp',
    'gtk/disclaimer.blp',
    'gtk/quicklink.blp',
    'gtk/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

about_conf = configuration_data()
about_conf.set('PACKAGE_URL', package_url)
about_conf.set('CONTRIBUTORS', contributors)
about_conf.set('ARTISTS', artists)
about_conf.set('APPID', application_id)
about_conf.set('VERSION', version)
about_conf.set('COPYRIGHT', copyright)

gnome.compile_resources('infocenter',
  'infocenter.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: [blueprints,
    configure_file (
      input: 'gtk/about_dialog.ui.in',
      output: '@BASENAME@',
      configuration: about_conf
  )]
)

python = import('python')
python3 = python.find_installation('python3')

conf = configuration_data()
conf.set('PYTHON', python3.full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'infocenter.in',
  output: 'infocenter',
  configuration: conf,
  install_dir: get_option('bindir'),
  install: true,
)

conf = configuration_data()

conf.set('DATA_DIR', DATA_DIR)
conf.set('PYTHON', python_bin.full_path())

configure_file(
  input: 'const.py.in',
  output: 'const.py',
  configuration: conf,
  install_dir: join_paths(python_dir, 'infocenter'),
  install: true
)

install_subdir(
  meson.current_source_dir(),
  exclude_directories: ['.mypy_cache', '__pycache__'],
  exclude_files: ['const.py.in', 'meson.build'],
  install_dir: python_dir,
)

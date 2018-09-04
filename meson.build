project('shuttlebackup',         version: '3.1.0',
  meson_version: '>= 0.46.0',
)

subdir('src')

message('Looking for dependencies...')

py3 = find_program('python3', required : true)

install_data(sources : 'src/shuttlebackup.py', rename : 'shuttlebackup', install_dir : '/usr/local/bin')
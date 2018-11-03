project('shuttlebackup',         version: '3.3.0',
  meson_version: '>= 0.46.0',
)

subdir('src')

message('Looking for dependencies...')

py3 = find_program('python3', required : true)

mkexec = run_command('chmod', '+x', 'src/shuttlebackup.py')

if mkexec.returncode() != 0
  message('Failed to change permissions.')
endif

if mkexec.returncode() == 0
  install_data(sources : 'src/shuttlebackup.py', rename : 'shuttlebackup', install_dir : '/usr/bin')
endif
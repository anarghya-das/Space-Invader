import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Space Invader",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["assets/"]}},
    executables=executables
)

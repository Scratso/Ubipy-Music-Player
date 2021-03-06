import cx_Freeze

executables = [cx_Freeze.Executable("Ubipy Music Player.py",
                                    shortcutName="Ubipy Music Player",
                                    shortcutDir="StartMenuFolder")]

# version number:
# a.b.c
#
# where a is 0, or 1. 0 = non-release, 1 = release. (beta and below is 0)
# b is the year of release.
# c is the edit number (147, as an example.)

cx_Freeze.setup(
    name="Ubipy Music Player",
    author="Damian Heaton",
    version="0.2016.3",
    options={"build_exe": {"packages":["pygame", "mutagen", "easygui", "pylast"],
                           "excludes": [],
                           "include_files":["music", "res", "src",
                                            "albumart-placeholder.png",
                                            "..\\LICENSE", "..\\README.md",
                                            "Ubipy Music Player.py"]},
             "bdist_msi": { } },
    executables = executables

    )

print("compiled")

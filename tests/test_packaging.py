"""Guards the exact bug this test suite was added for: materials.library's
CSV data files must ship with the installed package, not just be present
in the source tree during an editable install.
"""

import importlib.resources as pkg_resources


def test_library_csv_files_are_importable_package_data():
    for filename in ("elements.csv", "nubase2020.csv"):
        with pkg_resources.path("materials.library", filename) as path:
            assert path.is_file(), f"missing packaged data file: {filename}"

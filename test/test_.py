import filecmp
import io
import os
import re
import subprocess
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modpack_changelogger import generate_changelog  # pylint:disable=C0413

OLD_PACK = "test/packs/old.mrpack"
NEW_PACK = "test/packs/new.mrpack"


def test_mr():
    expected_output = "test/expected/mr.md"

    generate_changelog(OLD_PACK, NEW_PACK, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_cf():
    expected_output = "test/expected/cf.md"

    generate_changelog("test/packs/old.zip", "test/packs/new.zip", None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_cli():
    expected_output = "test/expected/cli.md"

    result = subprocess.run(
        ["modpack-changelogger", "-o", OLD_PACK, "-n", NEW_PACK, "-f", "Changelog.md"],
        check=False,
    )
    assert result.returncode == 0
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_custom_changelog_file():
    expected_output = "test/expected/custom_changelog_file.md"

    try:
        generate_changelog(OLD_PACK, NEW_PACK, None, "custom_name.md")
        assert filecmp.cmp("custom_name.md", expected_output, shallow=False)
    finally:
        if os.path.exists("custom_name.md"):
            os.remove("custom_name.md")


def test_formatted():
    expected_output = "test/expected/formatted.md"
    with open(expected_output, encoding="utf-8") as file:
        expected_output = file.read()

    assert expected_output == generate_changelog(OLD_PACK, NEW_PACK, None, "formatted")


def test_unformatted():
    expected_output_file = "test/expected/unformatted.md"

    output1, output2, output3 = generate_changelog(
        OLD_PACK,
        NEW_PACK,
        None,
        "unformatted",
    )

    with open(expected_output_file, encoding="utf-8") as f:
        expected1, expected2, expected3 = f.read().split("\n")

    assert str(output1) == expected1.strip()
    assert str(output2) == expected2.strip()
    assert str(output3) == expected3.strip()


def test_console():
    expected_output_file = "test/expected/console.md"

    console_output = io.StringIO()
    sys.stdout = console_output
    generate_changelog(OLD_PACK, NEW_PACK, None, "console")
    sys.stdout = sys.__stdout__
    console_output = console_output.getvalue()

    with open(expected_output_file, encoding="utf-8") as file:
        expected_output = file.read()

    assert expected_output == console_output


def test_config_new():
    try:
        result = subprocess.run(
            ["modpack-changelogger", "newconfig"],
            check=False,
            stdout=subprocess.PIPE,
        )
        assert result.returncode == 0
        assert os.path.isfile("config.json")
        assert (
            result.stdout.decode("utf-8")
            == f"A new configuration file has been created successfully.{os.linesep}"
        )
    finally:
        os.remove("config.json")


def test_version():

    result = subprocess.run(
        ["modpack-changelogger", "-v"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert (
        re.match(r"Modpack Changelogger \d+\.\d+\.\d+(-\w+)?", result.stdout.strip())
        is not None
    )

    assert result.returncode == 0


def test_cli_no_args_shows_help():
    result = subprocess.run(
        ["modpack-changelogger"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_cli_partial_args_returns_usage_error():
    result = subprocess.run(
        ["modpack-changelogger", "-o", OLD_PACK],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "Provide both --old and --new modpacks for comparison" in result.stderr


def test_check_options():
    config_path = "test/configs/check_options.json"
    expected_output = "test/expected/check_options.md"

    generate_changelog(OLD_PACK, NEW_PACK, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_comma():
    config_path = "test/configs/comma.json"
    expected_output = "test/expected/comma.md"

    generate_changelog(OLD_PACK, NEW_PACK, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_ind_bullet():
    config_path = "test/configs/ind_bullet.json"
    expected_output = "test/expected/ind_bullet.md"

    generate_changelog(OLD_PACK, NEW_PACK, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_ind_comma():
    config_path = "test/configs/ind_comma.json"
    expected_output = "test/expected/ind_comma.md"

    generate_changelog(OLD_PACK, NEW_PACK, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_header():
    config_path = "test/configs/header.json"
    expected_output = "test/expected/header.md"

    generate_changelog(OLD_PACK, NEW_PACK, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_broken_config():
    config_path = "test/configs/broken_config.json"

    with pytest.raises(ValueError):
        generate_changelog(OLD_PACK, NEW_PACK, config_path, None)


def test_inavlid_config_path():
    config_path = "invalid_config.json"

    with pytest.raises(FileNotFoundError):
        generate_changelog(OLD_PACK, NEW_PACK, config_path, None)

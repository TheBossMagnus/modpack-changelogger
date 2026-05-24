import hashlib
import json
import os
import tempfile
import zlib
from zipfile import BadZipFile, ZipFile

from .utils import (
    DifferentModpackFormatError,
    ModpackFormatError,
    UnsupportedModpackFormatError,
)


def get_json(MODPACKS_FORMAT, path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")

    if path.endswith(".mrpack"):
        if MODPACKS_FORMAT == "curseforge":
            raise DifferentModpackFormatError("curseforge", "modrinth")
        MODPACKS_FORMAT = "modrinth"

    elif path.endswith(".zip"):
        if MODPACKS_FORMAT == "modrinth":
            raise DifferentModpackFormatError("modrinth", "curseforge")
        MODPACKS_FORMAT = "curseforge"

    else:
        raise UnsupportedModpackFormatError(path)

    # Create a temporary directory to extract the modpack into
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Unpack the modpack file into the temp directory
            with ZipFile(path, "r") as zip_obj:
                zip_obj.extractall(path=temp_dir)

            # Get config folder hash
            config_hash = hash_directory(os.path.join(temp_dir, "overrides", "config"))
            script_hash = hash_directory(os.path.join(temp_dir, "overrides", "scripts"))
            overrides_name = get_overrides(os.path.join(temp_dir, "overrides", "mods"))

            # Parse the json file
            json_path = os.path.join(
                temp_dir,
                "modrinth.index.json"
                if MODPACKS_FORMAT == "modrinth"
                else "manifest.json",
            )
            with open(json_path, encoding="utf-8") as json_file:
                return (
                    MODPACKS_FORMAT,
                    json.load(json_file),
                    config_hash,
                    script_hash,
                    overrides_name,
                )
        except FileNotFoundError as error:
            raise ModpackFormatError(
                path,
                "missing manifest.json or modrinth.index.json",
            ) from error
        except json.JSONDecodeError as error:
            raise ModpackFormatError(
                path,
                "invalid manifest.json or modrinth.index.json",
            ) from error
        except BadZipFile as error:
            raise ModpackFormatError(
                path,
                "corrupted or invalid compression of the mrpack file",
            ) from error


def hash_directory(directory):
    crc = 0
    chunk_size = 4096  # Read files in 4KB chunks
    for dirpath, _, filenames in os.walk(directory):
        for filename in sorted(filenames):  # Sort filenames for consistent hashing
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        crc = zlib.crc32(chunk, crc)
            except OSError:
                continue
    return f"{crc & 0xFFFFFFFF:08x}"  # Return CRC32 as an 8-character hex string


def calculate_hash(filename):
    hash_sha512 = hashlib.sha512()
    chunk_size = 4096  # Read files in 4KB chunks
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()


def get_overrides(directory):
    hash_dict = {}
    if not os.path.exists(directory):
        return hash_dict  # Return empty dict if directory doesn't exist
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            hash_dict[file] = file_hash
    return hash_dict

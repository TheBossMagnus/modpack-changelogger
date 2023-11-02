import re
import asyncio
from get_mod_name import get_mod_name

def compare_packs(old_json, new_json, config): 
    # Get the Minecraft version from both packs
    old_mc_version = old_json['dependencies']['minecraft']
    new_mc_version = new_json['dependencies']['minecraft']

    # Get the loader and its version from the index.json
    old_loader = list(old_json['dependencies'].keys())[0]
    old_loader_version = old_json['dependencies'][old_loader]
    new_loader = list(new_json['dependencies'].keys())[0]
    new_loader_version = new_json['dependencies'][new_loader]

    # Load the list of mods from both packs
    added_urls = [url['downloads'] for url in new_json['files']]
    removed_urls = [url['downloads'] for url in old_json['files']]

    # Remove any URLs that are in both packs
    for added_url in added_urls.copy():
        for removed_url in removed_urls.copy():
            if added_url == removed_url:
                added_urls.remove(added_url)
                removed_urls.remove(removed_url)

    # Extract the mod IDs from the URLs
    added_ids = [re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0) for url in added_urls]
    removed_ids = [re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0) for url in removed_urls]

    # Find the IDs of any updated mods
    updated_ids = []
    for added_id in added_ids.copy():
        for removed_id in removed_ids.copy():
            if added_id == removed_id:
                added_ids.remove(added_id)
                removed_ids.remove(removed_id)
                updated_ids.append(added_id)

    # Get the mods names from the Modrinth API via get_mod_name function, ignore None responses
    added_mods, removed_mods, updated_mods = [], [], []
    async def main():

        if config['check']['added_mods']:
            added_mods.extend(filter(None, await asyncio.gather(*[get_mod_name(mod_id) for mod_id in added_ids])))

        if config['check']['removed_mods']:
            removed_mods.extend(filter(None, await asyncio.gather(*[get_mod_name(mod_id) for mod_id in removed_ids])))

        if config['check']['updated_mods']:
            updated_mods.extend(filter(None, await asyncio.gather(*[get_mod_name(mod_id) for mod_id in updated_ids])))

    asyncio.run(main())

    # Add loader and mc version changes
    if old_loader != new_loader and config['check']['loader']:
        added_mods.append(f"{new_loader} (mod loader)")
        removed_mods.append(f"{old_loader} (mod loader)")

    if old_loader_version != new_loader_version and config['check']['loader']:
        updated_mods.append(f"{new_loader} (mod loader)")

    if old_mc_version != new_mc_version and config['check']['mc_version']:
        updated_mods.append(f"Minecraft version {new_mc_version}")
    
    return added_mods, removed_mods, updated_mods
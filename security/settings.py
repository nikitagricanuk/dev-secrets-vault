import json
from config import PATH_TO_SETTINGS_FILE
from fastapi.responses import JSONResponse
import os

async def get_settings_list():
    with open(PATH_TO_SETTINGS_FILE, 'r') as fd:
        settings = json.load(fd) 

    settings_list = []

    # Iterate over the settings array to collect all settings
    for section in settings["settings"]:
        for category, items in section.items():  # Iterate over categories (e.g., 'auth', 'security')
            for item in items:  # Each item is a setting inside the category
                settings_list.extend(
                    {
                        "setting_key": f"{category}.{setting_key}",  # Format: "category.setting"
                        "value": setting_data["value"],
                        "comment": setting_data["comment"],
                    }
                    for setting_key, setting_data in item.items()
                )
    return JSONResponse(content=settings_list)

async def get_setting(setting_key: str):
    """
    Get a setting from the settings if it exists
    
    Args:
        setting_key (str): The name of the setting in the following format: category.setting
        
    Returns:
        int: A status code indicating if any error occurred:
            - 0: Setting does not exist.
        dict: All good, just return the setting:
            - data: The setting key and value.
    """
    with open(PATH_TO_SETTINGS_FILE, 'r') as fd:
        settings = json.load(fd)

    category = setting_key.split('.')[0]
    setting = setting_key.split('.')[1]

    # Iterate over the settings array to collect all settings
    return_data = None
    for section in settings["settings"]:
        if category in section: # Iterate over categories (e.g., 'auth', 'security')
            for item in section[category]:
                if setting in item: # Iterate over category items
                    return item[setting]["value"]
    return 0

async def set_setting(key: str, value: str):
    if await validate_setting(key, value):
        with open(PATH_TO_SETTINGS_FILE, 'r') as fd:
            settings = json.load(fd)

        category = key.split('.')[0]
        setting = key.split('.')[1]

        # Iterate over the settings array to collect all settings
        return_data = None
        for section in settings["settings"]:
            if category in section: # Iterate over categories (e.g., 'auth', 'security')
                for item in section[category]:
                    if setting in item: # Iterate over category items
                        item[setting]["value"] = value
                        break
        
        with open(PATH_TO_SETTINGS_FILE, 'w') as fd:
            json.dump(settings, fd, indent=2)

        return_data =  {"setting_key": key, 
                        "value": value
                        }

        return JSONResponse(content=return_data)
    
    return_data = {"detail": "The provided setting value is invalid."}
    return JSONResponse(content=return_data)

async def validate_setting(key: str, value: str):
    with open(PATH_TO_SETTINGS_FILE, 'r') as fd:
        settings = json.load(fd)
    try:
        category = key.split('.')[0]
        setting = key.split('.')[1]
    except IndexError:
        return False

    for section in settings["settings"]:
        if category in section: # Iterate over categories (e.g., 'auth', 'security')
            for item in section[category]:
                if setting in item: # Iterate over category items
                    return True
                
    return False
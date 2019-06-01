'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from singularity.logger import bot
from singularity.utils import (
    get_installdir,
    read_json
)

import sys
import os
import re



def get_custom_level(regexp=None,description=None,skip_files=None,include_files=None):
    '''get_custom_level will generate a custom level for the user, 
    based on a regular expression. If used outside the context of tarsum, the user
    can generate their own named and described filters.
    :param regexp: must be defined, the file filter regular expression
    :param description: optional description
    '''
    if regexp == None:
        regexp = "."
    if description is None:
        description = "This is a custom filter generated by the user."
    
    custom = {"description":description,
              "regexp":regexp}

    # Include extra files?
    if include_files is not None:
        if not isinstance(include_files,set):
            include_files = set(include_files)
        custom['include_files'] = include_files

    # Skip files?
    if skip_files is not None:
        if not isinstance(skip_files,set):
            skip_files = set(skip_files)
        custom['skip_files'] = skip_files

    return custom


def get_level(level, version=None, include_files=None, skip_files=None):
    '''get_level returns a single level, with option to customize files
    added and skipped.
    '''

    levels = get_levels(version=version)
    level_names = list(levels.keys())

    if level.upper() in level_names:
        level = levels[level]
    else:
        bot.warning("%s is not a valid level. Options are %s"  %(level.upper(),
                                                                "\n".join(levels)))
        return None

    # Add additional files to skip or remove, if defined
    if skip_files is not None:
        level = modify_level(level,'skip_files',skip_files)
    if include_files is not None:
        level = modify_level(level,'include_files',include_files)

    level = make_level_set(level)
    return level


def modify_level(level,field,values,append=True):
    '''modify level is intended to add / modify a content type.
    Default content type is list, meaning the entry is appended.
    If you set append to False, the content will be overwritten
    For any other content type, the entry is overwritten.
    '''
    field = field.lower()
    valid_fields = ['regexp','skip_files','include_files']
    if field not in valid_fields:
        bot.warning("%s is not a valid field, skipping. Choices are %s" %(field,",".join(valid_fields)))
        return level
    if append:
        if not isinstance(values,list):
            values = [values]
        if field in level:
            level[field] = level[field] + values
        else:
            level[field] = values
    else:
        level[field] = values

    level = make_level_set(level)

    return level       


def get_levels(version=None):
    '''get_levels returns a dictionary of levels (key) and values (dictionaries with
    descriptions and regular expressions for files) for the user. 
    :param version: the version of singularity to use (default is 2.2)
    :param include_files: files to add to the level, only relvant if
    '''
    valid_versions = ['2.3','2.2']

    if version is None:
        version = "2.3"  
    version = str(version)

    if version not in valid_versions:
        bot.error("Unsupported version %s, valid versions are %s" %(version,
                                                                    ",".join(valid_versions)))

    levels_file = os.path.abspath(os.path.join(get_installdir(),
                                                           'analysis',
                                                           'reproduce',
                                                           'data',
                                                           'reproduce_levels.json'))
    levels = read_json(levels_file)
    if version == "2.2":
        # Labels not added until 2.3
        del levels['LABELS']

    levels = make_levels_set(levels)

    return levels


def make_levels_set(levels):
    '''make set efficient will convert all lists of items
    in levels to a set to speed up operations'''
    for level_key,level_filters in levels.items():
        levels[level_key] = make_level_set(level_filters)
    return levels
    


def make_level_set(level):
    '''make level set will convert one level into
    a set'''
    new_level = dict()
    for key,value in level.items():
        if isinstance(value,list):
            new_level[key] = set(value)
        else:
            new_level[key] = value
    return new_level 

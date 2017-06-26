'''
The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from singularity.utils import (
    mkdir_p,
    write_json
)
from glob import glob
import sys
import os


def generate_registry(base,
                      uri,
                      name,
                      storage=None):

    '''initalize a registry, meaning generating the root folder with
    subfolders for containers and recipes, along with the config file
    at the root
    '''
    if storage is None:
        storage = "%s/storage" %(base) 

    container_base = "%s/containers" %storage

    if os.path.exists(base) or os.path.exists(storage):
        bot.error("%s or %s already exists, will not overwrite." %(base,storage))
        sys.exit(1)

    # Make directories for containers, builder, recipes
    mkdir_p(container_base)
    for subfolder in ['builder','recipes']:
        os.mkdir('%s/%s' %(base,subfolder))
    
    # /[base]/builder/templates
    os.mkdir("%s/builder/templates")

    bot.info("BASE: %s" %base)
    bot.info(" --> RECIPES: %s/recipes" %base)
    bot.info(" --> BUILDER: %s/builder\n" %base)
    bot.info("STORAGE: %s" %storage)
    bot.info(" --> CONTAINERS: %s/containers" %storage)

    config_file = generate_config(base=base,
                                  uri=uri,
                                  name=name,
                                  storage=storage)

    bot.debug("Adding CI templates to recipes folder.")
    copied = get_template(templates=['ci/.travis.yml'],
                          output_folder="%s/recipes" %base)

    return config_file


def generate_config(base,
                    uri,
                    name,
                    storage,
                    filename=None):

    '''generate config will write a config file at the registry
    base. The default filename is .shub
    '''

    if filename is None:
        filename = 'config.json'
    filename = os.path.basename(filename)

    config = { 
                "REGISTRY_BASE":  base,
                "STORAGE_BASE": storage,
                "REGISTRY_URI": uri,
                "REGISTRY_NAME": name 
             }

    config_file = "%s/%s" %(base,filename)
    bot.debug("Generating config file %s" %config_file)
    write_json(config,config_file)
    return config_file

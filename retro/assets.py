#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import glob
import os.path

import retro.backend

_IMAGE_ASSET_ = 'image'
_UNKNOWN_TYPE_ = 'unknown'

class AssetNotFound(Exception):
    def __init__(self, resource='unknown'):
        self.__rname = resource
    def __str__(self):
        return 'Cannot load asset: %s' % self.__rname


class UnrecognizedAsset(Exception):
    def __init__(self, resource='unknown'):
        self.__rname = resource
    def __str__(self):
        return 'Unknown or unsupported asset format: %s' % self.__rname

    
def _file_type_(filename):
    '''
    Yeah... quick'n'dirty
    '''
    filename = filename.upper()
    if filename.endswith('PNG') or filename.endswith('JPG'):
        return _IMAGE_ASSET_
    return _UNKNOWN_TYPE_


def load(resources_fname, is_required=True):
    '''
    Load resources: load('$ASSET_FOLDER\animation_frame*.png')
    '''
    assert(isinstance(resources_fname, str))

    # Search paths (yep... for now, hard coded  :'(
    #
    resources = set(glob.glob(os.path.join('assets', resources_fname)))
    resources.update(set(glob.glob(os.path.join('/usr/local/share/retro-assets', resources_fname))))
    resources = list(resources)
    resources.sort()

    # Check exists
    valid_resources = []
    for resource in resources:
        if (not os.path.exists(resource) and is_required):
            raise AssetNotFound(resource)
        valid_resources.append(resource)
    resources = valid_resources

    # Quick'n'dirty heuristic:
    if len(resources) == 1:
        if _file_type_(resources[0]) == _IMAGE_ASSET_:
            return retro.backend.load_image(resources[0])
        if is_required:
            raise UnrecognizedAsset(resources[0])
        # return None

    # More than one resource:
    # Only one type at a time!
    valid_type = _file_type_(resources[0])
    if any(
        [(_file_type_(resource) != valid_type)
         for resource in resources]) and is_required:
        raise UnrecognizedAsset('mix of file types')

    if valid_type == _IMAGE_ASSET_:
        return retro.backend.load_animation(resources)
    if is_required:
        raise UnrecognizedAsset('several files of type: %s' % valid_type)
    # return None

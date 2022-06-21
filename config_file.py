# coding: utf-8

'''
Opens a yaml file and returns a dictionary containing the configuration.
Or save the dictionary data to yaml file.
'''
import os
import yaml

def yaml_to_dict(datapath:str):
    '''
    Open and  Converts a yaml configuration file to a dictionary.
    :param datapath(str): The path to the yaml file.
    :return: A dictionary.
    '''    
    with open(datapath, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf

def dict_to_yaml(dict:dict, datapath:str):
    
    '''Converts a dictionary to a yaml file.
    :param dict: The dictionary to be converted.
    :param datapath: The path where the yaml file will be stored.
    '''
    with open(datapath, "w") as stream:
        try:
            yaml.dump(dict, stream)
        except yaml.YAMLError as exc:
            print(exc)

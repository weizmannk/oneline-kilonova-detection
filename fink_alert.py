# coding: utf-8
import os
import yaml


def yaml_to_dict(datapath:str):
    
    """Open a config file and return a dictionary containing the configuration.     
    Args:
        datapath (str): path to the yaml file
    """
    with open(datapath, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf

def dict_to_yaml(dict:dict, datapath:str):
    
    """Write a dictionary to a yaml file 
    Args:
        dict (dict):dictionary to write to the yaml file 
        datapath (str): path to the yaml file
    """
    with open(datapath, "w") as stream:
        try:
            yaml.dump(dict, stream)
        except yaml.YAMLError as exc:
            print(exc)
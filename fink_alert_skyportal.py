# coding: utf-8
import os
from fink_client.consumer import AlertConsumer
from astropy.time import Time
from fink_filters.classification import extract_fink_classification_from_pdf
import skyportal_api as skyportal_api
import config_file 
from switchers import fid_to_filter_ztf
import pandas as pd

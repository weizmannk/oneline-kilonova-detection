import os
import requests
import pandas as pd

# =============================================================================
# api_key for Fink call and recharge the local data 
# =============================================================================
api_key = 'http://134.158.75.151:24000/api/v1/objects'

# =============================================================================
# output data directory 
# =============================================================================
datapath = os.path.abspath(".") + "/" + os.path.join("output")
if not os.path.isdir(datapath):
    os.makedirs(datapath)


def data_upload(api_key,  ztf_id):
    """[Get data for ZTF fields and Fink science module outputs.]

    :param api_key: API key for Fink call 
    :type API_key: [str ]
    :param ztf_id:  each ZTF21..... folder name in the KN-Catcher-ReadyforO4
    :type ztf_id: [ str ]
    :return: Get only a subset data of the fields provide by each  Grandma KN-Catcher, ZTF_ID
    :rtype: [ json format ]
    """
    r = requests.post(api_key,
                json={
                    'objectId': ztf_id, 
                    'output-format': 'json'
                    }
                    )
    return r
    
def read_json(api_key, ztf_id):
    """[reading json file]
    
    :return: Format output in a DataFrame
    :rtype: [pandas.core.frame.DataFrame]
    """
    return pd.read_json(data_upload(api_key, ztf_id).content)

def data_frame(pdf):
    """[DataFrame Extracting ]

    :param pdf: json file read by pandas in read_json () function 
    :type pdf: [ DataFrame]
    :return:  extracting the time and magnitude data of the observations
    :rtype: [tuple]
    """
    firstdate_ztf = pdf['i:jd'].values[-1]
    times_ztf = pdf['i:jd']       #       - firstdate_ztf
    mags_ztf = pdf['i:magpsf']
    magerrs_ztf = pdf['i:sigmapsf']
    limmag_ztf = pdf['i:magnr']
    
    return firstdate_ztf, times_ztf, mags_ztf, magerrs_ztf, limmag_ztf

def ztf_labeling_filter(pdf):
    """[Labels of ZTF filters]

    :param pdf: json file read by pandas in read_json () function
    :type pdf: [DataFrame]
    :return:the data of g and r filters
    :rtype: [list]
    """
    
    filtdic = {1: 'g', 2: 'r'}
    ztf_filts = []
    for filt in pdf['i:fid']:
        ztf_filts.append(filtdic[filt])

    return ztf_filts


pdf = read_json(api_key, ztf_id)

ZTF_ID = [f.name for f in os.scandir(datapath) if f.is_dir() and len(f.name)==12]

# ================================================================================
# read json file
# ================================================================================
#for ztf_id  in ZTF_ID:
 #   print("Read the file",  ztf_id)


# read update json file data from ZTF 
pdf = read_json(api_key, ztf_id)
    
# ===============================================================================
# This line discards the bad folders that have been loaded  in ZTF_ID
# ===============================================================================
if pdf.shape !=(0, 0):
    
    # ===========================================================================
    # DataFrame from ZTF pipeline
    # ===========================================================================
    firstdate_ztf, times_ztf, mags_ztf, magerrs_ztf, limmag_ztf = data_frame(pdf)

    # ===========================================================================
    # Labels of ZTF filters
    # ===========================================================================
    ztf_filts = ztf_labeling_filter(pdf)


    #create NA for lack of usernames
    ztf_user =  len(ztf_filts)*["N/A"]
    ZTF = len(ztf_filts)*["ztf"]
    
    # ==========================================================================
    # Selection of data provide by users and ZTF online
    # ==========================================================================
    d = {'jd': times_ztf.values.tolist(),
        'mag': mags_ztf.values.tolist(),
        'mag_unc': magerrs_ztf.values.tolist(),
        'filters': ztf_filts,
        'limmag': limmag_ztf.values.tolist(), 
        'username' : ztf_user,
        'instrument' : ZTF
        }

    # =========================================================================
    # Make a custom pandas dataframe 
    # Read data and save it in csv
    # =========================================================================
    df = pd.DataFrame(data=d) 

    # =========================================================================
    # Create a csv file and save it under the ztf_id name
    # =========================================================================
    df.to_csv(datapath + '/'+ ztf_id + '.csv')

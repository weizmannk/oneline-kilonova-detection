from fink_client.consumer import AlertConsumer
from fink_client.configuration import load_credentials

import time
import tabulate

def poll_single_alert(myconfig, topics) -> None:
    """ Connect to and poll fink servers once.

    Parameters
    ----------
    myconfig: dic
    	python dictionnary containing credentials
    topics: list of str
    	List of string with topic names
    """
    maxtimeout = 5

    # Instantiate a consumer
    consumer = AlertConsumer(topics, myconfig)

    # Poll the servers
    topic, alert, key = consumer.poll(maxtimeout)

    # Analyse output - we just print some values for example
    if topic is not None:
        utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        table = [
            [
		 		alert['timestamp'],
		 		utc,
		 		topic,
		 		alert['objectId'],
		 		alert['cdsxmatch'],
		 		alert['candidate']['magpsf']
		 	],
		]
        headers = [
			'Emitted at (UTC)',
			'Received at (UTC)',
			'Topic',
			'objectId',
			'Simbad',
			'Magnitude'
		]
        print(tabulate(table, headers, tablefmt="pretty"))
    else:
        print(
            'No alerts received in the last {} seconds'.format(
                maxtimeout
            )
        )

    # Close the connection to the servers
    consumer.close()


if __name__ == "__main__":
    """ Poll the servers only once at a time """

    # to fill
    myconfig = {
            'username': 'weizmann',
            'bootstrap.servers': '134.158.74.95:24499',
            'group_id': 'weizmann_fink'
        }

    topics = [ 'fink_kn_candidates_ztf', 'fink_early_kn_candidates_ztf']

    poll_single_alert(myconfig, topics)
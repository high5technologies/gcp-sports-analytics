import base64
import json
import os
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import urllib.request
from google.cloud import logging

#def nba_all(request):
def nba_all(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    
    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)
    
    ##########################################################################
    # Input Data Check
    ##########################################################################

    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
    else: 
        message_data = []
    #date_string = message_data['date_string']
    #date_formatted = message_data['date_formatted']

    
    try:
        #request_json = request.get_json()
        #if request_json and 'StartDate' not in request_json:  
        #    startDate = datetime.now().strftime("%Y-%m-%d")
        #else:
        #    startDate = datetime.strptime(request_json['StartDate'], '%Y-%m-%d').date()
        #if request_json and 'EndDate' not in request_json:  
        #    endDate = datetime.now().strftime("%Y-%m-%d") 
        #else:
        #    endDate = datetime.strptime(request_json['EndDate'], '%Y-%m-%d').date()
        if 'start_date' not in message_data:  
            startDate = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            startDate = datetime.strptime(message_data['start_date'], '%Y-%m-%d').date()
        if 'end_date' not in message_data:  
            endDate = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            endDate = datetime.strptime(message_data['end_date'], '%Y-%m-%d').date()
    except:
        raise ValueError("Start & End dates must be in YYYY-MM-DD format")
    
    # Distinct list of Months between start and end date
    delta = endDate - startDate       # as timedelta
    
    if delta.days < 0:
        raise ValueError("StartDate can't be offer Begin Date")
    
    current_date = datetime.now()
    if current_date.month > 9:
        current_season = current_date.year + 1
    else:
        current_season = current_date.year 
    
    has_538_prediction_hist = False
    has_538_prediction_current = False
    has_538_raptor_hist = False
    has_538_raptor_current = False
    hist_begin_season = 0
    hist_end_season = 0
    current_begin_season = 0
    current_end_season = 0
    hist_begin_date = 0
    hist_end_date = 0
    current_begin_date = 0
    current_end_date = 0

    ##########################################################################
    # Get games/urls to scrape
    ##########################################################################
    
    try:

        for i in range(delta.days + 1):
            d = {}
            day = startDate + timedelta(days=i)
            d['date_string'] = day.strftime("%Y%m%d")
            d['date_formatted'] = day.strftime("%Y-%m-%d")
            d['date_string_month'] = str(day.month)
            d['date_string_day'] = str(day.day)
            d['date_string_year'] = str(day.year)
            season = day.year + 1 if day.month > 9 else day.year
            d['season_nbastats'] = str(season) + '-' + str(season+1)[-2:]
            data_string = json.dumps(d)  

            # NBACOM
            topic_id = "nba_nbacom_dates_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))   

            # NBASTATS - switching to the NBA STATS API 
            #topic_id = "nba_nbastats_dates_to_scrape"
            #topic_path = publisher.topic_path(project_id, topic_id)
            #future = publisher.publish(topic_path, data_string.encode("utf-8"))  

            # SBR
            topic_id = "nba_sbr_dates_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))        
            
            # ESPN - commenting this out for now - ESPN changed their logic and this no longer works
            topic_id = "nba_espn_dates_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            #future = publisher.publish(topic_path, data_string.encode("utf-8"))   

            # Rotoguru - commenting out - rotoguru is no longer supporting posting odds
            #topic_id = "nba_rotoguru_dates_to_scrape"
            #topic_path = publisher.topic_path(project_id, topic_id)
            #future = publisher.publish(topic_path, data_string.encode("utf-8"))   

            #######################
            # 538 Dates
            
            # Season of current date
            if day.month > 9:
                loop_season = day.year + 1
            else:
                loop_season = day.year

            if loop_season == current_season:
                has_538_prediction_current = True
                has_538_raptor_current = True
                if current_begin_season == 0:
                    current_begin_season = loop_season
                if current_begin_date == 0:
                    current_begin_date = day.strftime("%Y-%m-%d")
                current_end_season = loop_season
                current_end_date = day.strftime("%Y-%m-%d")
            else:
                has_538_prediction_hist = True
                has_538_raptor_hist = True
                if hist_begin_season == 0:
                    hist_begin_season = loop_season
                if hist_begin_date == 0:
                    hist_begin_date = day.strftime("%Y-%m-%d")
                hist_end_season = loop_season
                hist_end_date = day.strftime("%Y-%m-%d")



        # 538 Player Raptor (not ready)
        if has_538_raptor_hist:
            d = {}
            d['beginSeason'] = hist_begin_season
            d['endSeason'] = hist_end_season
            d['historic_url'] = True

            data_string = json.dumps(d)  
            topic_id = "nba_538_playerraptor_seasons_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))  

        if has_538_raptor_current:
            d = {}
            d['beginSeason'] = current_begin_season
            d['endSeason'] = current_end_season
            d['historic_url'] = False

            data_string = json.dumps(d)  
            topic_id = "nba_538_playerraptor_seasons_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))  

        # 538 Predictions (not ready)
        if has_538_prediction_hist: 
            d = {}
            d['startDate'] = hist_begin_date
            d['endDate'] = hist_end_date
            d['historic_url'] = True

            data_string = json.dumps(d)  
            topic_id = "nba_538_predictions_range_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        if has_538_prediction_current:
            d = {}
            d['startDate'] = current_begin_date
            d['endDate'] = current_end_date
            d['historic_url'] = False

            data_string = json.dumps(d)  
            topic_id = "nba_538_predictions_range_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))   
            


        # BR (Future???)

        return f'Source dates queued successfully (NBACOM, SBR, ESPN, 538)'

    except Exception as e:
        err = {}
        err['error_key'] = str(uuid.uuid4())
        err['error_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        err['function'] = os.environ.get('FUNCTION_NAME')
        err['data_identifier'] = "none"
        err['trace_back'] = str(traceback.format_exc())
        err['message'] = str(e)
        #err['data'] = data if data is not None else ""
        print(err)
        
        topic_id_error = "error_log_topic"
        data_string_error = json.dumps(err) 
        topic_path_error = publisher.topic_path(project_id, topic_id_error)
        future = publisher.publish(topic_path_error, data_string_error.encode("utf-8"))


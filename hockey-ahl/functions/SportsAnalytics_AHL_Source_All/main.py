import base64
import json
import os
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import calendar
import urllib.request

def ahl_all(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    fs = firestore.Client()
    
    ##########################################################################
    # Input Data Check
    ##########################################################################

    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
    else: 
        message_data = []
    
    try:
        if 'start_date' not in message_data:  
            startDate = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            startDate = datetime.strptime(message_data['start_date'], '%Y-%m-%d').date()
        if 'end_date' not in message_data:  
            endDate = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            endDate = datetime.strptime(message_data['end_date'], '%Y-%m-%d').date()
        if ('Rerun' in message_data or 'RERUN' in message_data or 'rerun' in message_data):
            rerun = True
        else:
            rerun = False
    except:
        raise ValueError("Start & End dates must be in YYYY-MM-DD format")
    
    # Distinct list of Months between start and end date
    delta = endDate - startDate       # as timedelta
    
    if delta.days < 0:
        raise ValueError("StartDate can't be offer Begin Date")
    
    #current_date = datetime.now()
    #if current_date.month > 9:
    #    current_season = current_date.year + 1
    #else:
    #    current_season = current_date.year 

    try:
        yearmonths = []
        for i in range(delta.days + 1):
            #d = {}
            #day = startDate + timedelta(days=i)
            #d['date_string'] = day.strftime("%Y%m%d")
            #d['date_formatted'] = day.strftime("%Y-%m-%d")
            #d['date_string_month'] = str(day.month)
            #d['date_string_day'] = str(day.day)
            #d['date_string_year'] = str(day.year)
            
            r = {}
            day = startDate + timedelta(days=i)
            #dt = day.strftime("%Y-%m-%d")
            r['monthname'] = day.strftime('%B').lower()
            r['month_number'] = day.month
            r['year'] = day.year
            if day.month > 9:
                r['season'] = day.year + 1
            else:
                r['season'] = day.year
            r['rerun'] = rerun

            first_day_of_month = day.replace(day=1)
            last_day_number = calendar.monthrange(day.year, day.month)[1]
            last_day_of_month = datetime(day.year, day.month, last_day_number).date()
            month_start_date = startDate if startDate > first_day_of_month else first_day_of_month
            month_end_date = endDate if endDate < last_day_of_month else last_day_of_month
            r['start_date'] = month_start_date.strftime("%Y-%m-%d")
            r['end_date'] = month_end_date.strftime("%Y-%m-%d")

            if r not in yearmonths: 
                yearmonths.append(r)

        for m in yearmonths:          
            data_string = json.dumps(m)  

            # AHL.COM API - HockeyTech
            topic_id = "ahl_ahlcom_months_to_scrape"
            topic_path = publisher.topic_path(project_id, topic_id)
            future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        for m in yearmonths:
            season = m['season']
            docs = fs.collection(u'reference').document(u'AHL').collection('ahl_hockeytech_seasons').where(u'season',u'==',str(season)).stream()
            
            season_indexes = []
            for doc in docs:
                d = doc.to_dict()
                
                event_flag = d['event_flag']
                season_start_date = datetime.strptime(d['start_date'], '%Y-%m-%d').date()
                season_end_date = datetime.strptime(d['end_date'], '%Y-%m-%d').date()
                season_index = d['hockeytech_key']

                si = {}
                si['season_index'] = season_index
                si['season_start_date'] = season_start_date
                si['season_end_date'] = season_end_date

                ssd = d['start_date'] #.strftime("%Y-%m-%d")
                sed = d['end_date'] #.strftime("%Y-%m-%d")
                print({"season_start_date":ssd,"season_end_date":sed,"season_index":season_index})
                if not event_flag:
                    # search for first date of season in date range given
                    # Only need to load roster once per year
                    print('check started')
                    for i in range(delta.days + 1):
                        dt = startDate + timedelta(days=i) 
                        print(dt.strftime("%Y-%m-%d"))
                        if dt == season_start_date and season_index not in season_indexes:
                            print('found')
                            season_indexes.append(si)

            # AHL.COM API - HockeyTech
            for si in season_indexes:
                data_string = json.dumps(si) 
                topic_id = "ahl_ahlcom_roster_seasons_to_scrape"
                topic_path = publisher.topic_path(project_id, topic_id)
                future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        return f'Source dates queued successfully (AHLCOM)'

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


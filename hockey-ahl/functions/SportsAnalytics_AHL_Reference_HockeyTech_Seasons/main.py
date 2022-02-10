from google.cloud import firestore

def load_firestore_reference_ahl_hockeytech_seasons(request):
    # Currently need to run this manually when first deploying to new env
    # To-do - figure out a way to have terraform execute this function
    db = firestore.Client()

    # Can I convert this to a JSON file?
    # Run this function on deployment
    # NEED DATES HERE SO GET GET SEASON_TYPE FROM RANGE
    # https://theahl.com/stats/roster/-1/57?league=4
    json_data = [
         {"season":"2005","season_type":"reg","hockeytech_key":"46"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2005","season_type":"allstar","hockeytech_key":"17"     ,"event_flag":true,"start_date":"2005-02-14","end_date":"2005-02-14"}
        ,{"season":"2005","season_type":"playoff","hockeytech_key":"69"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2006","season_type":"reg","hockeytech_key":"1"          ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2006","season_type":"allstar","hockeytech_key":"2"      ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2006","season_type":"playoff","hockeytech_key":"7"      ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2007","season_type":"reg","hockeytech_key":"8"          ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2007","season_type":"allstar","hockeytech_key":"9"      ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2007","season_type":"playoff","hockeytech_key":"10"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2008","season_type":"reg","hockeytech_key":"12"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2008","season_type":"allstar","hockeytech_key":"14"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2008","season_type":"playoff","hockeytech_key":"15"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2009","season_type":"reg","hockeytech_key":"16"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2009","season_type":"allstar","hockeytech_key":"28"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2009","season_type":"playoff","hockeytech_key":"29"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2010","season_type":"reg","hockeytech_key":"30"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2010","season_type":"allstar","hockeytech_key":"31"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2010","season_type":"playoff","hockeytech_key":"33"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2011","season_type":"reg","hockeytech_key":"34"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2011","season_type":"allstar","hockeytech_key":"35"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2011","season_type":"playoff","hockeytech_key":"36"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2012","season_type":"reg","hockeytech_key":"37"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2012","season_type":"allstar","hockeytech_key":"38"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2012","season_type":"playoff","hockeytech_key":"39"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2013","season_type":"reg","hockeytech_key":"40"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2013","season_type":"allstar","hockeytech_key":"41"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2013","season_type":"playoff","hockeytech_key":"42"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2014","season_type":"reg","hockeytech_key":"43"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2014","season_type":"allstar","hockeytech_key":"44"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2014","season_type":"playoff","hockeytech_key":"47"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2015","season_type":"reg","hockeytech_key":"48"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2015","season_type":"allstar","hockeytech_key":"49"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2015","season_type":"playoff","hockeytech_key":"50"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2016","season_type":"reg","hockeytech_key":"51"         ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2016","season_type":"allstar","hockeytech_key":"52"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2016","season_type":"playoff","hockeytech_key":"53"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2017","season_type":"reg","hockeytech_key":"54"         ,"event_flag":false,"start_date":"2016-10-14","end_date":"2017-04-15"}
        #,{"season":"2017","season_type":"allstar","hockeytech_key":"55"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2017","season_type":"playoff","hockeytech_key":"56"     ,"event_flag":false,"start_date":"2017-04-20","end_date":"2017-06-13"}
        ,{"season":"2018","season_type":"reg","hockeytech_key":"57"         ,"event_flag":false,"start_date":"2017-10-06","end_date":"2018-04-15"}
        #,{"season":"2018","season_type":"allstar","hockeytech_key":"59"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2018","season_type":"playoff","hockeytech_key":"60"     ,"event_flag":false,"start_date":"2018-04-19","end_date":"2018-06-14"}
        ,{"season":"2019","season_type":"reg","hockeytech_key":"61"         ,"event_flag":false,"start_date":"2018-10-05","end_date":"2019-04-15"}
        #,{"season":"2019","season_type":"allstar","hockeytech_key":"63"     ,"event_flag":true,"start_date":"","end_date":""}
        ,{"season":"2019","season_type":"playoff","hockeytech_key":"64"     ,"event_flag":false,"start_date":"2019-04-17","end_date":"2019-06-08"}
        ,{"season":"2020","season_type":"reg","hockeytech_key":"65"         ,"event_flag":false,"start_date":"2019-10-04","end_date":"2020-03-12"}
        ,{"season":"2020","season_type":"allstar","hockeytech_key":"67"     ,"event_flag":true,"start_date":"2020-01-26","end_date":"2020-01-26"}
        ,{"season":"2021","season_type":"reg","hockeytech_key":"68"         ,"event_flag":false,"start_date":"2021-02-05","end_date":"2021-05-20"}
        #,{"season":"2021","season_type":"playoff","hockeytech_key":"72"     ,"event_flag":false,"start_date":"","end_date":""}
        ,{"season":"2022","season_type":"reg","hockeytech_key":"73"         ,"event_flag":false,"start_date":"2021-10-15","end_date":"2022-04-30"}
        #,{"season":"2022","season_type":"playoff","hockeytech_key":"??"         ,"event_flag":false,"start_date":"2022-05-01","end_date":"2022-07-01"}
    ]
    for obj in json_data:
        doc_ref_key = obj['season'] + '_' + obj['season_type']
        doc_ref = db.collection(u'reference').document(u'AHL').collection('ahl_hockeytech_seasons').document(doc_ref_key)
        doc_ref.set(obj)
        
    return f'AHL Reference data added to firestore'

    
#,{"season":"2010","season_type":"reg","hockeytech_key":"30"}
#,{"season":"2011","season_type":"reg","hockeytech_key":"34"}
#,{"season":"2012","season_type":"reg","hockeytech_key":"37"}
#,{"season":"2013","season_type":"reg","hockeytech_key":"40"}
#,{"season":"2014","season_type":"reg","hockeytech_key":"43"}
#,{"season":"2015","season_type":"reg","hockeytech_key":"48"}
#,{"season":"2016","season_type":"reg","hockeytech_key":"51"}
#,{"season":"2017","season_type":"reg","hockeytech_key":"54"}
#,{"season":"2018","season_type":"reg","hockeytech_key":"57"}
#,{"season":"2019","season_type":"reg","hockeytech_key":"61"}
#,{"season":"2020","season_type":"reg","hockeytech_key":"65"}
#,{"season":"2021","season_type":"reg","hockeytech_key":"??????????????????????????????????????"}
#,{"season":"2022","season_type":"reg","hockeytech_key":"??????????????????????????????????????"}


import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
from bs4 import BeautifulSoup, Comment
import urllib.request
from google.cloud import logging
import time

def nba_nbacom_worker_individual_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)

    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        game_date = message_data['game_date']
        game_url_id = message_data['url_id']
        
        url = 'https://www.nba.com/game/' + game_url_id + '/play-by-play'
        #print(url)

        i = 1
        while i <= 3: # max 3 attempts
            logger.log_text("attmpt:"+str(i) + "; url:" + url + ";")
            r = requests.get(url)
            #print(r.content[0:3000])
            soup = BeautifulSoup(r.content, 'html.parser')
            script = soup.find("script", {"id": "__NEXT_DATA__"})
            if script is not None:
                break
            else:
                time.sleep(1) # if data not found, wait 1 second and try again
            i += 1

        data = json.loads(script.string)

        g = {}

        g['game_key'] = data['props']['pageProps']['game']['gameId']
        g['game_id'] = data['props']['pageProps']['game']['gameId']
        g['url_id'] = data['props']['pageProps']['id']
        g['season'] = data['props']['pageProps']['analyticsObject']['season']
        g['season_type'] = data['props']['pageProps']['analyticsObject']['seasonType']
        game_date_srting = data['props']['pageProps']['game']['gameCode'].split('/')[0]
        g['game_date'] = game_date_srting[0:4] + '-' + game_date_srting[4:6] + '-' + game_date_srting[6:8]
        g['game_code'] = data['props']['pageProps']['game']['gameCode']
        g['game_status'] = data['props']['pageProps']['game']['gameStatus']
        g['game_status_text'] = data['props']['pageProps']['game']['gameStatusText']
        g['period'] = data['props']['pageProps']['game']['period']
        g['game_clock'] = data['props']['pageProps']['game']['gameClock']
        g['game_time_utc'] = data['props']['pageProps']['game']['gameTimeUTC']
        g['game_et'] = data['props']['pageProps']['game']['gameEt']
        g['away_team_id'] = data['props']['pageProps']['game']['awayTeamId']
        g['home_team_id'] = data['props']['pageProps']['game']['homeTeamId']
        g['duration'] = data['props']['pageProps']['game']['duration']
        g['attendance'] = data['props']['pageProps']['game']['attendance']
        g['sellout'] = data['props']['pageProps']['game']['sellout']
        g['series_game_number'] = data['props']['pageProps']['game']['seriesGameNumber']
        g['series_text'] = data['props']['pageProps']['game']['seriesText']
        g['if_necessary'] = str(data['props']['pageProps']['game']['ifNecessary'])
        g['arena_id'] = data['props']['pageProps']['game']['arena']['arenaId']
        g['arena_name'] = data['props']['pageProps']['game']['arena']['arenaName']
        g['arena_city'] = data['props']['pageProps']['game']['arena']['arenaCity']
        g['arena_state'] = data['props']['pageProps']['game']['arena']['arenaState']
        g['arena_country'] = data['props']['pageProps']['game']['arena']['arenaCountry']
        g['arena_timezone'] = data['props']['pageProps']['game']['arena']['arenaTimezone']
        g['arena_street_address'] = data['props']['pageProps']['game']['arena']['arenaStreetAddress']
        g['arena_postal_code'] = data['props']['pageProps']['game']['arena']['arenaPostalCode']

        if len(data['props']['pageProps']['game']['broadcasters']['nationalBroadcasters']) > 0:
            g['national_broadcaster_id'] = data['props']['pageProps']['game']['broadcasters']['nationalBroadcasters'][0]['broadcasterId']
            g['national_broadcast_display'] = data['props']['pageProps']['game']['broadcasters']['nationalBroadcasters'][0]['broadcastDisplay']
        else:
            g['national_broadcaster_id'] = None
            g['national_broadcast_display'] = None

        g['home_team_id'] = data['props']['pageProps']['game']['homeTeam']['teamId']
        g['home_team_name'] = data['props']['pageProps']['game']['homeTeam']['teamName']
        g['home_team_city'] = data['props']['pageProps']['game']['homeTeam']['teamCity']
        g['home_team_tricode'] = data['props']['pageProps']['game']['homeTeam']['teamTricode']
        g['home_team_slug'] = data['props']['pageProps']['game']['homeTeam']['teamSlug']
        g['home_team_wins'] = data['props']['pageProps']['game']['homeTeam']['teamWins']
        g['home_team_losses'] = data['props']['pageProps']['game']['homeTeam']['teamLosses']
        g['home_score'] = data['props']['pageProps']['game']['homeTeam']['score']
        g['home_seed'] = data['props']['pageProps']['game']['homeTeam']['seed']
        g['home_in_bonus'] = data['props']['pageProps']['game']['homeTeam']['inBonus']
        g['home_timeouts_remaining'] = data['props']['pageProps']['game']['homeTeam']['timeoutsRemaining']

        g['away_team_id'] = data['props']['pageProps']['game']['awayTeam']['teamId']
        g['away_team_name'] = data['props']['pageProps']['game']['awayTeam']['teamName']
        g['away_team_city'] = data['props']['pageProps']['game']['awayTeam']['teamCity']
        g['away_team_tricode'] = data['props']['pageProps']['game']['awayTeam']['teamTricode']
        g['away_team_slug'] = data['props']['pageProps']['game']['awayTeam']['teamSlug']
        g['away_team_wins'] = data['props']['pageProps']['game']['awayTeam']['teamWins']
        g['away_team_losses'] = data['props']['pageProps']['game']['awayTeam']['teamLosses']
        g['away_score'] = data['props']['pageProps']['game']['awayTeam']['score']
        g['away_seed'] = data['props']['pageProps']['game']['awayTeam']['seed']
        g['away_in_bonus'] = data['props']['pageProps']['game']['awayTeam']['inBonus']
        g['away_timeouts_remaining'] = data['props']['pageProps']['game']['awayTeam']['timeoutsRemaining']

        g['home_pregame_stats_points'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['points']
        g['home_pregame_stats_rebounds_total'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['reboundsTotal']
        g['home_pregame_stats_assists'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['assists']
        g['home_pregame_stats_steals'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['steals']
        g['home_pregame_stats_blocks'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['blocks']
        g['home_pregame_stats_turnovers'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['turnovers']
        g['home_pregame_stats_field_goals_percentage'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['fieldGoalsPercentage']
        g['home_pregame_stats_three_pointers_percentage'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['threePointersPercentage']
        g['home_pregame_stats_free_throws_percentage'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['freeThrowsPercentage']
        g['home_pregame_stats_points_in_the_paint'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['pointsInThePaint']
        g['home_pregame_stats_points_second_chance'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['pointsSecondChance']
        g['home_pregame_stats_points_fast_break'] = data['props']['pageProps']['game']['pregameCharts']['homeTeam']['statistics']['pointsFastBreak']

        g['away_pregame_stats_points'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['points']
        g['away_pregame_stats_rebounds_total'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['reboundsTotal']
        g['away_pregame_stats_assists'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['assists']
        g['away_pregame_stats_steals'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['steals']
        g['away_pregame_stats_blocks'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['blocks']
        g['away_pregame_stats_turnovers'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['turnovers']
        g['away_pregame_stats_field_goals_percentage'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['fieldGoalsPercentage']
        g['away_pregame_stats_three_pointers_percentage'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['threePointersPercentage']
        g['away_pregame_stats_free_throws_percentage'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['freeThrowsPercentage']
        g['away_pregame_stats_points_in_the_paint'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['pointsInThePaint']
        g['away_pregame_stats_points_second_chance'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['pointsSecondChance']
        g['away_pregame_stats_points_fast_break'] = data['props']['pageProps']['game']['pregameCharts']['awayTeam']['statistics']['pointsFastBreak']

        g['home_postgame_stats_points'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['points']
        g['home_postgame_stats_rebounds_total'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['reboundsTotal']
        g['home_postgame_stats_assists'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['assists']
        g['home_postgame_stats_steals'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['steals']
        g['home_postgame_stats_blocks'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['blocks']
        g['home_postgame_stats_turnovers'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['turnovers']
        g['home_postgame_stats_field_goals_percentage'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['fieldGoalsPercentage']
        g['home_postgame_stats_three_pointers_percentage'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['threePointersPercentage']
        g['home_postgame_stats_free_throws_percentage'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['freeThrowsPercentage']
        g['home_postgame_stats_points_in_the_paint'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['pointsInThePaint']
        g['home_postgame_stats_points_second_chance'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['pointsSecondChance']
        g['home_postgame_stats_points_fast_break'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['pointsFastBreak']
        g['home_postgame_stats_biggest_lead'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['biggestLead']
        g['home_postgame_stats_lead_changes'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['leadChanges']
        g['home_postgame_stats_times_tied'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['timesTied']
        g['home_postgame_stats_biggest_scoring_run'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['biggestScoringRun']
        g['home_postgame_stats_turnovers_team'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['turnoversTeam']
        g['home_postgame_stats_turnovers_total'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['turnoversTotal']
        g['home_postgame_stats_rebounds_team'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['reboundsTeam']
        g['home_postgame_stats_points_from_turnovers'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['pointsFromTurnovers']
        g['home_postgame_stats_bench_points'] = data['props']['pageProps']['game']['postgameCharts']['homeTeam']['statistics']['benchPoints']

        g['away_postgame_stats_points'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['points']
        g['away_postgame_stats_rebounds_total'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['reboundsTotal']
        g['away_postgame_stats_assists'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['assists']
        g['away_postgame_stats_steals'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['steals']
        g['away_postgame_stats_blocks'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['blocks']
        g['away_postgame_stats_turnovers'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['turnovers']
        g['away_postgame_stats_field_goals_percentage'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['fieldGoalsPercentage']
        g['away_postgame_stats_three_pointers_percentage'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['threePointersPercentage']
        g['away_postgame_stats_free_throws_percentage'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['freeThrowsPercentage']
        g['away_postgame_stats_points_in_the_paint'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['pointsInThePaint']
        g['away_postgame_stats_points_second_chance'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['pointsSecondChance']
        g['away_postgame_stats_points_fast_break'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['pointsFastBreak']
        g['away_postgame_stats_biggest_lead'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['biggestLead']
        g['away_postgame_stats_lead_changes'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['leadChanges']
        g['away_postgame_stats_times_tied'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['timesTied']
        g['away_postgame_stats_biggest_scoring_run'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['biggestScoringRun']
        g['away_postgame_stats_turnovers_team'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['turnoversTeam']
        g['away_postgame_stats_turnovers_total'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['turnoversTotal']
        g['away_postgame_stats_rebounds_team'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['reboundsTeam']
        g['away_postgame_stats_points_from_turnovers'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['pointsFromTurnovers']
        g['away_postgame_stats_bench_points'] = data['props']['pageProps']['game']['postgameCharts']['awayTeam']['statistics']['benchPoints']

        g['home_starters_minutes'] = data['props']['pageProps']['game']['homeTeam']['starters']['minutes']
        g['home_starters_field_goals_made'] = data['props']['pageProps']['game']['homeTeam']['starters']['fieldGoalsMade']
        g['home_starters_field_goals_attempted'] = data['props']['pageProps']['game']['homeTeam']['starters']['fieldGoalsAttempted']
        g['home_starters_field_goals_percentage'] = data['props']['pageProps']['game']['homeTeam']['starters']['fieldGoalsPercentage']
        g['home_starters_three_pointers_made'] = data['props']['pageProps']['game']['homeTeam']['starters']['threePointersMade']
        g['home_starters_three_pointers_attempted'] = data['props']['pageProps']['game']['homeTeam']['starters']['threePointersAttempted']
        g['home_starters_three_pointers_percentage'] = data['props']['pageProps']['game']['homeTeam']['starters']['threePointersPercentage']
        g['home_starters_free_throws_made'] = data['props']['pageProps']['game']['homeTeam']['starters']['freeThrowsMade']
        g['home_starters_free_throws_attempted'] = data['props']['pageProps']['game']['homeTeam']['starters']['freeThrowsAttempted']
        g['home_starters_free_throws_percentage'] = data['props']['pageProps']['game']['homeTeam']['starters']['freeThrowsPercentage']
        g['home_starters_rebounds_offensive'] = data['props']['pageProps']['game']['homeTeam']['starters']['reboundsOffensive']
        g['home_starters_rebounds_defensive'] = data['props']['pageProps']['game']['homeTeam']['starters']['reboundsDefensive']
        g['home_starters_rebounds_total'] = data['props']['pageProps']['game']['homeTeam']['starters']['reboundsTotal']
        g['home_starters_assists'] = data['props']['pageProps']['game']['homeTeam']['starters']['assists']
        g['home_starters_steals'] = data['props']['pageProps']['game']['homeTeam']['starters']['steals']
        g['home_starters_blocks'] = data['props']['pageProps']['game']['homeTeam']['starters']['blocks']
        g['home_starters_turnovers'] = data['props']['pageProps']['game']['homeTeam']['starters']['turnovers']
        g['home_starters_foulsPersonal'] = data['props']['pageProps']['game']['homeTeam']['starters']['foulsPersonal']
        g['home_starters_points'] = data['props']['pageProps']['game']['homeTeam']['starters']['points']

        g['away_starters_minutes'] = data['props']['pageProps']['game']['awayTeam']['starters']['minutes']
        g['away_starters_field_goals_made'] = data['props']['pageProps']['game']['awayTeam']['starters']['fieldGoalsMade']
        g['away_starters_field_goals_attempted'] = data['props']['pageProps']['game']['awayTeam']['starters']['fieldGoalsAttempted']
        g['away_starters_field_goals_percentage'] = data['props']['pageProps']['game']['awayTeam']['starters']['fieldGoalsPercentage']
        g['away_starters_three_pointers_made'] = data['props']['pageProps']['game']['awayTeam']['starters']['threePointersMade']
        g['away_starters_three_pointers_attempted'] = data['props']['pageProps']['game']['awayTeam']['starters']['threePointersAttempted']
        g['away_starters_three_pointers_percentage'] = data['props']['pageProps']['game']['awayTeam']['starters']['threePointersPercentage']
        g['away_starters_free_throws_made'] = data['props']['pageProps']['game']['awayTeam']['starters']['freeThrowsMade']
        g['away_starters_free_throws_attempted'] = data['props']['pageProps']['game']['awayTeam']['starters']['freeThrowsAttempted']
        g['away_starters_free_throws_percentage'] = data['props']['pageProps']['game']['awayTeam']['starters']['freeThrowsPercentage']
        g['away_starters_rebounds_offensive'] = data['props']['pageProps']['game']['awayTeam']['starters']['reboundsOffensive']
        g['away_starters_rebounds_defensive'] = data['props']['pageProps']['game']['awayTeam']['starters']['reboundsDefensive']
        g['away_starters_rebounds_total'] = data['props']['pageProps']['game']['awayTeam']['starters']['reboundsTotal']
        g['away_starters_assists'] = data['props']['pageProps']['game']['awayTeam']['starters']['assists']
        g['away_starters_steals'] = data['props']['pageProps']['game']['awayTeam']['starters']['steals']
        g['away_starters_blocks'] = data['props']['pageProps']['game']['awayTeam']['starters']['blocks']
        g['away_starters_turnovers'] = data['props']['pageProps']['game']['awayTeam']['starters']['turnovers']
        g['away_starters_foulsPersonal'] = data['props']['pageProps']['game']['awayTeam']['starters']['foulsPersonal']
        g['away_starters_points'] = data['props']['pageProps']['game']['awayTeam']['starters']['points']

        g['home_bench_minutes'] = data['props']['pageProps']['game']['homeTeam']['bench']['minutes']
        g['home_bench_field_goals_made'] = data['props']['pageProps']['game']['homeTeam']['bench']['fieldGoalsMade']
        g['home_bench_field_goals_attempted'] = data['props']['pageProps']['game']['homeTeam']['bench']['fieldGoalsAttempted']
        g['home_bench_field_goals_percentage'] = data['props']['pageProps']['game']['homeTeam']['bench']['fieldGoalsPercentage']
        g['home_bench_three_pointers_made'] = data['props']['pageProps']['game']['homeTeam']['bench']['threePointersMade']
        g['home_bench_three_pointers_attempted'] = data['props']['pageProps']['game']['homeTeam']['bench']['threePointersAttempted']
        g['home_bench_three_pointers_percentage'] = data['props']['pageProps']['game']['homeTeam']['bench']['threePointersPercentage']
        g['home_bench_free_throws_made'] = data['props']['pageProps']['game']['homeTeam']['bench']['freeThrowsMade']
        g['home_bench_free_throws_attempted'] = data['props']['pageProps']['game']['homeTeam']['bench']['freeThrowsAttempted']
        g['home_bench_free_throws_percentage'] = data['props']['pageProps']['game']['homeTeam']['bench']['freeThrowsPercentage']
        g['home_bench_rebounds_offensive'] = data['props']['pageProps']['game']['homeTeam']['bench']['reboundsOffensive']
        g['home_bench_rebounds_defensive'] = data['props']['pageProps']['game']['homeTeam']['bench']['reboundsDefensive']
        g['home_bench_rebounds_total'] = data['props']['pageProps']['game']['homeTeam']['bench']['reboundsTotal']
        g['home_bench_assists'] = data['props']['pageProps']['game']['homeTeam']['bench']['assists']
        g['home_bench_steals'] = data['props']['pageProps']['game']['homeTeam']['bench']['steals']
        g['home_bench_blocks'] = data['props']['pageProps']['game']['homeTeam']['bench']['blocks']
        g['home_bench_turnovers'] = data['props']['pageProps']['game']['homeTeam']['bench']['turnovers']
        g['home_bench_foulsPersonal'] = data['props']['pageProps']['game']['homeTeam']['bench']['foulsPersonal']
        g['home_bench_points'] = data['props']['pageProps']['game']['homeTeam']['bench']['points']

        g['away_bench_minutes'] = data['props']['pageProps']['game']['awayTeam']['bench']['minutes']
        g['away_bench_field_goals_made'] = data['props']['pageProps']['game']['awayTeam']['bench']['fieldGoalsMade']
        g['away_bench_field_goals_attempted'] = data['props']['pageProps']['game']['awayTeam']['bench']['fieldGoalsAttempted']
        g['away_bench_field_goals_percentage'] = data['props']['pageProps']['game']['awayTeam']['bench']['fieldGoalsPercentage']
        g['away_bench_three_pointers_made'] = data['props']['pageProps']['game']['awayTeam']['bench']['threePointersMade']
        g['away_bench_three_pointers_attempted'] = data['props']['pageProps']['game']['awayTeam']['bench']['threePointersAttempted']
        g['away_bench_three_pointers_percentage'] = data['props']['pageProps']['game']['awayTeam']['bench']['threePointersPercentage']
        g['away_bench_free_throws_made'] = data['props']['pageProps']['game']['awayTeam']['bench']['freeThrowsMade']
        g['away_bench_free_throws_attempted'] = data['props']['pageProps']['game']['awayTeam']['bench']['freeThrowsAttempted']
        g['away_bench_free_throws_percentage'] = data['props']['pageProps']['game']['awayTeam']['bench']['freeThrowsPercentage']
        g['away_bench_rebounds_offensive'] = data['props']['pageProps']['game']['awayTeam']['bench']['reboundsOffensive']
        g['away_bench_rebounds_defensive'] = data['props']['pageProps']['game']['awayTeam']['bench']['reboundsDefensive']
        g['away_bench_rebounds_total'] = data['props']['pageProps']['game']['awayTeam']['bench']['reboundsTotal']
        g['away_bench_assists'] = data['props']['pageProps']['game']['awayTeam']['bench']['assists']
        g['away_bench_steals'] = data['props']['pageProps']['game']['awayTeam']['bench']['steals']
        g['away_bench_blocks'] = data['props']['pageProps']['game']['awayTeam']['bench']['blocks']
        g['away_bench_turnovers'] = data['props']['pageProps']['game']['awayTeam']['bench']['turnovers']
        g['away_bench_foulsPersonal'] = data['props']['pageProps']['game']['awayTeam']['bench']['foulsPersonal']
        g['away_bench_points'] = data['props']['pageProps']['game']['awayTeam']['bench']['points']
        g['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        game_players = []
        for player in data['props']['pageProps']['game']['homeTeam']['players']:
            gp = {}
            gp['game_player_key'] = str(g['game_id']) + '|' + str(g['home_team_id']) + '|' + str(player['personId'])
            gp['game_id'] = g['game_id']
            gp['team_id'] = g['home_team_id'] 
            gp['h_a'] = 'H'
            gp['person_id'] = player['personId']
            gp['game_date'] = g['game_date']
            gp['first_name'] = player['firstName']
            gp['family_name'] = player['familyName']
            gp['name_i'] = player['nameI']
            gp['player_slug'] = player['playerSlug']
            gp['position'] = player['position']
            gp['comment'] = player['comment']
            gp['jersey_num'] = player['jerseyNum']
            gp['minutes'] = player['statistics']['minutes']
            gp['field_goals_made'] = player['statistics']['fieldGoalsMade']
            gp['field_goals_attempted'] = player['statistics']['fieldGoalsAttempted']
            gp['field_goals_percentage'] = player['statistics']['fieldGoalsPercentage']
            gp['three_pointers_made'] = player['statistics']['threePointersMade']
            gp['three_pointers_attempted'] = player['statistics']['threePointersAttempted']
            gp['three_pointers_percentage'] = player['statistics']['threePointersPercentage']
            gp['free_throws_made'] = player['statistics']['freeThrowsMade']
            gp['free_throws_attempted'] = player['statistics']['freeThrowsAttempted']
            gp['free_throws_percentage'] = player['statistics']['freeThrowsPercentage']
            gp['rebounds_offensive'] = player['statistics']['reboundsOffensive']
            gp['rebounds_defensive'] = player['statistics']['reboundsDefensive']
            gp['rebounds_total'] = player['statistics']['reboundsTotal']
            gp['assists'] = player['statistics']['assists']
            gp['steals'] = player['statistics']['steals']
            gp['blocks'] = player['statistics']['blocks']
            gp['turnovers'] = player['statistics']['turnovers']
            gp['fouls_personal'] = player['statistics']['foulsPersonal']
            gp['points'] = player['statistics']['points']
            gp['plus_minus_points'] = player['statistics']['plusMinusPoints']
            gp['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            game_players.append(gp)

        for player in data['props']['pageProps']['game']['awayTeam']['players']:
            gp = {}
            gp['game_player_key'] = str(g['game_id']) + '|' + str(g['away_team_id']) + '|' + str(player['personId'])
            gp['game_id'] = g['game_id']
            gp['team_id'] = g['away_team_id'] 
            gp['h_a'] = 'A'
            gp['person_id'] = player['personId']
            gp['game_date'] = g['game_date']
            gp['first_name'] = player['firstName']
            gp['family_name'] = player['familyName']
            gp['name_i'] = player['nameI']
            gp['player_slug'] = player['playerSlug']
            gp['position'] = player['position']
            gp['comment'] = player['comment']
            gp['jersey_num'] = player['jerseyNum']
            gp['minutes'] = player['statistics']['minutes']
            gp['field_goals_made'] = player['statistics']['fieldGoalsMade']
            gp['field_goals_attempted'] = player['statistics']['fieldGoalsAttempted']
            gp['field_goals_percentage'] = player['statistics']['fieldGoalsPercentage']
            gp['three_pointers_made'] = player['statistics']['threePointersMade']
            gp['three_pointers_attempted'] = player['statistics']['threePointersAttempted']
            gp['three_pointers_percentage'] = player['statistics']['threePointersPercentage']
            gp['free_throws_made'] = player['statistics']['freeThrowsMade']
            gp['free_throws_attempted'] = player['statistics']['freeThrowsAttempted']
            gp['free_throws_percentage'] = player['statistics']['freeThrowsPercentage']
            gp['rebounds_offensive'] = player['statistics']['reboundsOffensive']
            gp['rebounds_defensive'] = player['statistics']['reboundsDefensive']
            gp['rebounds_total'] = player['statistics']['reboundsTotal']
            gp['assists'] = player['statistics']['assists']
            gp['steals'] = player['statistics']['steals']
            gp['blocks'] = player['statistics']['blocks']
            gp['turnovers'] = player['statistics']['turnovers']
            gp['fouls_personal'] = player['statistics']['foulsPersonal']
            gp['points'] = player['statistics']['points']
            gp['plus_minus_points'] = player['statistics']['plusMinusPoints']
            gp['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            game_players.append(gp)
                    
        team_period_scores = []
        for team in data['props']['pageProps']['game']['homeTeam']['periods']:
            tps = {}
            tps['game_team_period_score_key'] = str(g['game_id']) + '|' + str(g['home_team_id']) + '|' + str(team['period'])
            tps['game_id'] = g['game_id']
            tps['team_id'] = g['home_team_id'] 
            tps['h_a'] = 'H'
            tps['game_date'] = g['game_date']
            tps['period'] = team['period']
            tps['period_type'] = team['periodType']
            tps['score'] = team['score']
            tps['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            team_period_scores.append(tps)
        for team in data['props']['pageProps']['game']['awayTeam']['periods']:
            tps = {}
            tps['game_team_period_score_key'] = str(g['game_id']) + '|' + str(g['away_team_id'])  + '|' + str(team['period'])
            tps['game_id'] = g['game_id']
            tps['team_id'] = g['away_team_id'] 
            tps['h_a'] = 'A'
            tps['game_date'] = g['game_date']
            tps['period'] = team['period']
            tps['period_type'] = team['periodType']
            tps['score'] = team['score']
            tps['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            team_period_scores.append(tps)

        inactives = []
        for inactive in data['props']['pageProps']['game']['homeTeam']['inactives']:  
            i = {}
            i['game_inactive_key'] = str(g['game_id']) + '|' + str(g['home_team_id']) 
            i['game_id'] = g['game_id']
            i['team_id'] = g['home_team_id'] 
            i['h_a'] = 'H'
            i['game_date'] = g['game_date']
            i['person_id'] = inactive['personId']
            i['first_name'] = inactive['firstName']
            i['family_name'] = inactive['familyName']
            i['jersey_num'] = inactive['jerseyNum']
            i['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            inactives.append(i)
        for inactive in data['props']['pageProps']['game']['awayTeam']['inactives']: 
            i = {} 
            i['game_inactive_key'] = str(g['game_id']) + '|' + str(g['away_team_id']) 
            i['game_id'] = g['game_id']
            i['team_id'] = g['away_team_id'] 
            i['h_a'] = 'A'
            i['game_date'] = g['game_date']
            i['person_id'] = inactive['personId']
            i['first_name'] = inactive['firstName']
            i['family_name'] = inactive['familyName']
            i['jersey_num'] = inactive['jerseyNum']
            i['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            inactives.append(i)

        officials = []
        for official in data['props']['pageProps']['game']['officials']:
            o = {}
            o['game_official_key'] = str(g['game_id']) + '|' + str(official['personId'])
            o['game_id'] = g['game_id']
            o['person_id'] = official['personId']    
            o['game_date'] = g['game_date']
            o['name'] = official['name']
            o['name_i'] = official['nameI']
            o['first_name'] = official['firstName']
            o['family_name'] = official['familyName']
            o['jersey_num'] = official['jerseyNum']
            o['assignment'] = official['assignment']
            o['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            officials.append(o)

        events = []
        for play in data['props']['pageProps']['playByPlay']['actions']:
            p = {}
            p['game_event_key'] = str(g['game_id']) + '|' + str(play['actionNumber'])
            p['game_id'] = g['game_id']  
            p['game_date'] = g['game_date']
            p['action_number'] = play['actionNumber']
            p['clock'] = play['clock']
            p['period'] = play['period']
            p['team_id'] = play['teamId']
            p['team_tricode'] = play['teamTricode']
            p['person_id'] = play['personId']
            p['player_name'] = play['playerName']
            p['player_name_i'] = play['playerNameI']
            p['x_legacy'] = play['xLegacy']
            p['y_legacy'] = play['yLegacy']
            p['shot_distance'] = play['shotDistance']
            p['shot_result'] = play['shotResult']
            p['is_field_goal'] = play['isFieldGoal']
            p['score_home'] = play['scoreHome']
            p['score_away'] = play['scoreAway']
            p['points_total'] = play['pointsTotal']
            p['location'] = play['location']
            p['description'] = play['description']
            p['action_type'] = play['actionType']
            p['sub_type'] = play['subType']
            p['video_available'] = play['videoAvailable']
            p['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            events.append(p)

        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        #print(lines_to_load)
        #print(consensus_to_load)
        game_data_to_load = []
        game_data_to_load.append(g)

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game'
        replication_data['data'] = game_data_to_load
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game_player'
        replication_data['data'] = game_players
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game_team_period_score'
        replication_data['data'] = team_period_scores
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game_inactive'
        replication_data['data'] = inactives
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game_official'
        replication_data['data'] = officials
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbacom_game_event'
        replication_data['data'] = events
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        
        return f'NBA.com game successfully scraped'


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

            
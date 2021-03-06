import requests
import json
import datetime
from django.conf import settings
import pandas as pd
from decimal import Decimal

base_url = "https://delivery.chalk247.com"


def api_call(start_date, end_date):
    try:
        score_url = f"{base_url}/scoreboard/NFL/{start_date}/{end_date}.json?api_key={settings.NFL_API_KEY}"
        events_url = f"{base_url}/team_rankings/NFL.json?api_key={settings.NFL_API_KEY}"

        scores_data = requests.get(url=score_url).json()['results']
        rankings_data = requests.get(url=events_url).json()['results']['data']
        scoreboard_results = {event_key: scores_data[score]['data'][event_key]
                              for score in scores_data.keys() if len(scores_data[score]) > 0
                              for event_key in scores_data[score]['data'].keys()}

        for sb in scoreboard_results:
            event_date = datetime.datetime.strptime(scoreboard_results[sb]['event_date'], "%Y-%m-%d %H:%M")
            scoreboard_results[sb]['event_time'] = event_date.strftime('%H:%M')
            scoreboard_results[sb]['event_date'] = event_date.strftime('%d-%m-%Y')

        api_keys_subset = [
            "event_id", "event_date", "away_team_id", "away_nick_name",
            "away_city", "home_team_id", "home_city", "home_nick_name",
            "event_time"
        ]
        frame = pd.DataFrame(scoreboard_results).transpose()[api_keys_subset]
        new_score_data_json = json.loads(frame.to_json(orient='records'))
        df = pd.DataFrame(rankings_data)[['team_id', 'rank', 'adjusted_points']]
        new_ranks_json = json.loads(df.to_json(orient='records'))
        for event in new_score_data_json:
            for ranking in new_ranks_json:
                if event['away_team_id'] == ranking["team_id"]:
                    event['away_rank'] = ranking['rank']
                    event['away_rank_points'] = '{0:.2f}'.format(Decimal(ranking['adjusted_points']))
                    break
            for ranking in new_ranks_json:
                if event['home_team_id'] == ranking["team_id"]:
                    event['home_rank'] = ranking['rank']
                    event['home_rank_points'] = '{0:.2f}'.format(Decimal(ranking['adjusted_points']))
                    break
        return new_score_data_json
    except Exception as e:
        return ValueError(str(e))

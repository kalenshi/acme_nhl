import requests

score_board_url = "https://delivery.chalk247.com/" \
                  "scoreboard/NFL/2020-01-12/" \
                  "2020-01-19.json?api_key" \
                  "=74db8efa2a6db279393b433d97c2bc843f8e32b0"
rankings_url = "https://delivery.chalk247.com/team_rankings" \
               "/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0"


def api_call(date_range=None):
    try:
        score_data = requests.get(score_board_url).json()['results']
        rankings_data = requests.get(rankings_url).json()['results']['data']  # This is an array
        ['event_id', 'event_data', 'away_team_id', 'away_nick_name', 'away_city']
        ['rank', 'adjusted_points', '']
        return score_data
    except Exception as e:
        print("Error")

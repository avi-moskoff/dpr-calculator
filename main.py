import numpy as np
import functools

teams = [498, 1011, 2375, 2403, 2662, 4183, 5059, 6352, 6413, 8848, 9985]

matches = [
    {
        "red": [2662, 1011, 2375],
        "blue": [6352, 9985, 4183],
        "red_score": 11,
        "blue_score": 62,
    },
    {
        "red": [8848, 6413, 498],
        "blue": [2403, 5059, 6352],
        "red_score": 64,
        "blue_score": 68,
    },
    {
        "red": [8848, 6413, 4183],
        "blue": [9985, 5059, 2375],
        "red_score": 58,
        "blue_score": 6,
    },
    {
        "red": [1011, 2662, 9985],
        "blue": [498, 2403, 6413],
        "red_score": 15,
        "blue_score": 76,
    },
    {
        "red": [6352, 8848, 1011],
        "blue": [2375, 2662, 498],
        "red_score": 43,
        "blue_score": 31,
    },
    {
        "red": [8848, 2403, 498],
        "blue": [5059, 4183, 2662],
        "red_score": 86,
        "blue_score": 37,
    },
    {
        "red": [
            9985,
            6352,
            5059,
        ],
        "blue": [2403, 1011, 4183],
        "red_score": 14,
        "blue_score": 66,
    },
    {
        "red": [2375, 5059, 8848],
        "blue": [1011, 6413, 9985],
        "red_score": 16,
        "blue_score": 42,
    },
    {
        "red": [498, 6352, 6413],
        "blue": [2375, 4183, 2403],
        "red_score": 102,
        "blue_score": 82,
    },
    {
        "red": [2662, 2375, 498],
        "blue": [1011, 4183, 5059],
        "red_score": 38,
        "blue_score": 44,
    },
    {
        "red": [6352, 2662, 8848],
        "blue": [9985, 6413, 2403],
        "red_score": 16,
        "blue_score": 66,
    },
    {
        "red": [2662, 1011, 6352],
        "blue": [6413, 8848, 5059],
        "red_score": 20,
        "blue_score": 50,
    },
    {
        "red": [4183, 498, 9985],
        "blue": [6413, 2375, 2403],
        "red_score": 76,
        "blue_score": 66,
    },
    {
        "red": [5059, 1011, 2403],
        "blue": [4183, 6352, 2375],
        "red_score": 52,
        "blue_score": 58,
    },
    {
        "red": [2662, 498, 5059],
        "blue": [9985, 8848, 2375],
        "red_score": 36,
        "blue_score": 25,
    },
    {
        "red": [498, 6352, 8848],
        "blue": [6413, 4183, 1011],
        "red_score": 71,
        "blue_score": 64,
    },
    {
        "red": [498, 6352, 8848],
        "blue": [6413, 4183, 1011],
        "red_score": 71,
        "blue_score": 64,
    },
    {
        "red": [2403, 9985, 1011],
        "blue": [2662, 4183, 6413],
        "red_score": 22,
        "blue_score": 54,
    },
    {
        "red": [8848, 2662, 9985],
        "blue": [2403, 6352, 2375],
        "red_score": 20,
        "blue_score": 56,
    },
]

# 'dpr' or 'opr'
dpr_or_opr = "opr"

if __name__ == "__main__":
    red_matches = list(
        map(
            lambda match: list(
                map(lambda team: 1 if team in match["red"] else 0, teams)
            ),
            matches,
        )
    )

    blue_matches = list(
        map(
            lambda match: list(
                map(lambda team: 1 if team in match["blue"] else 0, teams)
            ),
            matches,
        )
    )

    red_scores = list(map(lambda match: match["red_score"], matches))

    blue_scores = list(map(lambda match: match["blue_score"], matches))

    match_matrix = np.matrix(red_matches + blue_matches)

    # if we are calculating OPR, we match teams up with their own scores
    # Otherwise, we match teams up with their opponent's score for DPR.
    score_vector = (
        np.array(red_scores + blue_scores)
        if dpr_or_opr == "opr"
        else np.array(blue_scores + red_scores)
    )

    A = np.matmul(match_matrix.transpose(), match_matrix)
    B = np.matmul(match_matrix.transpose(), score_vector).transpose()

    power_rating = np.linalg.solve(A, B)

    # Now, we want to know the average deviation from the opponent's expected score when a given team is playing.

    power_rating_map = {teams[i]: power_rating[i].item(0) for i in range(len(teams))}
    print(power_rating_map)

    total_matches_played = {
        team: functools.reduce(
            lambda acc, match: acc
            + (1 if team in match["red"] or team in match["blue"] else 0),
            matches,
            0,
        )
        for team in teams
    }

    def get_deviation(acc, match, team):
        opposing_alliance = "red" if team in match["blue"] else "blue"

        expected_opposing_score = functools.reduce(
            lambda score_acc, opposing_team: score_acc
            + power_rating_map[opposing_team],
            match[opposing_alliance],
            0,
        )

        # Will be positive if the team blocked points in this match
        return acc + expected_opposing_score - match[f"{opposing_alliance}_score"]

    total_points_prevented = {
        team: functools.reduce(
            lambda acc, match: get_deviation(acc, match, team), matches, 0
        )
        for team in teams
    }

    average_points_blocked = {
        team: total_points_prevented[team] / total_matches_played[team]
        for team in teams
    }

    for team in teams:
        print(team, average_points_blocked[team])

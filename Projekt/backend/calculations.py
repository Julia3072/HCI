import json

bound_low = 50
bound_high = 10
timespan = 5
maxScore = 100

heart_rate_bound_low = 70
heart_rate_bound_high = 80


def calculate_difficulty_score(song_file):
    """
    calculates a songs difficulty based on the reference json
    """
    with open(song_file) as data_file:
        data = json.load(data_file)

        # define arrays and counters
        color_ref = [data["green"], data["blue"], data["red"], data["yellow"]]
        color_cnt = [0] * 4

        values, old_time = [], 0

        while any([color_cnt[j] < len(color_ref[j]) for j in range(4)]):
            currents = []

            for i in range(4):
                if color_cnt[i] < len(color_ref[i]):
                    currents.append(color_ref[i][color_cnt[i]])

            # get minimum
            minimum = min(currents)

            number_currents, difficulty_number, difficulty_time = 0, 0, 0

            # count how many of these entries are the minimum and increase counter
            for i in range(4):
                if color_cnt[i] < len(color_ref[i]) and \
                                color_ref[i][color_cnt[i]] <= minimum + timespan:
                    number_currents += 1
                    color_cnt[i] += 1

            # transform to difficulty
            difficulty_number += 1 if number_currents == 1 else 3

            # get time between last and current key
            diff = minimum - old_time
            old_time = minimum

            # transform to difficulty
            difficulty_time += 3 if diff < bound_high else (2 if bound_high <= diff < bound_low else 1)

            # add to values
            values.append(difficulty_number * difficulty_time)

        difficulty = sum(values) / len(values)
        return int(maxScore - 10 * difficulty + 0.5)


def calculate_song_score(n_correct, n_insg, sums_ref, heart_avg):
    """
        calculates the score of a played game
    """
    # amount correctly played subtracted the number of unnecessary touches
    score = int(100 * (n_correct / sums_ref) - max((100 * (n_insg.value - sums_ref) / sums_ref), 0))

    # add bonus points based on average heart rate
    avg_heart_rate = sum(list(heart_avg)) / len(heart_avg)

    if avg_heart_rate < heart_rate_bound_low:
        score -= 5
    elif avg_heart_rate > heart_rate_bound_high:
        score += 5

    # make sure 0 <= score <= 100
    return min(max(score, 0), 100)

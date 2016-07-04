import json


class DifficultyCalculator:
    bound_low = 50
    bound_high = 10
    maxScore = 100

    data = ""

    def __init__(self, songFile):
        with open(songFile) as data_file:
            self.data = json.load(data_file)

    def calculateDifficulty(self):
        # get arrays
        green = self.data["green"]
        blue = self.data["blue"]
        red = self.data["red"]
        yellow = self.data["yellow"]

        # define counter
        c_green = 0
        c_blue = 0
        c_red = 0
        c_yellow = 0
        values = []
        oldTime = 0

        while c_green < len(green) or c_blue < len(blue) or c_red < len(red) or c_yellow < len(yellow):
            # get next entry
            currents = []
            if c_green < len(green):
                currents.append(green[c_green])
            if c_blue < len(blue):
                currents.append(blue[c_blue])
            if c_red < len(red):
                currents.append(red[c_red])
            if c_yellow < len(yellow):
                currents.append(yellow[c_yellow])

            # get minimum
            minimum = min(currents)
            numberCurrents = 0
            difficultyNumber = 0
            difficultyTime = 0

            # count how many of these entries are the minimum and increase counter
            if c_green < len(green) and green[c_green] == minimum:
                numberCurrents += 1
                c_green += 1
            if c_blue < len(blue) and blue[c_blue] == minimum:
                numberCurrents += 1
                c_blue += 1
            if c_red < len(red) and red[c_red] == minimum:
                numberCurrents += 1
                c_red += 1
            if c_yellow < len(yellow) and yellow[c_yellow] == minimum:
                numberCurrents += 1
                c_yellow += 1

            # transform to difficulty
            if numberCurrents == 1:
                difficultyNumber += 1
            else:
                difficultyNumber += 3

            # get time between last and current key
            diff = minimum - oldTime
            oldTime = minimum

            # transform to diffculty
            if diff < self.bound_high:
                difficultyTime += 3
            else:
                if self.bound_high <= diff and diff < self.bound_low:
                    difficultyTime += 2
                else:
                    difficultyTime += 1

            # add to values
            values.append(difficultyNumber * difficultyTime)

        return sum(values) / len(values)

    def getScore(self):
        difficulty = self.calculateDifficulty()
        return int(self.maxScore - 10 * difficulty + 0.5)


calc = DifficultyCalculator("backend/reference_song.json");
print(calc.getScore());

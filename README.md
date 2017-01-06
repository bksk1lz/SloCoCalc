# SloCoCalc
Calculates series standings and handicaps for Orienteering races from IOF XML results files
Compatible with IOF XML v2.0.3, working on v3.0

# Instructions
You'll need all the results files from your race series in a single folder. If you want to score men and women separately, create a file in the same folder named `women.txt` with one name per line (first and last) of each of the women. If you want to award bonues points to meet directors for the meet the direct, make a file named `MeetDirectors.txt` with one name per line (first and last) of the meet directors.

Run ScoreCalculator.py and follow prompts. The "number of races to count" is how many races will contribute to each racer's point total, ie you want to take the best 8 of 12 races so enter 8 there.

Results are saved in `output.csv` in the same folder as your data.

# More coming soon!

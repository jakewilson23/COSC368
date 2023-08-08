"""Write a separate python program that inputs each trial's data from the log file into a dictionary of key-value
pairs, where each key is a tuple of the form (amplitude, width, selection number) and the value is the associated time.

Modify this program so that it calculates the average time across all selections for each combination of amplitude
and width. The results should then be written to a file "summary.csv” in the following format:

A	W	ID	mean time
64	8	3.17	2.054
64	16	2.32	1.786
64	32	1.58	1.842
128	8	5.04	2.094

. . . Where the first column shows the amplitude, the second width, the third is the index of difficulty (use
math.log2 to calculate the logarithm value), and the fourth column is the mean time for all of the repeated trials.

Note: Mean times should be in seconds not milliseconds. If you're using the demo programs provided (or made your own
program match the behaviour of those), you'll need to divide the times by 1000 (as the times there were written in
milliseconds).

Remove the outliers Next, modify your script so that it ignores the first two selections in each block (combination
of amplitude and width). The first trial, in particular, is likely to be an outlier because the user must identify
the new target location while the clock is running. Eliminating the first two trials should reduce the noise in your
sample.

Group results by ID Finally, modify your program so that it calculates the mean time for each ID (note that some IDs
will correspond to multiple different amplitude/width pairs) and writes the results to the summary.csv file,
with ID in column 1 and mean time in column 2, as shown below:

ID	mean time
1.585	0.578
2.322	0.634
3.170	0.787
4.087	0.932
5.044	1.102
6.022	1.18
"""
import csv
import math
NUM_OF_SELECTIONS = 8

f = open('fitts_law_test_ui_log.txt', 'r')
contents = f.readlines()

# each key is a tuple of the form (amplitude, width, selection number) and the value is the associated time.
# don't include the first 2 values of each selection to eliminate noise from the results.
result_dict = {}
for count, result in enumerate(contents):
    if (count % NUM_OF_SELECTIONS != 0) and (count % NUM_OF_SELECTIONS != 1):
        string_list = result.split(" ")
        result_dict[(int(string_list[1]), int(string_list[2]), int(string_list[3]))] = float(string_list[4].strip())
# print(result_dict)

# each key is a tuple of the form (amplitude, width, ID) and the value is the associated times added up.
# ID (Index of Difficulty) = log2 (Amplitude/Width + 1), also round it to 2 decimal place
average_dict = {}
for k in result_dict:
    ID = round(math.log2(k[0]/k[1] + 1), 2)
    if (k[0], k[1], ID) in average_dict:
        average_dict[(k[0], k[1], ID)] += result_dict[k]
    else:
        average_dict[(k[0], k[1], ID)] = result_dict[k]
# print(average_dict)

# for each of the added up values divide them by the number of results in them to make the average
# the number of results in each value is the length of the first dict / length of the second dict
# also times by 1000 to get from milliseconds to seconds and round to 3 decimal place
for time in average_dict:
    average_dict[time] = round((average_dict[time] / (len(result_dict) / len(average_dict)) / 1000), 3)
# print(average_dict)

# calculate the mean time for each ID (note that some IDs will correspond to multiple different amplitude/width pairs)
id_dict = {}
for k in average_dict:
    if (k[2]) in id_dict:
        id_dict[k[2]].append(average_dict[k])
    else:
        id_dict[k[2]] = [average_dict[k]]
for k in id_dict:
    temp_list = id_dict[k]
    id_dict[k] = round(sum(temp_list) / len(temp_list), 3)
# print(id_dict)

with open('summary.csv', 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Mean Time']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for item in id_dict:
        output = [item, id_dict[item]]
        writer.writerow(output)

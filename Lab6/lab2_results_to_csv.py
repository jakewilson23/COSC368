"""
Your program should record a log of selections with the letter in the first column, the block number (0 to 5) in the
second column, and the time from cue exposure to selection in the third column in seconds, as follows:

c  0  2.46
"""
import csv

"""
Each test to convert to csv is a tuple in the format
(File to Convert to CSV, Name of CSV file to convert to)
and is appended to the test_result_list list.
"""
test_result_list = [('experiment_dynamic_log.txt', 'experiment_dynamic_log.csv'),
                    ('experiment_static_log.txt', 'experiment_static_log.csv')]

for test in test_result_list:
    f = open(test[0], 'r')
    contents = f.readlines()
    result_list = []
    for count, result in enumerate(contents):
        string_list = result.split(" ")
        milliseconds = float(string_list[4].strip())
        result_list.append([string_list[2], int(string_list[3]), round((milliseconds / 1000), 2)])
    with open(test[1], 'w', newline='') as csvfile:
        fieldnames = ['Letter', 'Block Number', 'Time From Cue Exposure']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for item in result_list:
            writer.writerow(item)

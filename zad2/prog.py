import os
import sys

files_stats = dict()
sum_of_files = 0
MAX_GRAPH_EXTENSION = 5
MAX_GRAPH_SIZE = 15
MAX_GRAPH_COUNT = 60
GRAPH_CHAR = '#'

def scan_dir(dir):
    for dirEntry in os.scandir(dir):
        if dirEntry.is_dir():
            scan_dir(dirEntry.path)
        elif dirEntry.is_file():
            extract_properties_from_file(dirEntry)


def extract_properties_from_file(entry):
    global sum_of_files
    entryExtension = entry.name.split('.')[-1]
    entrySize = entry.stat().st_size
    if entryExtension in files_stats:
        files_stats[entryExtension][0] += 1 #increase counter for file extension
        files_stats[entryExtension][1] += entrySize #increase sum size
    else:
        files_stats[entryExtension] = [1,entrySize,0]
    sum_of_files += 1

def count_graph(extensions):
    for ext in extensions:
        ext[1][2] = round(ext[1][0] / sum_of_files * MAX_GRAPH_COUNT)

def print_to_file(file,extensions):
    output_file = open(file, "w")
    for ext in extensions:
        output_file.write("{0}{1}B{2}\n".format(
            ext[0].rjust(MAX_GRAPH_EXTENSION),
            str(ext[1][1]).rjust(MAX_GRAPH_SIZE-1),
            (GRAPH_CHAR * ext[1][2]).rjust(MAX_GRAPH_COUNT)
        ))
    output_file.close

def main(args):
    inputdir = ''
    outputfile = ''

    if len(args) != 2:
        print("Usage: inputDir outputFile")
        sys.exit(2)
    else:
        inputdir = args[0]
        outputfile = args[1]

    scan_dir(inputdir)
    sorted_extensions = sorted(files_stats.items(), key=lambda l: l[1], reverse=True)
    count_graph(sorted_extensions)
    print_to_file(outputfile,sorted_extensions)

if __name__ == "__main__":
    main(sys.argv[1:])

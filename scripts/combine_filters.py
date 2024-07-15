def combine_filter_lists(input_files, output_file):
    combined_filters = set()

    # Read each input file and add its lines to the set
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith(('!', '[', '#')):
                    combined_filters.add(cleaned_line)

    # Sort the combined filters
    sorted_filters = sorted(combined_filters)

    # Write the sorted filters to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for filter in sorted_filters:
            f.write(filter + '\n')

# Example usage
input_files = ['filterlist1.txt', 'filterlist2.txt', 'filterlist3.txt']
output_file = 'combined_filterlist.txt'
combine_filter_lists(input_files, output_file)


# run 'python combine_filters.py'

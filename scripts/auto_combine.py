import requests
import os

def download_filter_list(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

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

# Define multiple sets of URLs and output files
filter_sets = {
    'set1': {
        'urls': [
            'https://example.com/filterlist1.txt',
            'https://example.com/filterlist2.txt',
            'https://example.com/filterlist3.txt'
        ],
        'output_file': 'combined_filterlist_set1.txt'
    },
    'set2': {
        'urls': [
            'https://example.com/anotherfilterlist1.txt',
            'https://example.com/anotherfilterlist2.txt'
        ],
        'output_file': 'combined_filterlist_set2.txt'
    }
    # Add more sets as needed
}

# Process each set
for set_name, set_data in filter_sets.items():
    input_files = []
    for i, url in enumerate(set_data['urls'], start=1):
        filename = f'{set_name}_filterlist{i}.txt'
        download_filter_list(url, filename)
        input_files.append(filename)
    combine_filter_lists(input_files, set_data['output_file'])

    # Clean up temporary files
    for file in input_files:
        os.remove(file)

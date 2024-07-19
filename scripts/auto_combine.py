import requests
import os
from datetime import datetime

def download_filter_list(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_domain(domain):
    # Remove 'www.' from the start of the domain
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove 'www.' from the start
    return domain

def combine_filter_lists(input_files, output_file, comments=None):
    combined_filters = set()

    # Read each input file and add its lines to the set
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith(('!', '[', '#')):
                    # Adjust the domain to be pure
                    if cleaned_line.startswith('||'):
                        cleaned_line = cleaned_line[2:]
                    if cleaned_line.endswith('^'):
                        cleaned_line = cleaned_line[:-1]
                    
                    cleaned_domain = clean_domain(cleaned_line)
                    combined_filters.add(cleaned_domain)

    # Sort the combined filters
    sorted_filters = sorted(combined_filters)
    
    # Count the number of entries after all cleaning
    num_entries = len(sorted_filters)

    # Generate last modified date and version
    last_modified = datetime.now().strftime("%B %d, %Y")
    version = datetime.now().strftime("%Y%m%d")

    # Write the sorted filters with comments to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        if comments:
            f.write('\n'.join(comments) + '\n')
            f.write(f"! Version: {version}\n")
            f.write(f"! Last modified: {last_modified}\n")
            f.write(f"! Entries: {num_entries}\n")
            f.write('\n')
        for filter in sorted_filters:
            f.write(f"||{filter}^\n")

# Define multiple sets of URLs, output files, and comments
filter_sets = {
    'nsfw': {
        'urls': [
            'https://raw.githubusercontent.com/DevShubam/Filters/main/nsfw/nsfw-personal.txt',
            'https://airvpn.org/api/dns_lists/?code=pornaway_sites&style=domains',
            'https://blocklistproject.github.io/Lists/adguard/porn-ags.txt',
            'https://raw.githubusercontent.com/ShadowWhisperer/BlockLists/master/RAW/Adult',
            'https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/pornblock4'
        ],
        'output_file': 'nsfw/nsfw_combined.txt',
        'comments': [
            "[AdBlock Plus 2.0]",
            "! Title: Blockd NSFW",
            "! Expires: 2 days (update frequency)",
            "! Description: Block Adult content"
        ]
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
    
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(set_data['output_file']), exist_ok=True)
    
    combine_filter_lists(input_files, set_data['output_file'], set_data.get('comments'))

    # Clean up temporary files
    for file in input_files:
        os.remove(file)

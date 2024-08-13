import requests
import os
from datetime import datetime

# Define a limit for the number of entries per file
ENTRY_LIMIT = 500000

def download_filter_list(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_domain(domain):
    # Remove '0.0.0.0 ' from the start of the domain
    if domain.startswith('0.0.0.0 '):
        domain = domain[8:]
    
    # Remove 'www.' from the start of the domain
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def write_filter_file(output_file, filters, comments=None):
    with open(output_file, 'w', encoding='utf-8') as f:
        if comments:
            f.write('\n'.join(comments) + '\n')
            f.write('\n')
        for filter in filters:
            f.write(f"||{filter}^\n")

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
    total_entries = len(sorted_filters)

    # Generate last modified date and version
    last_modified = datetime.now().strftime("%B %d, %Y")
    version = datetime.now().strftime("%Y%m%d")

    # Update comments with the current date and entry count
    if comments:
        comments.append(f"! Version: {version}")
        comments.append(f"! Last modified: {last_modified}")
        comments.append(f"! Entries: {total_entries}")

    # Write the full combined list
    write_filter_file(output_file, sorted_filters, comments)

    # Split into parts if necessary
    for i in range(0, total_entries, ENTRY_LIMIT):
        part_filters = sorted_filters[i:i + ENTRY_LIMIT]
        part_number = (i // ENTRY_LIMIT) + 1
        part_output_file = f"{output_file.rsplit('.', 1)[0]}-part{part_number}.txt"
        
        # Update comments with the correct title and entry count for the part
        part_comments = comments.copy()
        part_comments[1] = f"! Title: {comments[1].replace('Title:', '').strip()} (part {part_number})"
        part_comments[-1] = f"! Entries: {len(part_filters)}"
        
        write_filter_file(part_output_file, part_filters, part_comments)

# Define multiple sets of URLs, output files, and comments
filter_sets = {
    'nsfw': {
        'urls': [
            'https://raw.githubusercontent.com/DevShubam/Filters/main/nsfw/nsfw-personal.txt',
            'https://airvpn.org/api/dns_lists/?code=pornaway_sites&style=domains',
            'https://blocklistproject.github.io/Lists/adguard/porn-ags.txt',
            'https://raw.githubusercontent.com/ShadowWhisperer/BlockLists/master/RAW/Adult',
            'https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/pornblock4',
            'https://nsfw.oisd.nl'
        ],
        'output_file': 'nsfw/nsfw_combined.txt',
        'comments': [
            "[AdBlock Plus 2.0]",
            "! Title: Blockd NSFW",
            "! Description: Block Adult content",
            "! Homepage: https://github.com/DevShubam/Filters"
        ]
    },
    'gambling': {
        'urls': [
            'https://github.com/DevShubam/Filters/raw/main/gambling/gambling-personal.txt',
            'https://github.com/blocklistproject/Lists/raw/master/gambling.txt',
            'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/gambling-onlydomains.txt',
            'https://github.com/StevenBlack/hosts/raw/master/alternates/gambling/hosts'
        ],
        'output_file': 'gambling/gambling-combined.txt',
        'comments': [
            "[AdBlock Plus 2.0]",
            "! Title: Blockd Gambling",
            "! Description: Block Gambling Domains",
            "! Homepage: https://github.com/DevShubam/Filters"
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

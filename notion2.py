from notion_client import Client
import os
import re

def extract_doi(page):
    properties = page['properties']
    url = properties['URL']['url'] if properties['URL']['url'] else ""
    doi = properties['doi']['rich_text'][0]['plain_text'] if properties['doi']['rich_text'] else url # Assume non Arxiv links are doi-able that myst will automatically render
    if url and 'arxiv.org' in url:
        # Extract arXiv ID from URL
        arxiv_match = re.search(r'arxiv\.org/(?:abs|pdf|html)/(\d+\.\d+)', url)
        if arxiv_match:
            arxiv_id = arxiv_match.group(1)
            # Format as DOI (arXiv DOIs follow the pattern 10.48550/arXiv.XXXX.XXXXX)
            return f"https://doi.org/10.48550/arXiv.{arxiv_id}"
    return doi


def create_doc_page(page):
    """Create a documentation page for a paper if docs property is true"""
    properties = page['properties']
    title = properties['Title']['title'][0]['plain_text'] if properties['Title']['title'] else "Untitled"
    description = properties['Description']['rich_text'][0]['plain_text'] if properties['Description']['rich_text'] else ""
    tags = [tag['name'] for tag in properties['Tags']['multi_select']]
    slug = properties['slug']['rich_text'][0]['plain_text'] if properties['slug']['rich_text'] else ""
    doi_url = extract_doi(page)
    
    # Create the docs directory if it doesn't exist
    if not os.path.exists('paper-notes'):
        os.makedirs('paper-notes')

    # Generate filename from title
    filepath = f'paper-notes/{slug}.md'
    
    # Create page content with YAML frontmatter
    content = f"""
# {title}

## Overview
{description}

## Links
- [Paper]({doi_url})
- Tags: {', '.join(tags)}

## Notes
"""
    
    # Add blocks content if available
    try:
        blocks = notion.blocks.children.list(page['id'])
        for block in blocks['results']:
            if block['type'] == 'paragraph':
                text = block['paragraph']['rich_text']
                if text:
                    content += text[0]['plain_text'] + '\n\n'
            elif block['type'] == 'heading_2':
                text = block['heading_2']['rich_text']
                if text:
                    content += f"## {text[0]['plain_text']}\n\n"
            elif block['type'] == 'heading_3':
                text = block['heading_3']['rich_text']
                if text:
                    content += f"### {text[0]['plain_text']}\n\n"
            elif block['type'] == 'bulleted_list_item':
                text = block['bulleted_list_item']['rich_text']
                if text:
                    content += f"- {text[0]['plain_text']}\n"
    except Exception as e:
        print(f"Error fetching blocks for {title}: {e}")
    
    # Write the content to the file
    with open(filepath, 'w') as f:
        f.write(content)
    
    return slug

def process_paper_notes(page):
    """Process a Paper-Notes type page and return MyST list table entry"""
    # Extract basic information
    properties = page['properties']
    title = properties['Title']['title'][0]['plain_text'] if properties['Title']['title'] else "Untitled"
    tags = [tag['name'] for tag in properties['Tags']['multi_select']]

    doi_url = extract_doi(page)
    
    # Check if docs property is true
    docs_enabled = properties.get('docs', {}).get('checkbox', False)

    publish = properties.get('publish', {}).get('checkbox', False)

    if not publish:
        return
    
    # Generate docs page if enabled
    details_link = ""
    if docs_enabled:
        filename = create_doc_page(page)
        details_link = f"[Details]({filename})"
    else:
        details_link = ""

    # Start building the content if it doesn't exist
    header = """# Papers Overview

A collection of papers with summaries and quick access links.

## Paper Notes

```{list-table}
:header-rows: 1

* - Title
  - Tags
  - Full Notes
"""

    # Create the list table row
    table_row = f"* - [{title}]({doi_url})\n  - {', '.join(tags)}\n  - {details_link}\n"

    # Try to read existing content
    try:
        with open('paper-notes/index.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = header

    # Add the new row if it's not already there
    if title not in content:
        # If the file is new or empty, add the header
        if "```{list-table}" not in content:
            content = header

        # Add the new row
        if content.endswith('\n'):  # If there's already content
            content += table_row
        else:  # If we just added the header
            content += table_row

        # Write the updated content
        with open('paper-notes/index.md', 'w') as f:
            f.write(content)
            return details_link

def process_glossary(page):
    """Process a Glossary type page and return MyST list table entry"""
    # Extract basic information
    properties = page['properties']
    title = properties['Title']['title'][0]['plain_text'] if properties['Title']['title'] else "Untitled"
    description = properties['Description']['rich_text'][0]['plain_text'] if properties['Description']['rich_text'] else ""
    tags = [tag['name'] for tag in properties['Tags']['multi_select']]

    publish = properties.get('publish', {}).get('checkbox', False)

    if not publish:
        return

    # Generate docs page if enabled
    details_link = ""
    # Assuming you have a similar function for glossary docs
    filename = create_glossary_doc_page(page)
    details_link = f"[Details]({filename})"
    
    # Start building the content if it doesn't exist
    header = """# Glossary

A collection of terms and definitions used throughout the documentation.

```{list-table}
:header-rows: 1

* - Term
  - Tags
  - Full Notes
"""

    # Create the list table row
    table_row = f"* - {title}\n  - {', '.join(tags)}\n  - {details_link}\n"

    # Try to read existing content
    try:
        with open('glossary/index.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = header

    # Add the new row if it's not already there
    if title not in content:
        # If the file is new or empty, add the header
        if "```{list-table}" not in content:
            content = header

        # Add the new row
        if content.endswith('\n'):  # If there's already content
            content += table_row
        else:  # If we just added the header
            content += table_row

        # Make sure the glossary directory exists
        os.makedirs('glossary', exist_ok=True)

        # Write the updated content
        with open('glossary/index.md', 'w') as f:
            f.write(content)
            return details_link

def kebab_case(s):
    """Convert a string to kebab-case."""
    # Convert to lowercase
    s = s.lower()
    # Replace spaces with hyphens
    s = s.replace(" ", "-")
    # Remove any characters that aren't letters, numbers, or hyphens
    s = "".join(c for c in s if c.isalnum() or c == "-")
    # Remove duplicate hyphens
    s = "-".join(filter(None, s.split("-")))
    return s

import os
import re
import requests
import shutil
from urllib.parse import urlparse
from git import Repo

def clone_github_repo(github_url, project_dir):
    """Clone a GitHub repository to the projects directory"""
    try:
        Repo.clone_from(github_url, project_dir)
        return True
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return False

def download_ipynb(url, filepath):
    """Download an ipynb file from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading notebook: {e}")
        return False

def process_project(page):
    """Process a Project type page and return MyST list table entry"""
    properties = page['properties']
    title = properties['Title']['title'][0]['plain_text'] if properties['Title']['title'] else "Untitled"
    tags = [tag['name'] for tag in properties['Tags']['multi_select']]
    url = properties['URL']['url'] if properties['URL']['url'] else ""
    ipynb = properties.get('ipynb', {}).get('url', '')  # Assuming 'ipynb' is a URL property
    publish = properties.get('publish', {}).get('checkbox', False)

    if not publish:
        return

    # Create projects directory if it doesn't exist
    os.makedirs('projects', exist_ok=True)

    # Initialize variables for links
    details_link = ""
    notebook_link = ""

    # Handle URL and create project page
    # if url:
    #     # Use URL as details link and create project page
    #     details_link = f"[Details]({url})"
    # else:
    #     # Create project page and link to it
    #     details_link = f"[Details]({slug})"

    # Handle ipynb
    if ipynb:
        # Extract repository name for GitHub URLs
        if 'github.com' in ipynb:
            # Parse GitHub URL
            parsed_url = urlparse(ipynb)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Find the base repository URL by taking only owner and repo name
            if len(path_parts) >= 2:
                owner = path_parts[0]
                repo = path_parts[1]
                base_repo_url = f'https://github.com/{owner}/{repo}'
                project_dir = f'projects/{repo}'
                notebook_link = "/".join(path_parts[4:]) if len(path_parts)>3 else ""
                
                # Clone the repository using the base URL
                clone_github_repo(base_repo_url, project_dir)
                    # Find the first ipynb file in the repository
                    # for root, _, files in os.walk(project_dir):
                    #     for file in files:
                    #         if file.endswith('.ipynb'):
                    #             rel_path = os.path.relpath(os.path.join(root, file), 'projects')
                    #             notebook_link = f"[Notebook]({rel_path})"
                    #             break
        else:
            # Download individual notebook
            notebook_filename = f"{kebab_case(title)}.ipynb"
            notebook_path = f"projects/{notebook_filename}"
            if download_ipynb(ipynb, notebook_path):
                notebook_link = f"[Notebook]({notebook_filename})"


def create_glossary_doc_page(page):
    """Create a documentation page for a glossary term if docs property is true"""
    properties = page['properties']
    term = properties['Title']['title'][0]['plain_text'] if properties['Title']['title'] else "Untitled"
    description = properties['Description']['rich_text'][0]['plain_text'] if properties['Description']['rich_text'] else ""
    tags = [tag['name'] for tag in properties['Tags']['multi_select']]
    slug = properties['slug']['rich_text'][0]['plain_text'] if properties['slug']['rich_text'] else kebab_case(term)
    
    # Create the glossary directory if it doesn't exist
    if not os.path.exists('glossary'):
        os.makedirs('glossary')
    
    # Generate filename from term
    filepath = f'glossary/{slug}.md'
    
    # Create page content
    content = f"""
# {term}

## Definition
{description}

## Tags
{', '.join(tags)}

## Additional Notes
"""
    
    # Add blocks content if available
    try:
        blocks = notion.blocks.children.list(page['id'])
        for block in blocks['results']:
            if block['type'] == 'paragraph':
                text = block['paragraph']['rich_text']
                if text:
                    content += text[0]['plain_text'] + '\n\n'
            elif block['type'] == 'heading_2':
                text = block['heading_2']['rich_text']
                if text:
                    content += f"## {text[0]['plain_text']}\n\n"
            elif block['type'] == 'heading_3':
                text = block['heading_3']['rich_text']
                if text:
                    content += f"### {text[0]['plain_text']}\n\n"
            elif block['type'] == 'bulleted_list_item':
                text = block['bulleted_list_item']['rich_text']
                if text:
                    content += f"- {text[0]['plain_text']}\n"
    except Exception as e:
        print(f"Error fetching blocks for {term}: {e}")
    
    # Write the content to the file
    with open(filepath, 'w') as f:
        f.write(content)
    
    return slug

def get_notion_pages(token: str, database_id: str):
    """Get pages from Notion database and process them based on their Type"""
    global notion  # Make notion client available to other functions
    # Initialize the Notion client
    notion = Client(auth=token)
    
    # Query the database with pagination
    pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        response = notion.databases.query(
            database_id=database_id,
            start_cursor=start_cursor
        )
        pages.extend(response['results'])
        has_more = response['has_more']
        start_cursor = response['next_cursor']
    
    # Initialize papers.md if it doesn't exist
    if not os.path.exists('paper-notes/index.md'):
        with open('paper-notes/index.md', 'w') as f:
            f.write("""# Papers Overview

A collection of papers with summaries and quick access links.

## Paper Notes

```{list-table}
:header-rows: 1

* - Title
  - Tags
  - Full Notes 
""")
    

    for page in pages:
        # Get the page type
        properties = page.get('properties', {})
        type_prop = properties.get('Type', {})
        select_prop = type_prop.get('select') if type_prop else None
        page_type = select_prop.get('name') if select_prop else None
        
        if not page_type:
            # Safely get the title with multiple fallbacks
            title_prop = properties.get('Title', {})
            title_list = title_prop.get('title', [])
            if title_list and len(title_list) > 0 and isinstance(title_list[0], dict):
                title = title_list[0].get('plain_text', 'Untitled')
            else:
                title = 'Untitled'
            print(f"Warning: Page has no type: {title}")
            continue
            
        if page_type == "Paper-Notes":
            process_paper_notes(page)
        elif page_type == "Glossary":
            process_glossary(page)
        elif page_type == "Project":
            process_project(page)

# Example usage:
token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("NOTION_DATABASE")
get_notion_pages(token, database_id)
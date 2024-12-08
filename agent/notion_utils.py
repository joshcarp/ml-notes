from typing import Dict, List, Optional
from notion_client import Client
import os

from typing import Dict, List, Optional, Tuple
from notion_client import Client
import os

def get_notion_page(database_id: str,
                    cursor: Optional[str] = None,
                    filter_params: Optional[Dict] = None,
                    sort_params: Optional[List[Dict]] = None) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Fetch a single page from a Notion database with its full content,
    returning the page and a cursor for the next page.
    
    Args:
        database_id (str): The ID of the Notion database to query
        cursor (str, optional): Cursor for pagination from previous call
        filter_params (Dict, optional): Filter parameters for the query
        sort_params (List[Dict], optional): Sort parameters for the query
    
    Returns:
        Tuple[Optional[Dict], Optional[str]]: 
            - The page with its content (or None if no more pages)
            - Cursor for the next page (or None if no more pages)
    """
    
    # Get Notion API key from environment variables
    notion_api_key = os.getenv("NOTION_TOKEN")
    if not notion_api_key:
        raise ValueError("NOTION_TOKEN not found in environment variables")
    
    # Initialize the Notion client
    notion = Client(auth=notion_api_key)
    
    def get_page_content(page_id: str) -> List[Dict]:
        """Helper function to fetch all blocks for a page"""
        blocks = []
        has_more = True
        block_cursor = None
        
        while has_more:
            if block_cursor:
                response = notion.blocks.children.list(
                    block_id=page_id,
                    start_cursor=block_cursor
                )
            else:
                response = notion.blocks.children.list(block_id=page_id)
            
            blocks.extend(response["results"])
            has_more = response["has_more"]
            block_cursor = response.get("next_cursor")
            
        return blocks
    
    # Prepare query parameters
    query_params = {}
    if filter_params:
        query_params["filter"] = filter_params
    if sort_params:
        query_params["sorts"] = sort_params
    if cursor:
        query_params["start_cursor"] = cursor
    
    try:
        # Query the database for the next page
        response = notion.databases.query(
            database_id=database_id,
            page_size=1,  # Only get one page at a time
            **query_params
        )
        
        # If no results, return None for both page and cursor
        if not response["results"]:
            return None, None
        
        # Get the single page from results
        page = response["results"][0]
        
        # Fetch content for the page
        try:
            page["content"] = get_page_content(page["id"])
        except Exception as e:
            print(f"Warning: Failed to fetch content for page {page['id']}: {str(e)}")
            page["content"] = []
        
        # Return the page and the next cursor
        return page, response.get("next_cursor")
                
    except Exception as e:
        raise Exception(f"Error fetching Notion database: {str(e)}")
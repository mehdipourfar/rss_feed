import feedparser

from utils.funcs import time_struct_to_timestamptz


def crawl_and_parse(url):
    parser_result = feedparser.parse(url)
    entries = []

    for entry in parser_result.entries:
        if not all((
                entry.get('title'), entry.get('link'),
                entry.get('summary'), entry.get('published_parsed')
        )):
            # entry has no useful information, so we ignore it
            continue

        images = [
            link['href'] for link in entry.get('links', [])
            if link['rel'] == 'enclosure'
        ]
        image_url = images[0] if images else ''
        publish_date = time_struct_to_timestamptz(
            entry.get('published_parsed')
        )
        entries.append({
            'title': entry.get('title'),
            'link': entry.get('link'),
            'description': entry.get('summary'),
            'category': entry.get('category', ''),
            'author': entry.get('author', ''),
            'image_url': image_url,
            'publish_date': publish_date,
        })

    last_update = time_struct_to_timestamptz(
        parser_result['feed']['updated_parsed']
    )
    channel = {
        'title': parser_result['feed']['title'],
        'description': parser_result['feed']['subtitle'],
        'last_update': last_update,
    }
    return {
        'channel': channel,
        'entries': entries,
    }

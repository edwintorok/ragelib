# ragelib

ragelib is a library for [RAGE](https://github.com/perf101/rage/) to handle parsing and working with pages it generates.

## Prerequisites: Firefox, geckodriver

One of the key features of ragelib is the ability to fetch a rendered graph from RAGE. Graphs are rendered on the client, so this is done using a headless browser using the WebDriver standard. The technology chosen for this is Firefox and geckodriver, communicating with Selenium. Therefore you must have **Firefox** installed, and a release of geckodriver for your platform downloaded from https://github.com/mozilla/geckodriver/releases.

## Installation

Recommended use is with pipenv (`pip install pipenv`):
```
pipenv install -e git+https://github.com/perf101/ragelib.git#egg=ragelib
```

## brief_parser
This module is for parsing the HTML of a RAGE brief report page. It outputs a dictionary `{data_headings, data}` where `data_headings` are the row headings in the input report (ie builds tested), and `data` is defined as a list of row objects of the shape:

```
{
    'title',
    'graph_link', # Link to the graph for this row
    'tds' # Raw <td> elements from the row.
}
```

And where `len(data_headings) === len(tds)`


### Usage
`parsed = brief_parser.ReportParser(html, logger).parse_data()`

## graph_fetcher
This module is for fetching the graphs in a report using headless Firefox. It takes as input a `data` object as returned by `brief_parser`, and the path to look for `geckodriver`. It outputs a new `data` object of the same length with each row annotated with a new field `graph_bytes`:
```
{
    'title', # Unchanged
    'graph_link', # Unchanged
    'tds', # Unchanged
    'graph_bytes' # base64 encoded png screenshot of the rendered graph
}
```

### Usage
`data_with_images = graph_fetcher.ImageFetcher(data, geckodriver_path, logger).fetch_images()`


## brief_rewriter
This module is for writing the data object from `graph_fetcher` into HTML for display to the user. It takes as input the data headings and the data (with images). 

It outputs a HTML document where for each row in the original report we have a table with the data headings and that row's `<td>` elements, followed by the fetched graph for that row as an HTML base64-encoded image. 

### Usage
`html = brief_rewriter.HTMLBodyWriter(data_headings, data_with_images).get_body()` 

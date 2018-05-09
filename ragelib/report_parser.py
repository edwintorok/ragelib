from bs4 import BeautifulSoup

class ReportParser():
    def __init__(self, report_html, logger):
        self.soup = BeautifulSoup(report_html, 'html.parser')
        self.logger = logger

    @staticmethod
    def get_context(tr):
        # Get the context from a row
        return tr('td')[0].text.strip()

    @staticmethod
    def get_description(tr):
        # Get the description from a row
        return tr('td')[1].text.strip()

    @staticmethod
    def get_graph_link(tr):
        # Get the graph link from a row
        return tr.find('a')['href']

    @staticmethod
    def get_data_tds(tr):
        # tds from 3 are data
        return tr('td')[3:]

    def parse_data(self):

        self.logger.debug('Parsing report...')

        # Table rows from the report, including the headers
        all_rows = self.soup('tr')
        
        # The branch headings are in the third row, from column 4 onward.
        data_headings = self.get_data_tds(all_rows[2])

        # The data rows are the rows from row 4 onward (need to keep as a tr for style info for now)
        data_rows = all_rows[3:]
        # The visible rows are the rows in data_rows without style='display:none'
        visible_rows = [row for row in data_rows if 'style' not in row.attrs or not row['style']]
        
        self.logger.info(f"Report contains {len(visible_rows)} rows")
        if len(visible_rows) < len(data_rows):
            self.logger.warning(f"Report contains {len(data_rows) - len(visible_rows)} hidden rows. Freezing the brief report before saving it will make parsing faster.")

        data = [{
            'context': self.get_context(row),
            'title': self.get_description(row),
            'graph_link': self.get_graph_link(row),
            'tds': self.get_data_tds(row)
        } for row in visible_rows]

        self.logger.debug('Report parsed')

        return  {
            'data_headings': data_headings,
            'data': data
        }
class HTMLBodyWriter():
    def __init__(self, data_headings, data_with_images):
        self.data_headings = data_headings
        self.data = data_with_images

    @staticmethod
    def join_cells(tds):
        # Join string representations of the tds
        return ''.join([str(td) for td in tds])


    @staticmethod
    def make_image_element(image_bytes):
        if image_bytes:
            return f"<img src='data:image/png;base64,{image_bytes}' />"
        return ""


    def make_table_element(self, heading_cells, data_cells):
        return f"<table><tr>{self.join_cells(heading_cells)}</tr><tr>{self.join_cells(data_cells)}</tr></table>"


    def write_item(self, item, data_headings):
        return f"<h3>{item['title']}\
                    <small><a href='{item['graph_link']}'>(View in RAGE)</a></small>\
                 </h3>\
                 <div>{self.make_table_element(data_headings, item['tds'])}</div>\
                 <div>{self.make_image_element(item['graph_bytes'])}</div><hr>"


    def get_body(self):
        return '\n'.join([self.write_item(item, self.data_headings) for item in self.data])
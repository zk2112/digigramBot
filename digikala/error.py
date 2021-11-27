from scrapy.exporters import JsonItemExporter

class web ( JsonItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(file,ensure_ascii=False, **kwargs)
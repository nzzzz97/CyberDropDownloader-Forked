import re
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.http.request import Request

import settings


title_setting = settings.include_id_in_download_folder_name


class Erome_Spider(Spider):
    name = 'Erome'

    def __init__(self, *args, **kwargs):
        self.myurls = kwargs.get('myurls', [])
        super(Erome_Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.myurls:
            yield Request(url, self.parse)

    def parse(self, response, **kwargs):
        img_links = response.css('img[class="img-front lasyload"]::attr(data-src)').getall()
        vid_links = response.css('div[class=media-group] div[class=video-lg] video source::attr(src)').getall()

        try:
            title = response.css('div[class="col-sm-12 page-content"] h1::text').get()
            if title_setting:
                title = title + " - " + response.url.split('/')[-1]
        except Exception as e:
            title = response.url.split('/')[-1]
        title = re.sub(r'[/]', "-", title)

        for link in img_links:
            netloc = urlparse(link).netloc.replace('www.', '')
            yield {'netloc': netloc, 'url': link, 'title': title, 'referal': response.url, 'cookies': ''}
        for link in vid_links:
            netloc = urlparse(link).netloc.replace('www.', '')
            yield {'netloc': netloc, 'url': link, 'title': title, 'referal': response.url, 'cookies': ''}
import re
import warnings
import scrapy
import warnings
import pytz
from datetime import datetime
from prag.crawl.items import HideMyAssItem


class HideMyAssSpider(scrapy.Spider):
    name = 'hidemyass'
    allowed_domains = ['proxylist.hidemyass.com']

    def start_requests(self):
        self.scrape_dt = datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc)
        yield scrapy.Request('http://%s/' % self.allowed_domains[0],
                             callback=self.submit_form)

    def submit_form(self, response):
        yield scrapy.FormRequest.from_response(response, formid='proxy-search-form')

    def parse(self, response):
        for row in response.css('#listable > tbody > tr'):
            item = HideMyAssItem()
            item['source'] = self.name
            item['scraped_at'] = self.scrape_dt.isoformat()
            item['updated_at'] = get_update_time(row).isoformat()
            item['country'] = get_column_text(row, 4)
            item['ip_addr'] = get_ip_addr(row)
            item['port'] = int(get_column_text(row, 3))
            item['proto'] = get_column_text(row, 7)
            item['anonimity'] = get_column_text(row, 8).replace(' ', '')
            item['speed_qual'] = get_quality_percent(row, 5)
            item['connect_qual'] = get_quality_percent(row, 6)

            yield item

        for url in response.css('.pagination li a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(url))


def get_column_text(row, col_num):
    return row.xpath('string(td[%d])' % col_num).extract_first().strip().lower()


def get_quality_percent(row, col_num):
    style = row.xpath('td[%d]/div/div[@class="indicator"]/@style' % col_num).extract_first()
    match = re.search(r'width:\s*(\d+)\%', style)
    assert match, 'Invalid indicator style "%s"' % style
    return int(match.group(1))  # returns value from 0 to 100


def get_update_time(row):
    # We postpone import of dateparser just to avoid the below warning
    import ruamel.yaml.error
    warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
    import dateparser

    rel_time_text = get_column_text(row, 1) + ' ago'  # 11secs ago, 1h3m ago, etc
    naive_local_dt = dateparser.parse(rel_time_text)
    posix_ts = int(naive_local_dt.timestamp())
    utc_dt = datetime.utcfromtimestamp(posix_ts).replace(tzinfo=pytz.utc)
    return utc_dt


def get_ip_addr(row):
    text = ''.join(row.xpath('td[2]/*').extract())
    styles = row.xpath('string(td[2]//style)').extract_first()

    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'<style>.*</style>', '', text)  # remove styles
    text = re.sub(r'<div[^>]+style="display:none".*?</div>', '', text)  # remove hidden divs
    text = re.sub(r'<span[^>]+style="display:none".*?</span>', '', text)  # remove hidden spans
    text = re.sub(r'<span>\s*</span>', '', text)  # remove empty spans

    hiding_classes = re.findall(r'\.([^}]+)\s*\{\s*display:\s*none', styles)
    for class_ in hiding_classes:
        text = re.sub(r'<span[^>]+class="%s".*?</span>' % class_, '', text)
        text = re.sub(r'<div[^>]+class="%s".*?</div>' % class_, '', text)

    text = re.sub(r'<[^>]+>', '', text)  # remove tags
    text = re.sub(r'\s+', '', text)  # remove whitespace

    assert re.match(r'^\d{1,3}(\.\d{1,3}){3}$', text), 'Invalid IP address %s' % text
    return text

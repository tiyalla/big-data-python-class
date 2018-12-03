
import scrapy

class amazonItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    resp = scrapy.Field()
class AmazonSpider(scrapy.Spider):
    name = 'amaz'
    allowed_domains = ['https://www.amazon.com/']
    start_urls = ['https://www.amazon.com/books-used-books-textbooks/b/?ie=UTF8&node=283155&ref_=topnav_storetab_b','https://www.amazon.com/gp/browse.html?node=2625373011&ref_=nav_em_T1_0_4_14_1__mov', 'https://www.amazon.com/b/ref=s9_acss_bw_cg_TXTHPCCG_1c1_w?node=468204&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-8&pf_rd_r=F3C0AEBDPSV192J7BNP8&pf_rd_t=101&pf_rd_p=b48a6433-fbec-472a-9c4f-db43997d01de&pf_rd_i=465600']

    def parse(self, response):
        res = scrapy.Selector(response)
        titles = res.xpath('//ul/li')
        items = []
        for title in titles:
            item = nbaItem()
            item["title"] = title.xpath("a/text()").extract()
            item["link"] = title.xpath("a/@href").extract()
            item["resp"] = response
            if item["title"] != []:
                items.append(item)

        return items
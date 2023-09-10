import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class SunnahSpider(scrapy.Spider):
    name = "sunnah"
    allowed_domains = ["sunnah.com"]
    start_urls = ["https://sunnah.com/"]
    rules = [Rule(LinkExtractor(deny = ('/forty', '/bulugh', '/hisn')))]

    def parse(self, response):
        for author_collections in response.xpath("//div[@class='collection_title']/a/@href"):
            print("col: ", author_collections.get())
            if author_collections.get() in ["/forty"]:
                continue
            yield response.follow(author_collections, self.parse_authors)

    def parse_authors(self, response):
        for collection in response.xpath("//div[@class='book_title title']/a/@href"):
            yield response.follow(collection, self.parse_collection)
    
    def parse_collection(self, response):
        for hadith in response.xpath("//div[contains(@class,'actualHadithContainer')]"):

            try:
                hadith_text = hadith.xpath(".//div[@class='english_hadith_full']")

                if hadith_text.xpath("div[@class='hadith_narrated']/text()") and hadith_text.xpath("div[@class='hadith_narrated']/text()").get().strip():
                    narrator = hadith_text.xpath("div[@class='hadith_narrated']/text()").get()
                elif hadith_text.xpath("div[@class='hadith_narrated']/text()") and hadith_text.xpath("div[@class='hadith_narrated']/p/text()").get().strip():
                    narrator = hadith_text.xpath("div[@class='hadith_narrated']/p/text()").get()
                else:
                    narrator = ""

                if hadith_text.xpath("div[@class='text_details']//text()") and hadith_text.xpath("div[@class='text_details']//text()").get().strip():
                    text = hadith_text.xpath("div[@class='text_details']//text()")
                elif hadith_text.xpath("div[@class='text_details']//p//text()") and hadith_text.xpath("div[@class='text_details']//p//text()").get().strip():
                    text = hadith_text.xpath("div[@class='text_details']//p//text()")
                else:
                    print("No hadith text found")
                    continue

                hadith_reference = hadith.xpath(".//table[@class='hadith_reference']")

                author = hadith_reference.xpath("tr[1]/td[2]/a/text()")
                reference = hadith_reference.xpath("tr[2]/td[2]/span/text()")
                if reference == [] and hadith_reference.xpath("tr[2]/td[2]/text()") and hadith_reference.xpath("tr[2]/td[2]/text()").get().strip():
                    reference = hadith_reference.xpath("tr[2]/td[2]/text()")

                if not ((author and author.get().strip()) or (reference and reference.get().strip())):
                    print("No hadith reference found")
                    continue
            except:
                continue
            
            yield {
                "narrator": narrator,
                "text": text.get(),
                "author": ' '.join(author.get().split()[:-1]),
                "reference": reference.get().lstrip("\xa0:\xa0")
            }



    

import scrapy


class SunnahSpider(scrapy.Spider):
    name = "sunnah"
    allowed_domains = ["sunnah.com"]
    start_urls = ["https://sunnah.com/"]

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

            hadith_text = hadith.xpath(".//div[@class='english_hadith_full']")

            if hadith_text.xpath("div[@class='hadith_narrated']/text()"):
                narrator = hadith_text.xpath("div[@class='hadith_narrated']/text()")
            elif hadith_text.xpath("div[@class='hadith_narrated']/p/text()"):
                narrator = hadith_text.xpath("div[@class='hadith_narrated']/p/text()")
            else:
                return

            if hadith_text.xpath("div[@class='text_details']/text()"):
                text = hadith_text.xpath("div[@class='text_details']/text()")
            elif hadith_text.xpath("div[@class='text_details']/p/text()"):
                text = hadith_text.xpath("div[@class='text_details']/p/text()")
            else:
                print("No hadith text found")
                return

            hadith_reference = hadith.xpath(".//table[@class='hadith_reference']")

            author = hadith_reference.xpath("tr[1]/td[2]/a/text()")
            reference = hadith_reference.xpath("tr[2]/td[2]/span/text()")
            if reference == [] and hadith_reference.xpath("tr[2]/td[2]/text()"):
                reference = hadith_reference.xpath("tr[2]/td[2]/text()")

            if not (author or reference):
                print("No hadith reference found")
                print(hadith_reference, author, reference)
                return
            
            yield {
                "narrator": narrator.get().lstrip("\n"),
                "text": text.get().lstrip("\n"),
                "author": ' '.join(author.get().split()[:-1]).lstrip("\n"),
                "reference": reference.get().lstrip("\xa0:\xa0")
            }



    

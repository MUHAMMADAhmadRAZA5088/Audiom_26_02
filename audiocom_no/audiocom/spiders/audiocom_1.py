"""import scrapy Module"""
import scrapy


class Audiocom1Spider(scrapy.Spider):
    '''Spider class'''

    name = "main_scraper"
    allowed_domains = ["www.audiocom.no"]
    start_urls = [
                  "https://www.audiocom.no/bilstereo",
                  "https://www.audiocom.no/batstereo",
                  "https://www.audiocom.no/bobil",
                  "https://www.audiocom.no/hi-fi",
                  "https://www.audiocom.no/sikkerhet",
                  "https://www.audiocom.no/nyheter-og-media",
                  "https://www.audiocom.no/ekstrautstyr"
                  ]


    def parse(self, response):

        anchors = response.xpath("//div[@class='WebPubElement pub-static']/div[contains(@class, 'ArticleWithBackground Layout3Element')]/@data-link").getall()

        if anchors :
            yield from response.follow_all(anchors, callback=self.parse_product)
        
        yield scrapy.Request(response.url, callback=self.parse_product)
        

    def parse_product(self, response):
        
        product_anchors=response.xpath('//div[@class="InfoOverlay"]/div[@class="AddHeaderContainer"]/a/@href').getall()  
        if product_anchors is not None:
            yield from response.follow_all(product_anchors, callback=self.parse_product_scrape, dont_filter=True)
        
        product_small=response.xpath('//div[@class="ProduktDesc"]/a/@href').getall()  
        if product_small is not None:
            yield from response.follow_all(product_small, callback=self.parse_product_scrape, dont_filter=True)
        
        pagination=response.xpath('//a[.=">"]/@href').get()
        if pagination is not None:
            yield response.follow(pagination, callback=self.parse_product,)
        
        car_anchors=response.xpath("//div[@class='WebPubElement pub-static']/div[contains(@class, 'ArticleWithBackground Layout3Element')]/@data-link").getall()
        if car_anchors is not None:
            yield from response.follow_all(car_anchors, callback=self.parse_product, )


    def parse_product_scrape(self, response):

        product_images = []
        file_pdf = []
        
        images = response.xpath('//div[@class="product-image-container"]/div/img/@data-rsbigimg').getall()
        
        for count in range(0,17):
            
            try:
                product_images.append(images[count].replace('/','https://www.audiocom.no/',1))

            except Exception as ex: 
                product_images.append("")
            
        for pdf in product_images:

            if pdf.endswith(".pdf"):
                file_pdf.append(pdf)

        current=response.xpath(".//div[@class='current-price-container']/span[1]/text()").get()

        try:
            current = current.replace(",-","")

        except:
            current

        old = response.xpath(".//span[@class='OldPriceLabel']/text()").get()

        try:
            old = old.replace(",-","")

        except:
            old

        if current and old:
            discount_price = current
            Actual_price = old

        else:
            Actual_price = current
            discount_price = old

        brand_names = [
            '4 Connect',
            '4 Power',
            '4Connect',
            '4POWER',
            '5 Connect',
            'ACV',
            'ACX',
            'AH',
            'AI-SONIC',
            'Alpine',
            'Alpine',
            'Ampire',
            'Antenne (DAB)',
            'Antenne adapter',
            'Antennepisk',
            'Antennesplitter',
            'Asuka',
            'Audio/Video interface',
            'Audison',
            'Aura',
            'AutoDAB',
            'Axton',
            'BeatSonic',
            'BLACKVUE',
            'Blam',
            'Blam',
            'BLAM',
            'Blaupunkt',
            'BOSS',
            'Boss',
            'Brax',
            'Cadence',
            'Caliber',
            'CarAudio Systems',
            'CDS',
            'Cerwin Vega',
            'Clarion',
            'Comfort Modul',
            'ConnectED',
            'Connection',
            'Connects2',
            'Continental',
            'Crunch',
            'DAB integrering',
            'DAB-antenne',
            'DASHCAM',
            'DD Audio',
            'DEFA',
            'Dension',
            'Diamond Audio',
            'DIRECTOR',
            'Dynamat',
            'EMPHASER',
            'ESX',
            'Eton',
            'Fiamm',
            'Firefly',
            'Focal',
            'FOUR Audio',
            'FOUR Connect',
            'G4Audiio',
            'Garmin',
            'Gladen',
            'GLADEN',
            'Ground  Zero',
            'Ground Zero',
            'Halo',
            'Hardstone',
            'Harman/Kardon',
            'Helix',
            'HELIX Q',
            'Hertz',
            'Hertz Marine',
            'Hifonics',
            'In2digi',
            'JBL',
            'Jensen',
            'JL Audio',
            'JL Audio',
            'JVC',
            'JVC',
            'Kenwood',
            'Kicker',
            'Kicker',
            'Kram Telecom',
            'Kufatec',
            'Lukas',
            'MAGNAT',
            'Match',
            'MB Quart',
            'Metra',
            'MOSCONI',
            'MTX',
            'MTX Audio',
            'MUSWAY',
            'Nextbase',
            'NVX',
            'PAC',
            'PAC',
            'Parrot',
            'PEXMAN',
            'PhoenixGold',
            'Pioneer',
            'Polk Audio',
            'Power',
            'Prime',
            'Punch',
            'Pure',
            'Pyle',
            'QVIA',
            'Renegade',
            'RetroSound',
            'Roberts',
            'Rockford Fosgate',
            'Sangean',
            'Scosche',
            'Sony',
            'Sound Marine',
            'SounDigital',
            'Soundmagus',
            'SoundQubed',
            'SoundQuest',
            'Stinger',
            'Stinger',
            'Strands',
            'TARAMPS',
            'Teleskopantenne',
            'TFT',
            'Toma Carparts',
            'uniDAB',
            'VCAN',
            'Video in motion',
            'Xplore',
            'Xzent',
            'Zenec'
        ]
        
        company_brand = ""   
        heading=  response.xpath(".//h1/text()").get()
        
        for brand in brand_names:
            try:
                if brand.upper() in heading.upper():
                    if brand:
                        company_brand=brand
                        break
            except Exception as ex:
                company_brand=""
        categories=response.xpath('//div[@class="BreadCrumb"]/a/text()').getall()
        categories.pop()
        categories.pop(0)
        product_categories=[]
        for i in range(0,6):
            try:
                product_categories.append(categories[i])
            except:
                product_categories.append("")


        product_Description = response.xpath('//div[@class="ProductInfo"]/div[position() >= 5]').getall()
        
        if product_categories[0].strip() != "BILGUIDE":
            
            response_obj={
                    "product Id" : response.css(".product-number-inner .prd-num-label::text").get(),
                    "Main Category" :product_categories[0].strip(),
                    "Category 1" : product_categories[1].strip(),
                    "Category 2" : product_categories[2].strip(),
                    "Category 3" : "",
                    "Category 4" : "",
                    "Category 5" : "",
                    "Product Brand" : company_brand,
                    "Product Name" : response.xpath(".//h1/text()").get(),
                    "Product Information" : response.xpath(".//h2/text()").get(),
                    "url" : response.url,
                    "Main Price" : Actual_price,
                    "Discount Price" : discount_price,
                    "Product Discription" : product_Description,
                    "file_pdf" : ",".join(file_pdf),
                    "source" : "https://www.audiocom.no/",

                }
            for i in range(1, 18):
                response_obj["Picture {}".format(i)] = product_images[i-1].strip()

            yield response_obj

            
           
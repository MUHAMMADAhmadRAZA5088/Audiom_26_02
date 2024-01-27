"""import scrapy Module"""
import scrapy
import re
import pandas as pd


class Audiocom1Spider(scrapy.Spider):
    '''Spider class'''

    name = "one"
    allowed_domains = ["www.audiocom.no"]
    start_urls = ["https://www.audiocom.no/bilstereo/2000728/h%c3%b8yttalerbrakett-audi-a4-hattehylle-din-165"]


    def parse(self, response):
        
        product_images = []
        file_pdf = []
        
        images = response.xpath('//div[@class="product-image-container"]/div/img/@data-rsbigimg').getall()
        
        for count in range(0,17):
            
            try:
                product_images.append(images[count].replace('/','https://www.audiocom.no/',1))

            except Exception as ex: 
                product_images.append("")
            
        for pdf in product_images:

            if pdf.endswith(".jpg"):
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

        brand_names=[
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
                        company_brand = brand
                        break

            except Exception as ex:
                company_brand = ""

        categories=response.xpath('//div[@class="BreadCrumb"]/a/text()').getall()
        categories.pop()
        categories.pop(0)
        categories.pop(0)
        product_categories=[]
        for i in range(0,6):

            try:
                product_categories.append(categories[i])
            except:
                product_categories.append("")

        product_Description = response.xpath('//div[@class="ProductInfo"]/div[position() >= 5]//text()').getall()
        
        web_data = ''.join(response.xpath('//div[@class="ProductInfo"]/div[position() >= 5]//text()').getall())

        final_brand = []
        final_model = []
        final_years = []
        
        if web_data: 
            
            df = pd.read_csv('C:\\scraper\\car_scraper\\car_models.csv')

            brand_csv = []
            for brand in set(df['Brand']):
                if "audio" not in web_data.lower():
                    if brand in web_data:
                        brand_csv.append(brand.strip())

            model_csv = []
            for model in set(df['Model']):
                if model in web_data:
                    model_csv.append(model)
            
            model_csv  = [item for item in model_csv if len(item.strip()) > 0]
            years = re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(web_data))
            years = set(years)
            final_brand = []
            final_model = []
            final_years = []

            last_brand = []
            last_model = []
            last_years = []
            
            if  brand_csv and model_csv:
                for brands in brand_csv: 
                    brand_df = df[df["Brand"] == brands]
                    
                    for model_df in set(brand_df["Model"]):
                        
                        for models in set(model_csv):
                            if model_df == models:
                                final_model.append(model_df)
                                final_brand.append(brands)

            if brand_csv and final_model == []:
                final_brand.extend(brand_csv)


            if years and  final_model:   
                for count in range(0,len(final_brand)):
                    inner_year = [] 
                    csv_year = df[(df['Brand'] == final_brand[count]) & (df['Model'] == final_model[count] )]
                
                    for  year in years:
                        for df_year in csv_year['Year']:
                            if str(df_year) == year:
                                inner_year.append(year)
                    

                    inner_year  = [item for item in inner_year if len(item.strip()) > 0]
                    try:
                        for year in inner_year:
                            last_brand.append(final_brand[count])
                            last_model.append(final_model[count])
                            last_years.append(year)
                    except :
                        last_brand.append(final_brand[count])
                        last_model.append(final_model[count]) 
                        last_years.append('')

            if last_brand and last_model:
                final_brand.clear()
                final_model.clear()
                final_years.clear()
                final_brand.extend(last_brand)
                final_model.extend(last_model)
                final_years.extend(last_years)

        # print(final_brand)
        # print(final_model)
        # for brand in set(final_brand):
        #     if brand.lower() == "audi":
        #         yield {"url" : response.url}
        
        if final_brand != [] and final_model != [] and final_years != []:
            for index in range(len(final_brand)):
                response_obj={
                        "product Id" : response.css(".product-number-inner .prd-num-label::text").get(),
                        "Main Category" : product_categories[0].strip(),
                        "Category 1" : product_categories[1].strip(),
                        "Category 2" : product_categories[2].strip(),
                        "Category 3" : product_categories[3].strip(),
                        "Category 4" : product_categories[4].strip(),
                        "Category 5" : product_categories[5].strip(),
                        "Product Brand" : company_brand,
                        "Product Name" : response.xpath(".//h1/text()").get(),
                        "Product Information" : response.xpath(".//h2/text()").get(),
                        "Car Brand" : final_brand[index],
                        "Car Model" : final_model[index],
                        "Car Years" : final_years[index],
                        "url" : response.url,
                        "Main Price" : Actual_price,
                        "Discount Price" : discount_price,
                        "Product Discription" : product_Description,
                        "file_pdf" : file_pdf,
                        "source" : "https://www.audiocom.no/",

                    }
                for i in range(1, 18):
                    response_obj["Picture {}".format(i)] = product_images[i-1].strip()

                yield response_obj
            
        
            
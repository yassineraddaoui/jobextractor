import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

from .offre import JobOffer

logger = logging.getLogger(__name__)

def handle_exception(e):
    logger.error(f"An error occurred: {str(e)}")
    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def offer_to_dict(offer):
    return {
        "title": offer.title,
        "link": offer.link,
        "image": offer.image,
        "company": offer.company,
        "sector": offer.sector,
        "location": offer.location,
        "type": offer.type,
        "availability": offer.availability,
        "description": offer.description,
        "source": offer.source,
    }

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def extract_info_from_offer(offer, source):
    o = JobOffer()
    
    if source == "LinkedIn":
        link = offer.find("a")
        o.link = link['href']
        o.image = offer.find("img")['data-delayed-url'] if offer.find("img") else None
        o.title = offer.find("h3").text.strip()
        company_elements = offer.find_all("a")
        o.company = company_elements[1].text.strip() if len(company_elements) > 1 else ""
        o.source = source

    elif source == "Keejob":
        elements = offer.find_all("a")
        o.title = elements[1].text.strip()
        o.link = "https://www.keejob.com" + elements[1]['href']
        o.company = elements[2].text.strip()
        o.image = 'https://www.keejob.com/'+ offer.find("img")['src'] if offer.find("img") else None
        recruiter_link = "https://www.keejob.com" + elements[0]['href']
        set_details_kj(o, recruiter_link)
        o.source = source

    return o

def set_details_kj(o, recruiter_link):
    response = fetch_html_content(recruiter_link)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        details = soup.find_all("div", class_="block_a span12")
        for detail in details:
            sector_info = detail.find("div", class_="span9 content").text
            if "Secteur" in sector_info:
                o.sector = sector_info.split(":")[-1].strip()

@api_view(['GET'])
def linkedin_jobs(request):
    url = "https://www.linkedin.com/jobs/search?keywords=&location=Tunisie&geoId=102134353&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    response = fetch_html_content(url)
    soup = BeautifulSoup(response, 'html.parser')

    offers = []
    job_cards = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")
    
    for offer in job_cards:
        try:
            offers.append(extract_info_from_offer(offer, "LinkedIn"))
        except Exception as e:
            print(f"Error extracting LinkedIn info: {e}")

    offers_data = [offer_to_dict(offer) for offer in offers]
    return Response(offers_data)

@api_view(['GET'])
def keejob_jobs(request):
    url = "https://www.keejob.com/"
    response = fetch_html_content(url)
    soup = BeautifulSoup(response, 'html.parser')

    offers = []
    job_cards = soup.find_all("div", class_="block_white")
    
    for offer in job_cards:
        try:
            if len(offer.find_all("a")) > 2:
                offers.append(extract_info_from_offer(offer, "Keejob"))
        except Exception as e:
            print(f"Error extracting Keejob info: {e}")

    offers_data = [offer_to_dict(offer) for offer in offers]
    return Response(offers_data)


@api_view(['GET'])
def opencarrier_jobs(request):
    url = "https://www.optioncarriere.tn/recherche/emplois?s=&l=Tunisie"
    html_content = fetch_html_content(url)

    if not html_content:
        return Response({'error': 'Failed to fetch HTML content'}, status=500)

    job_offer_list = parse_job_articles(html_content)
    return Response(job_offer_list)

def parse_job_articles(html_content):
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    job_articles = soup.find_all('article', class_='job')
    
    job_offer_list = []
    
    for article in job_articles:
        job_offer = JobOffer(
            titre=article.find('h2').text.strip() if article.find('h2') else "N/A",
            link='https://www.optioncarriere.tn'+article.find('a', href=True)['href'] if article.find('a', href=True) else "N/A",
            company=article.find('p', class_='company').text.strip() if article.find('p', class_='company') else "N/A",
            location=article.find('ul', class_='location').find('li').text.strip() if article.find('ul', class_='location') else "N/A",
            description=article.find('div', class_='desc').text.strip() if article.find('div', class_='desc') else "N/A",
            source='Optioncarriere',
            image = 'https://news.umanitoba.ca/wp-content/uploads/2021/11/Career-Month-3-UM-Today--1200x799.png'
        )
        
        job_offer_list.append(job_offer.to_dict())
    
    return job_offer_list

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize global soup object to prevent multiple requests
URL = "http://donboscoberhampore.in/"

def getSoup(url=URL):
    """
    Fetches and parses the HTML content of the given URL using BeautifulSoup.
    
    Args:
        url (str): The URL to fetch and parse. Defaults to the global URL.
    
    Returns:
        BeautifulSoup object: Parsed HTML content.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

@app.errorhandler(404)
def not_found_error(e):
    """
    Handles 404 errors by returning a JSON response with an error message.

    Args:
        e (HTTPException): The exception instance.

    Returns:
        Response: JSON response with the error message.
    """
    return jsonify({"error": "Resource not found", "message": str(e)}), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Handles 500 errors by returning a JSON response with an error message.

    Args:
        e (HTTPException): The exception instance.

    Returns:
        Response: JSON response with the error message.
    """
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """
    Handles HTTP exceptions by returning a JSON response with an error message.

    Args:
        e (HTTPException): The exception instance.

    Returns:
        Response: JSON response with the error message and description.
    """
    response = e.get_response()
    response.data = jsonify({"error": e.name, "description": e.description}).data
    response.content_type = "application/json"
    return response

@app.errorhandler(Exception)
def handle_generic_exception(e):
    """
    Handles generic exceptions by returning a JSON response with a generic error message.

    Args:
        e (Exception): The exception instance.

    Returns:
        Response: JSON response with the error message.
    """
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "Something went wrong!"}), 500

@app.route("/")
def home():
    """
    Home route that returns a welcome message in JSON format.
    
    Returns:
        Response: JSON response with welcome message and metadata.
    """
    return jsonify({
        "message": "Welcome to the Don Bosco School API!",
        "title": "DBS API",
        "author": "Swastik Bhattacharjee",
        "target": "http://donboscoberhampore.in/"
    }), 200

@app.route("/birthdays", methods=["GET"])
def getBirthdays():
    """
    Fetches and returns the list of student birthdays in JSON format.
    
    Query Parameters:
        tuple (bool): Whether to return the data in tuple format or as formatted strings.
    
    Returns:
        Response: JSON response with the list of student birthdays.
    """
    try:
        soup = getSoup()
        in_tuple = request.args.get("tuple", "true").lower() == "true"
        birthdays = []
        rows = soup.find_all('table', style=lambda x: x and 'text-decoration: none;' in x)
        for row in rows:
            name_tag = row.find('span', id=lambda x: x and x.endswith('name1Label'))
            class_tag = row.find('span', id=lambda x: x and x.endswith('Label3'))
            section_tag = row.find('span', id=lambda x: x and x.endswith('Label4'))
            if name_tag and class_tag and section_tag:
                name = name_tag.text.strip()
                student_class = class_tag.text.strip()
                section = section_tag.text.strip()
                birthdays.append((name, student_class, section) if in_tuple else f"{name} ({student_class} {section})")
        return jsonify({"birthdays": birthdays}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/notices", methods=["GET"])
def getNotices():
    """
    Fetches and returns the list of notices in JSON format.
    
    Returns:
        Response: JSON response with the list of notices.
    """
    return jsonify({"notices": getLinks("ctl00_cph123_DataList1")}), 200

@app.route("/competitionResults", methods=["GET"])
def getCompetitionResults():
    """
    Fetches and returns the list of competition results in JSON format.
    
    Returns:
        Response: JSON response with the list of competition results.
    """
    return jsonify({"competitionResults": getLinks("ctl00_cph123_DataList4")}), 200

@app.route("/housePoints", methods=["GET"])
def getHousePoints():
    """
    Fetches and returns the house points in JSON format.
    
    Returns:
        Response: JSON response with the house points.
    """
    try:
        soup = getSoup()
        house_points = {}
        house_colors = {
            'd62828': 'Red',
            '007a3d': 'Green',
            '003f87': 'Blue',
            'fcd856': 'Yellow'
        }
        spans = soup.select('span[id^="ctl00_cph123_Label"]')
        for span in spans:
            parent_td = span.find_parent('td')
            if parent_td:
                style = parent_td.get('style', '')
                color = next((s.split(':')[1].strip() for s in style.split(';') if 'background-color' in s), None)
                house_name = house_colors.get(color.lstrip('#'))
                if house_name:
                    house_points[house_name] = int(span.text.strip())
        return jsonify({"housePoints": house_points}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/eventLinks", methods=["GET"])
def getEventLinks():
    """
    Fetches and returns the list of event links and their titles in JSON format.
    
    Returns:
        Response: JSON response with the list of event links and titles.
    """
    try:
        soup = getSoup("http://donboscoberhampore.in/events.aspx")
        a_tags = soup.find_all('a')
        base_url = "http://donboscoberhampore.in"
        events = []

        for a_tag in a_tags:
            href = a_tag.get('href')
            span = a_tag.find('span')
            title = span.text.strip() if span else 'No Title'
            if href and href.startswith('/events-'):
                full_url = base_url + href
                events.append({'title': title, 'url': full_url})

        unique_events = list({event['url']: event for event in events}.values())
        events_json = json.dumps(unique_events, indent=4)

        return jsonify({"events": unique_events}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extractEventImages(url):
    """
    Extracts and returns a list of event image URLs from the given URL.
    
    Args:
        url (str): The URL to fetch and parse for event images.
    
    Returns:
        list: A list of unique event image URLs.
    """
    base_url = 'http://donboscoberhampore.in'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [base_url + img_tag.get('src') for img_tag in img_tags if img_tag.get('src') and img_tag.get('src').startswith('/imgs/events/')]
    unique_img_urls = list(set(img_urls))
    return unique_img_urls

@app.route('/eventImages', methods=['GET'])
def getEventImages():
    """
    Fetches and returns the list of event images from the provided URL in JSON format.
    
    Query Parameters:
        url (str): The URL to fetch event images from.
    
    Returns:
        Response: JSON response with the list of event images.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        images = extractEventImages(url)
        return jsonify({"images": images}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getLinks(element_id):
    """
    Extracts and returns the list of links and their titles from a given HTML element ID.
    
    Args:
        element_id (str): The HTML element ID to search for links.
    
    Returns:
        list: A list of dictionaries containing link titles and URLs.
    """
    try:
        soup = getSoup()
        links = []
        container = soup.find(id=element_id)
        if container:
            for link in container.find_all('a', href=True):
                heading_tag = link.find('span', id=lambda x: x and x.endswith('topic1Label'))
                if heading_tag:
                    url = link['href'].strip()
                    url = f"http://donboscoberhampore.in{url}" if url.startswith('/') else url
                    links.append({"title": heading_tag.text.strip(), "url": url})
        return links
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)

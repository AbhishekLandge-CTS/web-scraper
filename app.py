from flask import Flask, request, jsonify
from result_store import get_results, clear_results, store_result
from crochet import setup, wait_for
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from search_scraper.spiders.search import SearchSpider

app = Flask(__name__)
setup()  # initialize Crochet

runner = CrawlerRunner()  # global runner

@wait_for(timeout=30.0)
def run_spider(search_url, query):
    clear_results()
    return runner.crawl(SearchSpider, search_url=search_url, query=query)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    search_url = data.get("search_url")
    query = data.get("query")

    if not search_url or not query:
        return jsonify({"error": "Missing 'search_url' or 'query'"}), 400

    try:
        run_spider(search_url, query)
        return jsonify(get_results())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, request, jsonify
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
# from result_store import get_results, clear_results
# import importlib
# import threading
# from scrapy.crawler import CrawlerRunner
# from twisted.internet import reactor
# from crochet import setup, wait_for

# app = Flask(__name__)
# results = []


# setup()  # initialize Crochet once

# @wait_for(timeout=60.0)
# def run_spider(search_url, query):
#     from search_scraper.spiders.search import SearchSpider  # Import here to avoid circular issues
#     runner = CrawlerRunner()
#     d = runner.crawl(SearchSpider, search_url=search_url, query=query)
#     return d


# @app.route('/scrape', methods=['POST'])
# def scrape():
#     data = request.get_json()
#     search_url = data.get("search_url")
#     query = data.get("query")

#     if not search_url or not query:
#         return jsonify({"error": "Missing 'search_url' or 'query'"}), 400

#     clear_results()

#     try:
#         run_spider(search_url, query)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     return jsonify(get_results())

# # Store scraped items here
# def store_result(item):
#     results.append(item)

# if __name__ == '__main__':
#     app.run(debug=True)


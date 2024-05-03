# from flask import request, jsonify, Blueprint
# from .local_scrape_ebay import extract_ebay_listings_from_file

# bp = Blueprint('routes', __name__)

# @bp.route('/listings', methods=['GET'])
# def listings():
#     # Retrieve query parameters
#     url = request.args.get('url', default='https://www.ebay.com/b/Mens-Hats/52365/bn_738858', type=str)  # Provide a default URL or handle None values appropriately
#     max_listings = request.args.get('max_listings', default=None, type=int)  # Defaults to None if not specified

#     if not url:
#         return jsonify({'error': 'URL is required'}), 400
#     file_path = "Men's Hats for Sale - eBay.html"
#     # Call the scrape function with the parameters
#     results = extract_ebay_listings_from_file(file_path, max_listings)
#     return jsonify(results)

# def configure_routes(app):
#     app.register_blueprint(bp)

from flask import jsonify, Blueprint
from .local_scrape_ebay import extract_ebay_listings_from_file

bp = Blueprint('routes', __name__)

@bp.route('/listings', methods=['GET'])
def listings():
    max_listings = 100  # You can change this as needed
    file_path = "data\Men's Hats for Sale - eBay.html"
    # Call the scrape function with predefined parameters
    results = extract_ebay_listings_from_file(file_path, max_listings)
    return jsonify(results)

def configure_routes(app):
    app.register_blueprint(bp)

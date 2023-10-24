# URL Shortener Service

Goal: Create a URL Shortener Service that takes a url and shortens it with random choice of integers. Using the shortened url will redirect to the original url.

Languages/Frameworks:
Used HTML and Javascript for the interface and Python and Flask for the backend API endpoints.

To setup:
- run python app.py and use the local host https given to get the start page.
- to get the routes, add onto the end of '/' what route like /list or /shorten or /<short_code>

GET /list:
- Should return all the original URL's with their respective shortened URL's in JSON form.

GET /:
- Renders the index.html page.

POST /shorten:
- Shortens the original URL into a shortened version.

/<short_code>:
- Redirects the shortened URL to the original URL.

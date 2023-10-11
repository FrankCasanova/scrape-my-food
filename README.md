# Supermarket Product Scraper

This project is a web scraper that fetches product data from various supermarket websites. It's built with Python and uses the FastAPI framework for the web server.

## Instalation
```bash
pip install -r requirements.txt
```
## Features

The application provides the following endpoints:

- `/mercadona`: Returns a list of products scraped from the Mercadona website.
- `/carrefour`: Returns a list of products scraped from the Carrefour website.
- `/el-jamon`: Returns a list of products scraped from the El Jamón website.
- `/dia`: Returns a list of products scraped from the Día website.
- `/prices`: Returns a list of lists of products scraped from all the above stores.

Each endpoint returns a list of `Product` models. If the scraping process fails, it raises an HTTPException with status code 500.

## Running the Server

To run the server, execute the following command:

```bash
python main.py
```
This will start the server at http://127.0.0.2:8000.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT
Feel free to modify it as per your needs!

Documented by Frank Casanova

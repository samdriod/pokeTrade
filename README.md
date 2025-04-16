# PokeTrade Project

## Project Description

PokeTrade is a platform built with Django and SQLite3 that allows users to trade Pokémon cards. The application uses the Pokémon TCG API to fetch card data, stores this data in a database, and then uses the stored data to power the trading system, enabling users to manage their card listings, make offers, and interact with other traders. The styling of this project is done using Tailwind CSS.

## Features

* **User Authentication:** Users can create accounts, log in, and manage their profiles.
* **Card Listings:** Users can create listings for cards they want to trade.
* **Offer System:** Users can make offers on other users' card listings.
* **Pokémon TCG API Integration:** The application uses the Pokémon TCG API to retrieve card data.
* **Database Storage:** The application uses SQLite3 to store user data, card listings, offers, and Pokémon card data.
* **Data Retrieval and Usage:**

    1.  Fetches card data from the Pokémon TCG API.
    2.  Stores the fetched data in a database.
    3.  Uses the stored data to display and manage card information within the application.

## Technologies Used

* Django: A Python web framework.
* SQLite3: A lightweight database.
* Pokémon TCG API: [https://api.pokemontcg.io/v2/](https://api.pokemontcg.io/v2/)
* Tailwind CSS: For styling.

## API Key

>   **Note:** The API key is not included here for security reasons. You will need to obtain your own API key from the Pokémon TCG API and configure it in your application's settings.

## Database

The project uses SQLite3 as its database. The database file is `db.sqlite3`. The database schema is defined in the `models.py` files within the `accounts`, `listings`, and `offers` apps. The database stores user data, card listings, offers, and Pokémon card data fetched from the API.

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd PokeTrade
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate # On macOS and Linux
    venv\Scripts\activate # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6.  **Access the application in your browser:** [http://localhost:8000/](http://localhost:8000/)

## Running the Application

To run the application:

```bash
python manage.py runserver
```
##Testing

```bash
tests:python manage.py test
```

# 🎓 Don Bosco School API (DBS API)

Welcome to the Don Bosco School API! This API provides various endpoints to fetch information from the Don Bosco School website, including birthdays, notices, competition results, house points, event links, and event images.

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Home](#home)
  - [Birthdays](#birthdays)
  - [Notices](#notices)
  - [Competition Results](#competition-results)
  - [House Points](#house-points)
  - [Event Links](#event-links)
  - [Event Images](#event-images)
- [Author](#author)
- [Credits and Disclaimer](#credits-and-disclaimer)

---

## 🌟 Introduction

The Don Bosco School API allows you to fetch various types of information from the Don Bosco School website. This API is built using Flask and BeautifulSoup to scrape and serve the data in a structured format.

---

## 🛠️ Installation

To install and run the API locally, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/SwastikBhattacharjee/dbs-api.git
    cd dbs-api
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Flask application:**

    ```sh
    flask run
    ```

The API will be available at `http://127.0.0.1:5000`.

---

## 🚀 Usage

You can use tools like `curl`, Postman, or your web browser to interact with the API endpoints. Below are the available endpoints and their usage.

---

## 📚 Endpoints

### 🏠 Home

**Endpoint:** `/`

**Method:** `GET`

**Description:** Returns a welcome message and metadata about the API.

**Example:**

```sh
curl http://127.0.0.1:5000/
```

---

### 🎂 Birthdays

**Endpoint:** `/birthdays`

**Method:** `GET`

**Description:** Fetches and returns the list of student birthdays.

**Query Parameters:**
- `tuple` (optional): Whether to return the data in tuple format or as formatted strings. Default is `true`.

**Example:**

```sh
curl http://127.0.0.1:5000/birthdays
```

---

### 📢 Notices

**Endpoint:** `/notices`

**Method:** `GET`

**Description:** Fetches and returns the list of notices.

**Example:**

```sh
curl http://127.0.0.1:5000/notices
```

---

### 🏆 Competition Results

**Endpoint:** `/competitionResults`

**Method:** `GET`

**Description:** Fetches and returns the list of competition results.

**Example:**

```sh
curl http://127.0.0.1:5000/competitionResults
```

---

### 🏅 House Points

**Endpoint:** `/housePoints`

**Method:** `GET`

**Description:** Fetches and returns the house points.

**Example:**

```sh
curl http://127.0.0.1:5000/housePoints
```

---

### 🔗 Event Links

**Endpoint:** `/eventLinks`

**Method:** `GET`

**Description:** Fetches and returns the list of event links and their titles.

**Example:**

```sh
curl http://127.0.0.1:5000/eventLinks
```

---

### 🖼️ Event Images

**Endpoint:** `/eventImages`

**Method:** `GET`

**Description:** Fetches and returns the list of event images from the provided URL.

**Query Parameters:**
- `url` (required): The URL to fetch event images from.

**Example:**

```sh
curl "http://127.0.0.1:5000/eventImages?url=http://donboscoberhampore.in/events.aspx"
```

---

## 👨‍💻 Author

This API was created by **Swastik Bhattacharjee**. Swastik is a passionate developer with a keen interest in web scraping and API development. You can find more about Swastik on [GitHub](https://github.com/SwastikBhattacharjee).

---

## 📜 Credits and Disclaimer

This API uses data from the [Don Bosco School website](http://donboscoberhampore.in/). All data and content belong to their respective owners. This API is intended for educational and informational purposes only. The author is not affiliated with Don Bosco School and does not claim any ownership of the data provided by the website.

---

Feel free to contribute to this project by submitting issues or pull requests. Happy coding! 🚀


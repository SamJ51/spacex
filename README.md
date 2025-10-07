# SpaceX Dashboard

The project is a Django-based web application that consumes and displays structured data from the SpaceX public API.

## Table of Contents
- Project Features
- Technology Stack
- AI Usage Log
- Local Setup Steps

---

## Project Features

### Core
- Launches Page
- Crew Page
- Payloads Page
- Home Page

### Added Enhancements
- Search Functionality
- Database Caching
- Expandable Card Sections

### Additions
- Added testing for models, views, and populate functions
- Utilised Docker containerisation for application portability

## Technology Stack

| Category         | Tool             | Details
|------------------|--------------------------|------------------------------------------------------------------------|
| Language         | Python 3.13.7-slim       | Slim Python version to help minimise Docker build time.                |
| Containerisation | Docker                   | Allows the application environment to be consistent across systems.    |
| Database         | SQLite                   | A quick and easy-to-set-up database that is ideal for this application.|
| Framework        | Django 5.2.6             | The latest Django version at the time of project initiation.           |
| Library          | requests 2.28.1          | Used to manage HTTP requests.                                          |
| Django Libraries  | Various built-in libraries| Used for purposes like sorting, testing, and time.                     |

---

## AI Usage Log

| Task | AI Model | Chat Link |
|---|---|---|
| Steps for setting a template up in Django | ChatGPT 5 | https://chatgpt.com/share/68e4a8e4-b2a0-800c-adc2-ae86c4425f96 |
| Adding excluded attributes into Launch template | ChatGPT 5 | https://chatgpt.com/share/68e4a957-eec4-800c-9dc4-1d0b85765f4b |
| Creation of the payload template based on the same style and structure as the Launch and Crew templates| ChatGPT 5 | https://chatgpt.com/share/68e4aad7-1050-800c-9f73-323b17f6ccff
| Methods for avoiding image aspect ratios messing up cards | ChatGPT 5 | https://chatgpt.com/share/68e4ac40-3bd4-800c-9067-36bd729a4ada
| Conversion of Payload information to card structure in the same style as the crew page | ChatGPT 5 | https://chatgpt.com/share/68e4ad15-dabc-800c-9caa-c9174e99012a
| Merging of CSS from templates to stylesheet | ChatGPT 5 | https://chatgpt.com/share/68e4ad72-afac-800c-94a5-1b627d7fe3c1
| Conversion of Launch template to a card format in the same style as crew and payload | ChatGPT 5 | https://chatgpt.com/share/68e4adb1-527c-800c-8e43-e753f05d7c08
| CSS for fading an input tag border color | ChatGPT 5 | https://chatgpt.com/share/68e4ae37-d03c-800c-92ad-f4fa91d11a6d
| Bug fix for links and media button | Gemini 2.5 Pro | https://g.co/gemini/share/45692f737045
| Tests for models, population functions, and views | Gemini 2.5 Pro | https://g.co/gemini/share/20513cd4260b |

---

## Local Setup Steps

### 1. Prerequisites
- Git
- Docker

### 2. Clone Repository 

Run `git clone https://github.com/SamJ51/spacex.git`

### 3. Rename Environment File in Root
Run `cp example.env .env`

### 4. Build and Run Docker Containers
Run `docker compose up --build`

### 5. View Website on `http://localhost:8000`

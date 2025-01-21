# CITS5505_Group
UWA CITS5505 Group Project (2024S1)

| UWA ID     | Name                 | GitHub Username  |
|------------|----------------------|------------------|
| 24046428   | Mingyu (Arthur) Lian | Mingyu-Lian      |
| 24035732   | Chensu Yang          | HohhotDog        |
| 24153409   | Longyi (Louie) Su    | LouieSu          |
| 23863688   | Junchen Wang         | wangchunsum      |
# Job Insight
## Introduction

**Job Insight** is a social platform tailored for university students, focusing on sharing interview experiences and career development resources to better prepare for the job market.

## Features and Motivation

### Motivation
University students face numerous challenges when preparing for job interviews and stepping into their careers, often lacking practical experience and guidance. Traditional career hubs have typically provided a static, one-way flow of information, which can feel outdated and impersonal. Many of these platforms lack interactive elements, making it difficult for users to engage meaningfully with the content. Furthermore, they are often not user-friendly, featuring clunky interfaces that are not tailored to the needs of tech-savvy college students.

**Job Insight** aims to bridge this gap by offering a dynamic platform for information sharing, facilitated through interactions between students and alumni. Unlike conventional career resources, Job Insight emphasizes a community-driven approach where both content and support are crowd-sourced and highly interactive. This environment not only enhances the relevance and timeliness of the information but also creates a more engaging user experience. By transforming the way career guidance is delivered, Job Insight aims to empower students with the tools and community support they need to successfully navigate their entry into the workforce.

### Features

- **Interview Experience Sharing**: Users can share their interview experiences, including questions asked, interview processes, and more.
- **Job Information Browsing**: Access up-to-date job postings and internship opportunities from various companies.
- **Bridging Industry Expert & Uni Alumni**: User can engage with community and connect with industry expert or uni alumni to get updated information for their care

## Prerequisites
- Ensure you have Python installed on your machine. This app requires Python 3.8 or newer. 
You can download Python from [Python.org](https://www.python.org/downloads/).
Ensure your computer has the following software installed:
- Python 3.8+
- flask

## Install the required packages:
   pip install -r requirements.txt

## References
- All images used in this project are owned by our team.
- Portions of the code were developed with the assistance of ChatGPT. These sections are appropriately marked within the code.

### Configuration

- Create a `.env` file in the root directory of the project and add the necessary environment variables:
  ```plaintext
  FLASK_APP=run.py
  FLASK_ENV=development

## How to run
- git clone https://github.com/Mingyu-Lian/CITS5505_Group.git
- source venv/bin/activate
- python app.py 
- or flask run
- Open a web browser and go to `http://127.0.0.1:5000` to view the app.

## Testing
- There are several testing files for testing the availablities of the functions of each files inside of app folder including a Selenium testing file and Unit testing fikle.
- Unit test files: Please enter python -m unittest tests/test_xxxx(The name of the file).py to the terminal under virtual environment.
- Selenium Testing files: Just simply enter pytest tests/selenium_test.py in the terminal under virtural environment 

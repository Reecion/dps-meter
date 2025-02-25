
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DPS Meter</h3>

  <p align="center">
    Screenshots based DPS meter for Ashes of Creation log chat.
  </p>

  <h3 align="center">Built With</h3>

  [![Python][Python]][Python-url]
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

There was a need amoung my friends for a DPS meter for Ashes of Creation game. The game does not have currently any addons that could provide that feature and they do not provide any API to do so... at least legally, so I've made a code that would capture a screenshots of specific part of a screen - log chat. Then the screenshot is run through a OCR libarary to detect text, which then is being filtered to provide a sum of damage in that time interval as well as logs which would tell us what ability did how much damage.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Installation

1. Clone the repository
2. Install required dependencies

  ```sh
  pip install -r requirements.txt
  ```
3. Run `main.py`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

When the code is running you can type the command to start some interaction. List of commands:

 - `exit` - Closes the program
 - `start` - Starts dps meter
 - `stop` - Stops dps meter
 - `test` - Shows the screenshot of the area that's being captures
 - `text` - Prints the text that screenshot detects
 - `settings` - Prints current capture region settings
 - `set` - Sets screenshot capture region

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Screenshots -->
## Screenshots

This is how the log chat may look like:

![screenshot-1]

Example DPS meter showing damage:

![screenshot-3]

Example of each skill logs:

![screenshot-4]

Example of all logs:

![screenshot-2]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Attribution

* [Logo Icon](https://www.flaticon.com/free-icon/risk_4334580?related_id=4334580&origin=search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python]: https://img.shields.io/badge/python-3783ed?style=for-the-badge&logo=python&logoColor=ffffff
[Python-url]: https://www.python.org/

[screenshot-1]: images/screenshot_1.jpg
[screenshot-2]: images/screenshot_2.jpg
[screenshot-3]: images/screenshot_3.jpg
[screenshot-4]: images/screenshot_4.jpg
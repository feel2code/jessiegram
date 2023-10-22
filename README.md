<h1 align="center" ><a href="http://jessiegram.ru">🐕JessieGram🐈</a></h1>

![Jessiegram Logo](https://repository-images.githubusercontent.com/485134292/07733572-d11d-4641-8204-39c5aaafb535)

<h4>
    "Jessiegram" is my pet-project about our pets!
    It's a free to signup, you can create posts with your pets,
    comment and like other posts, follow authors which posts you like.
    <br>
    Feel free to use <a href="http://jessiegram.ru">JessieGram</a>!</h4>

## Installation and usage:
Make `.env` file based on example in `.env.example`

Put there all necessary variables for run server

Simply run:
```bash
git clone https://github.com/feel2code/jessiegram.git && cd jessiegram && chmod +x run_server.sh
./run_server.sh
```

## Docker
If you have Docker installed, then you can install and deploy Jessiegram in the easiest way:
```bash
docker pull feel2code/jessiegram:latest && docker run --env-file .env -d -p 80:8000 feel2code/jessiegram
```

<h3 align="center"> Technologies used in this project</h3>
<p align="center">
    <a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" style="height: 35px" alt="Powered by Django." title="Powered by Django." /></a>
    <a href="http://www.djangoproject.com/"><img
                        src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo-shadow.png"
                        style="height: 40px"
                        alt="bootstrap technology"/></a><br>
    <img src="https://img.shields.io/github/license/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="LICENSE">
    <img src="https://img.shields.io/github/contributors/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Contributors">
    <img src="https://img.shields.io/github/repo-size/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Repository Size"> <br>
    <img src="https://img.shields.io/badge/python-3.9-green?style=for-the-badge&logo=appveyor" alt="Python Version">
    <img src="https://img.shields.io/github/issues/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Issues">
    <img src="https://img.shields.io/github/stars/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Stars">
</p>

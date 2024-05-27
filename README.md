<h1 align="center" ><a href="https://github.com/feel2code/jessiegram">🐕JessieGram🐈</a></h1>

![Jessiegram Logo](https://repository-images.githubusercontent.com/485134292/07733572-d11d-4641-8204-39c5aaafb535)

**Jessiegram** is my study-pet-project about pets developed on Django.

## Installation and usage:
Make `.env` file based on example in `.env.example`

### Local deploy
```bash
git clone https://github.com/feel2code/jessiegram.git && cd jessiegram && chmod +x run_server.sh
./run_server.sh
```

### Docker
If you have Docker installed, then you can install and deploy Jessiegram in the easiest way:
```bash
docker pull feel2code/jessiegram:latest && docker run --env-file .env -d -p 80:8000 feel2code/jessiegram
```

<h3 align="center"> Technologies used in this project</h3>
<p align="center">
    <a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" style="height: 37px" alt="Powered by Django." title="Powered by Django." /></a>
    <a href="http://https://getbootstrap.com/"><img src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo-shadow.png" style="height: 40px" alt="bootstrap technology"/></a>
    <a href="https://develop.spacemacs.org"><img alt="Developed with Spacemacs" src="https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg" style="height:37px"/></a>
    <br>
    <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white" alt="Sqlite">
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white" alt="Figma">
    <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" alt="Git">
    <br>
    <img src="https://img.shields.io/badge/python-3.11-green?style=for-the-badge&logo=appveyor" alt="Python Version">
    <img src="https://img.shields.io/github/issues/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Issues">
    <br>
    <img src="https://img.shields.io/github/stars/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Stars">
    <img src="https://img.shields.io/github/repo-size/feel2code/jessiegram?style=for-the-badge&logo=appveyor" alt="Repository Size">
    <br>
</p>


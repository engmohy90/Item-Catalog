## Table of contents

- [Overview](#overview)
- [guide for use](#guide-for-using)
- [What included](#what-included)
- [contant](#contact)

## overview
- this is item category website project based on flask.
- the website is a list of category and its items.
- any one can view wesite.
- only register user can edit or delete items or add new category. 
- only the owner of the item who can delete it or modify on it.
- to run this project follow this guide step by step.

## Guide for using

1 - Install Vagrant and VirtualBox if you have not done so already follow this [link](https://www.udacity.com/wiki/ud197/install-vagrant)<br>
2 - Clone this [repo](https://github.com/engmohy90/udacityP5)<br>
3 - cd to the repo dir where you will find the catalog.py and Vagrantfile<br>
4 - type comand vagrant up and wait till complite <br>
5 - type vagrant ssh comand<br>
6 - cd from ssh to shared dir which is /vagrant/udacityP5<br>
7 - now run the project by comand python catalog.py<br>

## What included

```
├── catalog.db
├── catalog.py
├── README.md
├── static
│   ├── face.jpg
│   ├── login.js
│   ├── main.css
│   ├── main.js
│   ├── signin.png
│   └── signup.js
├── templates
│   ├── base.html
│   ├── delete.html
│   ├── edit.html
│   ├── iteminfo.html
│   ├── items.html
│   ├── login.html
│   ├── mainpage.html
│   ├── newC.html
│   ├── newitem.html
│   ├── profile.html
│   └── signup.html
├── test.py
└── Vagrantfile

```
- catalog.py where flash code writen
- catalog.db where python code using sqlalchemy  to provide the database for the project
- static dir where css and js 
- templates dir where you can find all html  files for the project 
- vagrant files >> configration for vagrent


## contact 
if you have any inquery or any sugestion feel free contact me any time i am always there
<br>
email : engmohy90@gmail.com




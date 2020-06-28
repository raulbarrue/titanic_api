from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = [dcc.Markdown("""
### Intro

This project main objective is to learn how to deliver a machine learning algorithm for "deployment" use.

The reasons to use the Titanic dataset are three:

    1. Simple enough to understand.
    2. Engaging with the users.
    3. It was a long-overdue project. 

 

I have followed this tutorial for the Dash webapp: [Link](https://towardsdatascience.com/how-to-create-an-interactive-dash-web-application-11ea210aa6d9)

---

Questions?
You can reach me out on [Linkedin](https://www.linkedin.com/in/raulbarrue/)

""")]
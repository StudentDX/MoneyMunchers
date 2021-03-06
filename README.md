# PepperMint
## By MoneyMunchers

## Roster:
* David Xiedeng - Project Manager
* Eric Lam - Backend and Database Design
* Vishwaa Sofat - Frontend Design and Database Implementation
* Emory Walsh - Frontend Design and small backend tasks

## Description:
Our project is a budget management application. Users will be able to record their expenses and allot a budget. They can set a budget and our website will tell them if they are saving or overspending. We’ll alert them in instances where they are in danger of going over the budget. Users will be able to see trends in their expenditures over time and how much they have saved.

## [Video Demo](https://youtu.be/ZTnAUi1clLA)

## APIs:
* [Exchange Rates API](https://docs.google.com/document/d/1BDjby5I0kwVJHwZqG5sdHL-vToQsQI_oxhmlBbA87bM/edit)
  * Gives a list of all conversion rates of currencies around the world.
  * Will allow the user to input a different currency than the one they normally use.
* [CanvasJS Graphing API](https://docs.google.com/document/d/1CGVWZKRGY5PUvfaPLchy5yb2WyTaq3vBLx04mmNxk-8/edit)
  * Creates a chart using javascript and HTML
  * Will be used to display trends in the users expenditures over time.

## How to Use:
Create a virtual machine:
```
python3 -m venv <hero>
# <hero> can be replaced with another name
```

Run virtual machine:
```
#to activate
. ~/<hero>/bin/activate

#to deactivate
deactivate
```

Install pip modules:
```
pip install -r ./doc/requirements.txt
```

Run app:
```
python run.py
```

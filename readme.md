Latest version of main branch will be deployed to https://sweng-visualisation.herokuapp.com/

Install virtualenv by:
```pip install virtualenv```

Create a virtualenv:
```virtualenv env```

To start virtual environment for Windows, 
```env\Scripts\activate```  

For Mac and Linux, I think: 
```source env\bin\activate```

If anyone installs any new dependencies, run this command and commit the changes: 
```pip freeze > requirements.txt ```

To install dependencies from requirements.txt file, :
```pip install -r requirements.txt```

To run the server do one of the following
```run server/app.py```

For some this tells you flask module not found, instead try one of the two:
```python -m flask run```
```python3 -m flask run```





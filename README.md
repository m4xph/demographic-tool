# demographic-tool

## Using the tool

You can run the tool with the following steps:
1. Clone GitHub repo ```git clone https://github.com/m4xph/demographic-tool.git```.
2. Install dependencies using ```pip install -r requirements.txt```.
3. Run the Python application using the Python interpreter. ```python main.py``` or ```python3 main.py```
4. Confirm that you would like to use the demographic model.
5. Select your preferred industry by typing the industry name.
6. The demographics estimations will now show up. Confirm if you would like to have recommendations on accessibility measure implementation.
7. The program will show recommendations for accessibility measures.
Optionally, you can use your own demographic data or any self-gathered demographics on your customers to get tailored recommendations for your demographics (see section 5.5.1).

## Configuration & custom data

The data the tool uses can be changed to the needs of individual user needs and use cases. The restructured datasets which contain the underlying data are found within the GitHub repository under the directory data/datasets. New datasets can be added by adding new .json files. There are three kinds of data structures (based on granularity) that new datasets may follow: (1) the dimension-combination structure, with series including age range and gender specification. (2) split dimensions, with age ranges in the series and fixed values for the gender. (3) gender only, with estimations only given for the male and the female population. The documentation on the GitHub page describes how these files should be structured. 
The standard demographics for the different industries can be found in the file data/industry_demographics.json. The demographics in this file can be changed or new industries can be added by creating a new entry in the file. The documentation on the GitHub page describes how this entry should be structured.
Lastly, the model makes use of demographic numbers on the Dutch population to weigh the different age ranges within the demographic estimations. The weights can be adapted by changing the constants in dataset/industry_demographics.py.


### Dataset type (1) dimension-combination structure example
```json
{
  "id": "your-dataset-id",
  "name": "your-dataset-name",
  "link": "source-of-dataset.example",
  "disability": "specific-disability",

  "series": [
    {
      "age_start": 10,
      "age_end": 20,
      "gender": "male",
      "proportion": 1
    },
    {
      "age_start": 21,
      "age_end": 30,
      "gender": "male",
      "proportion": 2
    },
    {
      "age_start": 10,
      "age_end": 20,
      "gender": "female",
      "proportion": 3
    },
    {
      "age_start": 21,
      "age_end": 30,
      "gender": "female",
      "proportion": 4
    }
  ]
}
```

### Dataset type (2) split-dimension structure example
```json

{
  "id": "your-dataset-id",
  "name": "your-dataset-name",
  "link": "source-of-dataset.example",
  "disability": "specific-disability",
  
  "fixed": {
    "gender": {
      "male": 1.0,
      "female": 3.0
    }
  },
  
  "series": [
    {
      "age_start": 10,
      "age_end": 20,
      "proportion": 1
    },
    {
      "age_start": 21,
      "age_end": 30,
      "proportion": 2
    }
  ]
}
```

### Dataset type (3) gender-only structure example
```json

{
  "id": "your-dataset-id",
  "name": "your-dataset-name",
  "link": "source-of-dataset.example",
  "disability": "specific-disability",

  "fixed": {
    "gender": {
      "male": 1.0,
      "female": 3.0
    }
  }
}
```
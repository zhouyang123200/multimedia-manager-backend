# multimedia-manager-backend
multimedia manager backend service
#### 1. How to setup development enviroment
```shell
cd src
python run.py
```
#### 2. Run test cases
```shell
cd src
python -m pytest
```

#### 3. launch flask shell
```shell
cd src
export FLASK_APP=run
python -m flask shell
```

#### 4. access internal swagger api doc service
launch flask service and access endpoint:
```
http://localhost:5000/apidocs/
```
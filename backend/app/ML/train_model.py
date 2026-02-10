import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from ML.preprocessing import preprocess
from sklearn.ensemble import RandomForestRegressor
import pickle

File_path=r'F:\Projects\techathon\backend\app\Data\india_metro_accidents_2000.csv'

df=preprocess(File_path)

X=df.drop("Risk_Score",axis=1)
y=df['Risk_Score']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=15)

model=RandomForestRegressor()

model.fit(X_train,y_train)

y_pred=model.predict(X_test)

#r2_score(y_test,y_pred)

model_path=r'F:\Projects\techathon\backend\app\models\risk_model.pkl'

with open(model_path,'wb') as file:
    pickle.dump(model,file)

print("model train done")

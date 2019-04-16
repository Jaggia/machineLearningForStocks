### Created by Alex Saad-Falcon
# LinearRegression is a machine learning library for linear regression  
from sklearn.linear_model import LinearRegression  
# pandas and numpy are used for data manipulation  
import pandas as pd  
import numpy as np  
# matplotlib and seaborn are used for plotting graphs  
import matplotlib.pyplot as plt  
import seaborn  
# fix_yahoo_finance is used to fetch data  
import fix_yahoo_finance as yf 


# Read data
Df = yf.download('SPY','2008-01-01','2018-04-05')
# Only keep close columns  
Df=Df[['Close']]  
# Drop rows with missing values  
Df= Df.dropna()  
# Plot the closing price of GLD  
# Df.Close.plot(figsize=(10,5))  
# plt.ylabel("Gold ETF Prices")
# plt.show()


Df['S_3'] = Df['Close'].shift(1).rolling(window=3).mean()  
Df['S_9']= Df['Close'].shift(1).rolling(window=9).mean()  
Df= Df.dropna()  
X = Df[['S_3','S_9']]  
X.head()

# Define dependent variable
y = Df['Close']
y.head()


t=.8  
t = int(t*len(Df))  
# Train dataset  
X_train = X[:t]  
y_train = y[:t]  
# Test dataset  
X_test = X[t:]  
y_test = y[t:]  

linear = LinearRegression().fit(X_train,y_train)  
print("Gold ETF Price =", round(linear.coef_[0],2), \
"* 3 Days Moving Average", round(linear.coef_[1],2), \
"* 9 Days Moving Average +", round(linear.intercept_,2))

r2_score = linear.score(X[t:],y[t:])*100 
float("{0:.2f}".format(r2_score)) 
print('r2_score', r2_score)

predicted_price = linear.predict(X_test) 
predicted_price = \
pd.DataFrame(predicted_price,index=y_test.index,columns = ['price']) 
predicted_price.plot(figsize=(10,5)) 
y_test.plot()
plt.legend(['predicted_price','actual_price']) 
plt.ylabel("Gold ETF Price") 
plt.show() 
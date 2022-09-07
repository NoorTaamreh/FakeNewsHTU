import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv("data.csv")

print(data.columns)

data['text'] = data['text'] + ' '+ data['title']
data['length'] = data['text'].apply(lambda x: len(x))

print(data['length'].value_counts().head(90))

X_train, X_test, y_train, y_test = train_test_split(data['text'],data['Flag'], stratify=data['Flag'], test_size=0.1)

tfidf_vectorizer=TfidfVectorizer(use_idf=True, max_df=750)

X_train = tfidf_vectorizer.fit_transform(X_train)
X_test  = tfidf_vectorizer.transform(X_test)

scikit_log_reg = LogisticRegression()
model=scikit_log_reg.fit(X_train,y_train)

print(model.score(X_train, y_train), model.score(X_test, y_test))

print(model.predict(tfidf_vectorizer.transform(["وقال بن بوزيد: ” تنعقد الجمعية العالمية للصحة الافتراضية الـ 74 في سياق هذه الأزمة العالمية التي فرضتها جائحة كوفيد-19 منذ حوالي سنة و نصف، و التي كانت لها عواقب صحية و اقتصادية و اجتماعية بدرجات متفاوتة على جميع دول العالم. و قد كشفت هذه الأزمة ال"])))

import pickle
pickle.dump(model,open('logistic_model.pkl', 'wb'))
pickle.dump(tfidf_vectorizer,open('tfidf.pkl','wb'))
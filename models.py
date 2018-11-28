
import pickle
s = pickle.dumps(clf)
model = pickle.loads(s)
# define one new instance
Xnew = [[varA, varB, varC, varD]]
# make a prediction
ynew = model.predict(Xnew)

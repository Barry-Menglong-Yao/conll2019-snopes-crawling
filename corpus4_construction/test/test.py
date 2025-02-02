from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
def test_decision_tree():
    X, y = make_classification(n_samples=1000, n_features=4,
                           n_informative=2, n_redundant=0,
                           random_state=0, shuffle=False)
    clf = RandomForestClassifier(n_estimators=100, max_depth=2,
                                random_state=0)
    clf.fit(X, y)
 
    print(clf.feature_importances_)
    
    print(clf.predict([[0, 0, 0, 0]]))


test_decision_tree()
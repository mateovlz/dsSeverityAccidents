import pickle, os

def get_prediction(vars, model, url):
    if model == 'clf':
        MODEL = 'model_clf.pickle'
    if model == 'dt':
        MODEL = 'model_dt.pickle'
    # load the model from disk
    loaded_model = pickle.load(open(url+MODEL, 'rb'))
    #result = loaded_model.score(X_test, Y_test)
    result = loaded_model.predict([vars])
    return result[0]

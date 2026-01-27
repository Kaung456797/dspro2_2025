from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class JobAnalyzer:
    def __init__(self, df):
        self.df = df

    def regression(self):
        X = self.df[["skill_count"]]
        y = self.df["salary"]

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)

        return model.coef_[0], model.intercept_, r2, y_pred
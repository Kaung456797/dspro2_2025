import matplotlib.pyplot as plt

def plot_scatter(df):
    plt.figure()
    plt.scatter(df["skill_count"], df["salary"])
    plt.xlabel("Skill Count")
    plt.ylabel("Salary")
    plt.title("Skill Count vs Salary")
    plt.show()

def plot_regression(df, y_pred):
    plt.figure()
    plt.scatter(df["skill_count"], df["salary"])
    plt.plot(df["skill_count"], y_pred)
    plt.xlabel("Skill Count")
    plt.ylabel("Salary")
    plt.title("Regression Analysis")
    plt.show()
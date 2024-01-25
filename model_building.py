from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import warnings
from standardisation import main
warnings.filterwarnings("ignore")


house_price_df = main()


def correlation_matrix_visualization():
    # Correlation matrix to understand feature relationships
    correlation_matrix = house_price_df.drop(['date'], axis=1).corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()


def model_building():
    try:
        # Selecting the features and target variable
        x_features = house_price_df[['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'view', 'condition']]
        y_target = house_price_df['price(in 1000)']

        # Splitting the dataset into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x_features, y_target, test_size=0.2, random_state=42)

        # Building the Linear Regression Model
        model = LinearRegression()

        # Fitting the model on the training data
        model.fit(x_train, y_train)

        # Model Evaluation
        y_prediction = model.predict(x_test)

        # Mean Squared Error and R-squared for model evaluation
        mse = mean_squared_error(y_test, y_prediction)
        r2 = r2_score(y_test, y_prediction)
        return model, y_test, y_prediction
    except Exception as model_building_error:
        print(str(model_building_error))


def model_prediction_visualization():
    # Predictions and Visualization
    _, y_test, y_prediction = model_building()
    plt.scatter(y_test, y_prediction)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Actual Prices vs. Predicted Prices")
    plt.show()


def performance_checker_and_visualization():
    # We can also create a residual plot to check the model's performance
    _, y_test, y_prediction = model_building()
    residuals = y_test - y_prediction
    plt.scatter(y_test, residuals)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("Actual Prices")
    plt.ylabel("Residuals")
    plt.title("Residual Plot")
    plt.show()


if __name__ == "__main__":
    model, _, _ = model_building()

    import pickle

    # Save the trained model to a .pkl file
    with open('./myproject/price_prediction_model/model/linear_regression_model.pkl', 'wb') as file:
        pickle.dump(model, file)

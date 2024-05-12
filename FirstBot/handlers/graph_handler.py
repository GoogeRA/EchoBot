import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np



def create_graph(metric_data):
    # Initialize dictionaries to store values for each category
    # categories = {'Факт': [], 'План': [], 'Прогноз': []}
    #
    # keys = [item for item in categories]
    #
    # # Iterate over keys and metric_data simultaneously
    # for key, data_set in zip(keys, metric_data):
    #     for value, date in data_set:
    #         categories[key].append((value, date))


    # Create empty lists to store data for each metric
    fact_values = []
    fact_dates = []
    plan_values = []
    plan_dates = []
    predict_values = []
    predict_dates = []

    # Extract data from metrics_data
    for metric in metric_data:
        # Unpack value and date from each tuple in the metric list
        for value, date in metric:
            if metric is metric_data[0]:
                fact_values.append(value)
                fact_dates.append(date)
            elif metric is metric_data[1]:
                plan_values.append(value)
                plan_dates.append(date)
            else:
                predict_values.append(value)
                predict_dates.append(date)

    # Convert dates to matplotlib-compatible format
    fact_dates = [date.strftime('%d-%m-%Y') for date in fact_dates]
    plan_dates = [date.strftime('%d-%m-%Y') for date in plan_dates]
    predict_dates = [date.strftime('%d-%m-%Y') for date in predict_dates]

    # Plotting the lines
    plt.figure(figsize=(10, 6))  # Adjust figsize as needed
    plt.plot(fact_dates, fact_values, label='Fact', marker='o')
    plt.plot(plan_dates, plan_values, label='Plan', marker='s')
    plt.plot(predict_dates, predict_values, label='Predict', marker='^')
    plt.xticks(rotation=45)

    # Customize plot
    plt.title('Выбранные показатели')
    plt.xlabel('Дата')
    plt.ylabel('Значение показателя')
    plt.grid(True)
    plt.legend()


# Save the plot to a buffer
    img_buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer

def test_graph():

    # Generate some data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot data on the axis
    ax.plot(x, y, label='sin(x)')

    # Customize plot
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Simple Plot')
    ax.legend()

    # Show the plot
    img_buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return img_buffer




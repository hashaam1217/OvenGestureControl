import panel as pn
import numpy as np
import matplotlib.pyplot as plt

# Generate some data for the plot
x_values = np.linspace(0, 10, 100)
y_values = np.sin(x_values)

# Create a Panel app
def plot_function(freq):
    # Update the plot based on the frequency parameter
    y_updated = np.sin(freq * x_values)

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_values, y_updated, label=f"sin({freq}x)")
    ax.set_title("Interactive Sinusoidal Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()

    # Convert the Matplotlib figure to a Panel object
    return pn.pane.Matplotlib(fig)

# Create a slider widget
frequency_slider = pn.widgets.FloatSlider(name="Frequency", start=0.1, end=5, step=0.1, value=1)

# Combine the slider and the plot
dashboard = pn.Column(
    "# Interactive Sinusoidal Plot",
    frequency_slider,
    pn.bind(plot_function, freq=frequency_slider),
)

# Show the dashboard
dashboard.servable()


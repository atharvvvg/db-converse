import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns # For styling

# Apply a modern, minimal theme once
# sns.set_theme(style="whitegrid", palette="muted")
# Or apply per chart if more control is needed.

def generate_bar_chart_figure(labels, values, title="Bar Chart", xlabel="Categories", ylabel="Values"):
    """Generates a Matplotlib Figure object for a bar chart."""
    fig = Figure(figsize=(5, 4), dpi=100) # Create a Figure
    ax = fig.add_subplot(111) # Add an Axes to the figure

    # Use Seaborn for better aesthetics if desired, or plain Matplotlib
    # sns.barplot(x=labels, y=values, ax=ax, palette="viridis")
    ax.bar(labels, values, color=sns.color_palette("viridis", len(labels)))


    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45) # Rotate x-labels if they are long
    fig.tight_layout() # Adjust layout to prevent labels from overlapping
    return fig 
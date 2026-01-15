import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores, mean_scores, save_path='training_plot.png'):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))

    # Save the plot to a file
    plt.savefig(
        save_path)  # You can customize the filename, format (e.g., 'training_plot.pdf'), and options like dpi=300 for higher resolution

    plt.show(block=False)
    plt.pause(.1)
import matplotlib.pyplot as plt
import seaborn as sns


def plot_threshold_analysis(threshold_data: dict):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    param = threshold_data['parameter']
    values = threshold_data['values']
    payoffs = [r['firm_payoff'] for r in threshold_data['results']]

    ax = axes[0]
    ax.plot(values, payoffs, 'b-', linewidth=2)
    ax.set_xlabel(param)
    ax.set_ylabel('Выигрыш фирмы')
    ax.grid(True, alpha=0.3)

    for threshold in threshold_data['threshold']['thresholds']:
        ax.axvline(threshold['param_value'], color='r', linestyle='--', alpha=0.5)
        ax.text(threshold['param_value'], max(payoffs) * 0.8,
                f'{threshold["from_strategy"]}->{threshold["to_strategy"]}',
                rotation=90, color='red')

    ax = axes[1]
    strategies = [1 if r['equilibrium'][0] == 'x_high' else 0 for r in threshold_data['results']]
    ax.fill_between(values, 0, strategies, alpha=0.5, step='mid')
    ax.set_xlabel(param)
    ax.set_ylabel('Стратегия фирмы (1=x_high, 0=x_low)')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['x_low', 'x_high'])
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

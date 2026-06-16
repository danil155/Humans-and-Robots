import sys
import json
from pathlib import Path
from datetime import datetime

import matplotlib

sys.path.insert(0, str(Path(__file__).parent))

from domain.models import ProductionParams, GameParams
from analysis.clusters import COMPANY_CLUSTERS
from analysis.threshold_analyzer import ThresholdAnalyzer, analyze_all_clusters
from analysis.visualizer import plot_threshold_analysis

matplotlib.use('Qt5Agg')


def run_full_analysis():
    print('\n1. АНАЛИЗ КЛАСТЕРОВ')
    print('-' * 70)
    cluster_results = analyze_all_clusters()

    print('\n2. ДЕТАЛЬНЫЙ АНАЛИЗ ПОРОГОВ')
    print('-' * 70)

    all_thresholds = {}

    for cluster_name, cluster_data in COMPANY_CLUSTERS.items():
        print(f'\n{cluster_data["name"]}:')

        prod = ProductionParams(**cluster_data['production_params'])
        game = GameParams(**cluster_data['game_params'])

        analyzer = ThresholdAnalyzer(prod, game)

        thresholds = {
            'w_h': analyzer.analyze_w_h_threshold(
                game.w_m,
                list(range(30, 201, 10))
            ),
            'fine': analyzer.analyze_fine_threshold(
                list(range(1000, 100001, 5000))
            ),
            'robot_cost': analyzer.analyze_robot_cost_threshold(
                list(range(5, 101, 5))
            )
        }

        all_thresholds[cluster_name] = thresholds

        for param_name, analysis in thresholds.items():
            if analysis['threshold']['total_changes'] > 0:
                for t in analysis['threshold']['thresholds']:
                    print(
                        f'  {param_name}: при {t["param_value"]:.0f} стратегия меняется с {t["from_strategy"]} '
                        f'на {t["to_strategy"]}')
            else:
                strat = analysis['results'][0]['equilibrium'][0]
                print(f'  {param_name}: стратегия стабильна (всегда {strat})')

    print('\n3. ВИЗУАЛИЗАЦИЯ')
    print('-' * 70)

    first_cluster = list(all_thresholds.keys())[0]
    first_analysis = all_thresholds[first_cluster]['fine']

    print(f'Строим график для {COMPANY_CLUSTERS[first_cluster]["name"]} (штраф)...')
    plot_threshold_analysis(first_analysis)

    print('\n4. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ')
    print('-' * 70)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = Path(__file__).parent / 'analysis_results'
    results_dir.mkdir(exist_ok=True)

    full_results = {
        'timestamp': timestamp,
        'cluster_results': cluster_results,
        'thresholds': all_thresholds
    }

    def convert_to_serializable(obj):
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        return obj

    with open(results_dir / f'full_analysis_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(full_results, f, indent=2, ensure_ascii=False, default=convert_to_serializable)

    print(f'Результаты сохранены в: {results_dir / f"full_analysis_{timestamp}.json"}')

    print('\n5. СВОДНАЯ ТАБЛИЦА')
    print('=' * 70)
    print(f'\n{"Кластер":<30} {"Равновесие":<35} {"Прибыль фирмы":>15}')
    print('-' * 80)

    for name, data in cluster_results.items():
        cluster_label = COMPANY_CLUSTERS[name]['name'][:28]
        eq = " → ".join(data['equilibrium'])
        payoff = data['payoffs']['Firm']
        print(f'{cluster_label:<30} {eq:<35} {payoff:>15.2f}')


if __name__ == "__main__":
    run_full_analysis()

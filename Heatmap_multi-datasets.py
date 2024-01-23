#封装
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_combined_heatmap(file_path, limit_data=False, threshold_factor=2, reorder=False, reorder_groups=None, subplot_spacing=0.1, output_path='output_heatmap.pdf'):
    # 读取文件
    data = pd.read_csv(file_path, header=None)

    # 数据处理
    data = data.set_index(0)
    data.index.name = 'Gene'
    datasets = data.iloc[0]
    groups = data.iloc[1]
    samples = data.iloc[2]
    gene_expression = data.iloc[3:]
    gene_expression = gene_expression.apply(pd.to_numeric, errors='coerce')
    data_processed = gene_expression.T
    data_processed['Dataset'] = datasets
    data_processed['Group'] = groups
    data_processed.index = samples
    grouped_averages = data_processed.groupby(['Dataset', 'Group']).mean()
    unique_datasets = grouped_averages.index.get_level_values(0).unique()

    # 创建一个包含所有热图的大画布
    fig, axs = plt.subplots(len(unique_datasets), 1, figsize=(10, len(unique_datasets) * 2 + 1))

    for i, (ax, dataset) in enumerate(zip(axs, unique_datasets)):
        data_to_plot = grouped_averages.xs(dataset).copy()

        # 如果需要调整顺序
        if reorder and reorder_groups:
            for group in reorder_groups:
                if group in data_to_plot.index:
                    data_to_plot = data_to_plot.loc[[group] + [g for g in data_to_plot.index if g != group]]
                    break

        # 如果需要限制数据大小
        if limit_data:
            dataset_mean = data_to_plot.mean().mean()
            threshold = dataset_mean * threshold_factor
            data_to_plot = data_to_plot.clip(upper=threshold)

        sns.heatmap(data_to_plot, cmap='viridis', ax=ax)
        ax.set_ylabel(dataset, rotation=90, labelpad=30)

        if i < len(unique_datasets) - 1:
            ax.set_xlabel('')
            ax.set_xticks([])
        else:
            ax.set_xticklabels(data_to_plot.columns, rotation=90)

        ax.tick_params(axis='y', rotation=0)

    plt.tight_layout(pad=subplot_spacing)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

# 使用示例
create_combined_heatmap(
    file_path='XXX.csv',
    limit_data=True,
    threshold_factor=2,
    reorder=True,
    reorder_groups=['Uninfected', 'Control'],
    subplot_spacing=0.1,
    output_path='XXX.pdf'
)

# 使用示例
create_combined_heatmap(
    file_path='XXX.csv',
    limit_data=True,
    threshold_factor=5,
    reorder= True,
    reorder_groups=['WT.Mock', 'Control'],
    subplot_spacing=0.1,
    output_path='XXX.pdf'
)
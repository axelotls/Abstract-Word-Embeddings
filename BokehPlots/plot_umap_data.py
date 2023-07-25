import pandas as pd
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import Category20, Turbo256
import umap


def interactive_plot(umap_embedding_df, words_to_highlight=None, splits=None, fn=None):
    datasource = ColumnDataSource(umap_embedding_df)
    # define color mapping
    palette = []
    if words_to_highlight is not None:
        if splits is None:
            l = len(words_to_highlight)
            if 256 > l > 20:
                palette = [Turbo256[i] for i in range(0, 256, int(256/l))][:l]
            elif l <= 20:
                palette = Category20[l]
                words_to_highlight = words_to_highlight[:l]
            else:
                print('too many words to highlight.')
                return
        else:
        
            colors = Category20[20]
            if len(splits) == 3:
                colors = [Category20[20][6], Category20[20][0], Category20[20][4]]
            palette = [0] * len(words_to_highlight)
            start = 0
            for i, end in enumerate(splits):
                palette[start:end] = [colors[i]] * (end - start)
                start = end

    color_mapping = CategoricalColorMapper(factors=words_to_highlight, palette=palette)

    plot_figure = figure(
        title='UMAP projection of word embeddings',
        # plot_width=600,
        # plot_height=600,
        tools=('pan, wheel_zoom, reset')
    )

    plot_figure.add_tools(HoverTool(tooltips="""
    <div>
        <div>
            <span style='font-size: 16px; color: #224499'>Word:</span>
            <span style='font-size: 18px'>@Word</span>
        </div>
    </div>
    """))

    if fn is not None:
        output_file(filename=fn, title='UMAP projection of word embeddings')

    plot_figure.circle(
        'x',
        'y',
        source=datasource,
        color=dict(field='Word', transform=color_mapping),
        line_alpha=0.6,
        fill_alpha=0.6,
        size=7
    )
    if fn is not None:
        save(plot_figure)
    else:
        show(plot_figure)


def generate_umap_embedding(labels, word_embeddings):

    # collapse embeddings to two dimensions
    reducer = umap.UMAP()
    reducer.fit(word_embeddings)
    umap_embedding = reducer.transform(word_embeddings)

    # save data to csv
    umap_df = pd.DataFrame(umap_embedding, columns=['x', 'y'])
    umap_df['Word'] = labels
    umap_df.index = labels

    return umap_df

import matplotlib.pyplot as plt
import numpy as np
from palettable.colorbrewer.qualitative import Paired_9 as mycorder
from viroconcom.read_write import read_ecbenchmark_dataset, read_contour
from viroconcom.plot import plot_contour

dataset_chars = ['A', 'B', 'C']
return_periods = [1, 20]
lastname_firstname = ['Wei_Bernt', 'GC_CGS', 'hannesdottir_asta',
                      'haselsteiner_andreas', 'BV', 'mackay_ed',
                      'qiao_chi', 'rode_anna', 'vanem_DirectSampling',
                      'vanem_DirectSamplingsmoothed', 'vanem_IFORM']
styles_for_contribution = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '--', '.-']
colors_for_contribution = mycorder.mpl_colors
for idx in range(3):
        colors_for_contribution.append(colors_for_contribution[8])
legends_for_contribution = ['Contribution 1',
                          'Contribution 2',
                          'Contribution 3',
                          'Contribution 4',
                          'Contribution 5',
                          'Contribution 6',
                          'Contribution 7',
                          'Contribution 8',
                          'Contribution 9, DS',
                          'Contribution 9, DS smoothed',
                          'Contribution 9, IFORM'
                          ]
n_contours_to_analyze = 11


fig, ax = plt.subplots(len(return_periods), len(dataset_chars), sharex='row', sharey='row', figsize=(10, 8))
for (return_period, ax0) in zip(return_periods, ax):
    for (dataset_char, ax1) in zip(dataset_chars, ax0):
        # Load the environmental data.
        file_name = 'datasets/' + dataset_char + '.txt'
        sample_hs, sample_tz, label_hs, label_tz = read_ecbenchmark_dataset(file_name)

        contours_hs = []
        contours_tz = []
        max_hs_on_contour = np.empty(n_contours_to_analyze)
        for i in range(n_contours_to_analyze):
            contribution_nr = i + 1
            if contribution_nr > 9:
                contribution_nr = 9
            folder_name = 'results/exercise-1/participant-' + str(contribution_nr)
            file_name = folder_name + '/' + lastname_firstname[i] + '_dataset_' + \
                        dataset_char + '_' + str(return_period) + '.txt'
            (hs, tz) = read_contour(file_name)
            if i in (7, 8, 9, 10):
                (tz, hs) = read_contour(file_name)
            contours_hs.append(hs)
            contours_tz.append(tz)
            max_hs_on_contour[i] = max(hs[~np.isnan(tz)])

        # Plot the data and the contour.
        # fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax1.scatter(sample_tz, sample_hs, c='black', alpha=0.5, zorder=-2)
        for i in range(n_contours_to_analyze):
            ylim = 1.05 * max([max(max_hs_on_contour), max(sample_hs)])
            plot_contour(contours_tz[i], contours_hs[i],
                         ax=ax1,
                         line_style=styles_for_contribution[i],
                         color=colors_for_contribution[i],
                         upper_ylim=ylim)
        
        ax1.set_rasterization_zorder(-1)
        ax1.set_xlabel(label_tz.capitalize())
        ax1.set_ylabel(label_hs.capitalize())
        ax1.set_title('Dataset ' + dataset_char + ', ' + str(return_period) + '-year contour')
        
lgd = fig.legend(legends_for_contribution, 
           loc='lower center', 
           ncol=6, 
           prop={'size': 8})
fig.tight_layout(rect=(0,0.05,1,1))
plt.savefig('results/e1_overlay_abc.pdf', bbox_inches='tight', bbox_extra_artists=[lgd])
plt.show()


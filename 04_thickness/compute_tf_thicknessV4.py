import numpy as np
import math
import read_proc as atlas_read
import matplotlib.pyplot as plt
import os
import default_fonts
import pandas as pd


def plot_luminance_element(ax, data, i):
    ax.plot(data['x'], data['delta_l_rel'], 'k')
    ax.set_ylim(-30, 0)
    ax.set_xlim(0, 36)
    ax.tick_params(direction='in')
    # ax.set_xlabel(r'$s$ [km]', labelpad=2)
    ax.xaxis.set_ticks(np.arange(0, 36.001, 6))
    ax.yaxis.set_ticks(np.arange(-30, 0.001, 10))
    ax.set_xticklabels([])

    ax2 = ax.twiny()
    ax2.tick_params(direction='in')
    ax2.set_xlim(left=0, right=20.001)
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.tick_top()
    ax2.set_xticklabels([])
    ax2.xaxis.set_ticks(np.arange(0, 20.001, 4))

    if i == 4:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(r'$\Delta L_\mathrm{rel}(t)$ [%]')
    pass


def plot_volume_element(ax, data, i):
    ax.plot(data['x'], data['vol_exp'], 'k', label=r'$d_\mathrm{avg,exp}$')
    ax.plot(data['x'], data['vol_lin'], 'silver', label=r'$d_\mathrm{avg,lin}$')
    ax.set_ylim(0, 0.12)
    ax.set_xlim(0, 36)
    ax.tick_params(direction='in')
    ax.set_xlabel(r'$s$ [km]', labelpad=2)
    ax.xaxis.set_ticks(np.arange(0, 36.001, 6))
    ax.yaxis.set_ticks(np.arange(0, 120.1, 40))

    ax2 = ax.twiny()
    ax2.tick_params(direction='in')
    ax2.set_xlim(left=0, right=20.001)
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.tick_top()
    ax2.set_xticklabels([])
    ax2.xaxis.set_ticks(np.arange(0, 20.001, 4))

    if i == 6:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(r'$V_\mathrm{avg}~[\mathrm{\mu m}^3]$')
        ax.legend(frameon=False)
    pass


def plot_delta_thickness_element(ax, data, i):
    # global ax2

    y_exp = data['d_avg_exp']
    y_lin = data['d_avg_lin']
    y = y_lin - y_exp
    ax.plot(data['x'], y, 'k')
    # ax.plot(data['x'], data['d_avg_lin'], 'silver', label='linear')
    ax.set_ylim(-50, 50)
    ax.set_xlim(0, 36)
    ax.tick_params(direction='in')
    # ax.set_xlabel(r'$s$ [km]', labelpad=2)
    # ax.xaxis.set_ticks(np.arange(0, 36.001, 6))
    # ax.yaxis.set_ticks(np.arange(0, 150.001, 50))
    ax.set_xticklabels([])

    ax2 = ax.twiny()
    ax2.tick_params(direction='in')
    ax2.set_xlim(left=0, right=20.001)
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.tick_top()
    ax2.xaxis.set_ticks(np.arange(0, 20.001, 4))
    ax2.set_xticklabels([])

    if i % 2 == 0:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(r'$\Delta d_\mathrm{avg}$ [nm]')
        # ax.legend(loc='upper left', frameon=False)


def plot_stacked_multiplot(plot_data):
    import default_fonts
    fig = plt.figure()
    ax1 = fig.add_subplot(4, 2, 1)
    plot_thickness_element(ax1, plot_data[1], 1)
    ax2 = fig.add_subplot(4, 2, 2)
    plot_thickness_element(ax2, plot_data[0], 2)

    ax7 = fig.add_subplot(4, 2, 3)
    plot_delta_thickness_element(ax7, plot_data[1], 7)

    ax8 = fig.add_subplot(4, 2, 4)
    plot_delta_thickness_element(ax8, plot_data[0], 8)

    ax3 = fig.add_subplot(4, 2, 5)
    plot_luminance_element(ax3, plot_data[1], 3)
    ax4 = fig.add_subplot(4, 2, 6)
    plot_luminance_element(ax4, plot_data[0], 4)

    ax5 = fig.add_subplot(4, 2, 7)
    plot_volume_element(ax5, plot_data[1], 5)
    ax6 = fig.add_subplot(4, 2, 8)
    plot_volume_element(ax6, plot_data[0], 6)

    fig.subplots_adjust(wspace=0.08, hspace=0.2, left=0.115, right=0.96, top=0.92, bottom=0.07)
    fig.align_ylabels([ax1, ax3, ax5])
    # plt.show()
    plt.savefig('thickness_progression_smooth.pdf', transparent=1)
    plt.close()
    pass


def plot_thickness_element(ax, data, i):
    # global ax2
    ax.plot(data['x'], data['d_avg_exp'], 'k', label=r'$d_\mathrm{avg,exp}$')
    ax.plot(data['x'], data['d_avg_lin'], 'silver', label=r'$d_\mathrm{avg,lin}$')
    ax.set_ylim(0, 150)
    ax.set_xlim(0, 36)
    ax.tick_params(direction='in')
    # ax.set_xlabel(r'$s$ [km]', labelpad=2)
    ax.xaxis.set_ticks(np.arange(0, 36.001, 6))
    ax.yaxis.set_ticks(np.arange(0, 150.001, 50))
    ax.set_xticklabels([])

    ax2 = ax.twiny()
    ax2.tick_params(direction='in')
    ax2.set_xlim(left=0, right=20.001)
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.tick_top()
    ax2.set_xlabel(r'$t$ [h]', labelpad=7)
    ax2.xaxis.set_ticks(np.arange(0, 20.001, 4))

    if i == 2:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(r'$d_\mathrm{avg}$ [nm]')
        ax.legend(loc='upper left', frameon=False)


if __name__ == '__main__':

    test_collection = [(1617, 550207, 0.8782, 0.097793),  # set, id, c_clean, measured thickness
                       (1615, 550200, 0.8134, 0.092416),
                       ]

    # file_collection = ['backup_thicknessdata/550207.xlsx',
    #                    'backup_thicknessdata/550200.xlsx',
    #                    ]
    file_collection = ['-1_smooth.xlsx',
                       '550200_smooth.xlsx',
                       ]

    src_root = '/home/jibachi/PycharmProjects/jbc_tools/data'

    data_collection = []
    for idx_test, temp_test in enumerate(test_collection):
        set_no = temp_test[0]
        idx = temp_test[1]
        c_clean = temp_test[2]
        thickness = temp_test[3]

        df_file = pd.read_excel(file_collection[idx_test])

        file_src = os.path.join(src_root, f'set_{set_no}', f'{idx:08d}.0001.proc')
        df = atlas_read.AtlasData(file_src)

        # delta_l_rel_last = df.data['delta_l_rel'].iloc[-1]/100
        # thickness_last = thickness/c_clean
        # df_delta_l_rel = df.data['delta_l_rel']/100
        # epsilon = calc_epsilon(delta_l_rel=delta_l_rel_last,thickness=thickness_last)
        # d_avg_exp = compute_exponential_thickness_function(delta_l_rel=df_delta_l_rel, epsilon=epsilon)
        # m = calc_linear_degradation_rate(delta_l_rel_last,thickness_last)
        # d_avg_lin = compute_linear_thickness_function(df_delta_l_rel, m)
        # x = df.data['segment_sliding_distance'] / 1000
        volume_exp = df_file['thickness1'] * 4 * 2 * np.pi * 30
        volume_lin = df_file['thickness2'] * 4 * 2 * np.pi * 30
        data_collection.append({'x': df_file['d'] * 1.8,
                                'd_avg_exp': df_file['thickness1'] * 1000,
                                'd_avg_lin': df_file['thickness2'] * 1000,
                                'delta_l_rel': df.data['delta_l_rel'],
                                'vol_exp': volume_exp,
                                'vol_lin': volume_lin,
                                })
    plot_stacked_multiplot(data_collection)

    print()

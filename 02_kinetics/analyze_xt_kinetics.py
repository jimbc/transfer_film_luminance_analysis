import os
import matplotlib.pyplot as plt
import exponential_regression as exp_fit
import pandas as pd
import numpy as np
import my_chisquare


def reduced_chi_square(expected, observed):
    chi2, r2 = my_chisquare.my_chisquare(observed, expected)
    return r2


def plot(x, y):
    ax = plt.subplot(111)
    ax.plot(x, y)
    plt.show()
    plt.close()
    pass


def model_function(t, A, K, C):
    return A * np.exp(K * t) + C


def plot_combined(x_full, y_full, x_expected, y_expected, gof, file_name):
    ax = plt.subplot(111)
    ax.plot(x_full, y_full, label='measured')
    ax.plot(x_expected, y_expected, label='computed')
    ax.legend()

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.09, f'r2={round(gof, 3)}', transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    ax.text(0.05, 0.95, f'x_min={round(x_expected[0], 3)}\nx_max={round(x_expected[-1], 3)}',
            transform=ax.transAxes,
            fontsize=14,
            verticalalignment='top',
            bbox=props)
    # plt.show()
    plt.savefig(file_name)
    # print(f'{file_name} plotted...')
    plt.close()
    pass


def plot_all_fit_from_same_t_init(ax, data_list, input_params, i):
    x_full = data_list[0]['x_full']*1.8
    y_full = data_list[0]['y_full']
    ln1 = ax.plot(x_full, y_full, color='silver', label='measured')
    fit_over_threshold = []
    best_gof = []
    max_width = 0.0
    first_plot=True
    for idx, dict_el in enumerate(data_list):
        if not best_gof:
            best_gof = dict_el
        x_expected = dict_el['x_expected']*1.8
        y_expected = dict_el['y_expected']
        curr_gof = dict_el['gof_corr']
        if curr_gof >= input_params['gof_threshold']:
            if dict_el['x_expected'][-1] - dict_el['x_expected'][0] > max_width:
                fit_over_threshold = dict_el
        elif curr_gof >= best_gof['gof_corr']:
            best_gof = dict_el
        if idx%6 == 0:
            if first_plot:
                ln2 = ax.plot(x_expected, y_expected, color='dimgrey', linestyle='dashed', label='other fits')
                first_plot=False
            else:
                ax.plot(x_expected, y_expected, color='dimgrey', linestyle='dashed', label='other fits')
    if fit_over_threshold:
        x_expected = fit_over_threshold['x_expected']
        y_expected = fit_over_threshold['y_expected']
        set_color = 'red'
        # ax.plot(x_expected, y_expected, color='red')
    else:
        x_expected = best_gof['x_expected']
        y_expected = best_gof['y_expected']
        set_color = 'blue'
    ln3 = ax.plot(x_expected*1.8, y_expected, color='k', label='best fit')

    ax.tick_params(direction='in')
    ax.set_xlim(0,36)
    ax.set_ylim(-35,0)
    ax.xaxis.set_ticks(np.arange(0, 36.001, 6))

    ax2 = ax.twiny()
    ax2.tick_params(direction='in')
    ax2.set_xlim(left=0, right=20.001)
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.tick_top()
    ax2.xaxis.set_ticks(np.arange(0, 20.001, 4))

    if i == 2 or i==4:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel(r'$\Delta L_\mathrm{rel}(x,t)$ [%]')

    if i == 1 or i ==2:
        ax.set_xticklabels([])
    else:
        ax.set_xlabel(r'$s$ [km]')

    if i == 3 or i ==4:
        ax2.set_xticklabels([])
    else:
        ax2.set_xlabel(r'$t$ [h]', labelpad=7)

    if i==2:
        lns = ln1 + ln2 + ln3
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=0, frameon=False)
        # ax.legend([ln1,ln2,ln3],('measured', 'other fits', 'best fit'))
    pass


def plot_four_layer_stacked_multiplot(plot_data, input_params):
    import default_fonts
    fig = plt.figure(figsize=(6.0, 4.0))
    ax1 = fig.add_subplot(2, 2, 1)
    plot_all_fit_from_same_t_init(ax1, plot_data[0], input_params, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    plot_all_fit_from_same_t_init(ax2, plot_data[1], input_params, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    plot_all_fit_from_same_t_init(ax3, plot_data[3], input_params, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    plot_all_fit_from_same_t_init(ax4, plot_data[4], input_params, 4)


    fig.subplots_adjust(hspace=0.1, wspace=0.08, left=0.105, right=0.96, bottom=0.12)
    # plt.show()
    plt.savefig(f'{input_params["test_id"]:08d}_kinetic_eval.pdf', transparent=0)
    plt.close()
    pass


def main(input_params):
    df = pd.read_csv(input_params['input_file_path'], sep='\t', names=['segment_elapsed_time', 'delta_l_rel'])
    t = np.array(df['segment_elapsed_time'])
    l = np.array(df['delta_l_rel'])

    x_step_size = len(t) / 100
    # min_step_size = int(len(t) / 100 * input_params['min_segment_length_percent'])
    resolution_step_size = input_params['step_size_percent']

    res = []
    lower_bound = -1.0

    gof_threshold = input_params['gof_threshold']
    is_last_gof_over_threshold = False
    plot_data = []
    for i in range(0, 100, resolution_step_size):
        if t[int(i * x_step_size)] <= lower_bound:
            continue
        temp_data = []
        for j in range(i + int(input_params['min_segment_length_percent']),
                       101,
                       resolution_step_size):
            t_temp = t[int(i * x_step_size): int(j * x_step_size)]
            l_temp = l[int(i * x_step_size): int(j * x_step_size)]
            t_temp_max = t_temp[-1]
            # tare t_temp for fit
            tara_value = t_temp[0]
            t_temp = t_temp - tara_value
            try:
                a, k, c = exp_fit.exp_fit(t_temp, l_temp)
            except FloatingPointError:
                continue

            y_expected = model_function(t_temp, a, k, c)
            gof_raw = reduced_chi_square(l_temp, y_expected)
            fit_width_bonus = input_params['fit_width_bonus']
            gof_corr = gof_raw + (j - i) / (100 - i) * fit_width_bonus
            if input_params['keep_plots']:
                temp_data.append({'x_full': t,
                                  'y_full': l,
                                  'x_expected': (t_temp + tara_value),  # revert tara for plotting
                                  'y_expected': y_expected,
                                  'gof_raw': gof_raw,
                                  'gof_corr': gof_corr,
                                  'a': round(a, 3),
                                  'k': round(-k, 3),
                                  'c': round(c, 3),
                                  't_init': i,
                                  't_finish': j,
                                  })

            if gof_corr >= gof_threshold:
                if t_temp_max > lower_bound:
                    lower_bound = t_temp_max
                if not is_last_gof_over_threshold:
                    is_last_gof_over_threshold = True
            elif is_last_gof_over_threshold:
                is_last_gof_over_threshold = False

            current_data = [i, j, round(gof_corr, 3), round(a, 3), round(-k, 9), round(c, 3)]
            res.append(current_data)
        plot_data.append(temp_data)
    for i, plot_el in enumerate(plot_data):
        df = pd.DataFrame(plot_el)
        df.to_csv(f"fitted_data/{input_params['test_id']:08d}.{i:02d}.csv")

    plot_four_layer_stacked_multiplot(plot_data, input_params)

    # if input_params['keep_plots']:
    #     plot_four_layer_stacked_multiplot(plot_data, input_params)
        # plot_all_fit_from_same_t_init(temp_data, input_params, i, j)
    # res = pd.DataFrame(res, columns=('t_i', 't_f', 'gof_corr', 'a', 'k', 'c'))
    # res.to_csv(input_params['output_file_path'], sep='\t', index=False)


if __name__ == '__main__':
    DEBUG = 1

    input_params = {}
    if DEBUG:
        import datetime

        print('Debug mode is ACTIVE!!!')
        input_params['test_id'] = 550213
        input_params['segment_id'] = 3
        input_params['width_position'] = 3.0
        input_params['step_size_percent'] = 1
        input_params['gof_threshold'] = 0.92
        input_params['min_segment_length_percent'] = 1
        input_params['keep_plots'] = 1
        input_params[
            'output_file_path'] = '/home/jibachi/Documents/diss_jbc/figures/scripts/kinetics/results/out.csv'
        input_params['output_plot_path'] = r'/home/jibachi/Documents/diss_jbc/figures/scripts/kinetics/results'
        input_params['xlabel'] = '$t$ [h]'
        input_params['ylabel'] = '$\Delta L_\mathrm{rel} [%]$'
        input_params['fit_width_bonus'] = 0.015
        input_params['input_file_path'] = f"/home/jibachi/Documents/diss_jbc/figures/scripts/kinetics/xt_slices/" \
                                          f"{input_params['test_id']}/{input_params['test_id']:08d}.0001.xt." \
                                          f"{input_params['width_position']}"
    else:
        import sys

        input_params['input_file_path'] = sys.argv[1]
        input_params['test_id'] = int(sys.argv[2])
        input_params['segment_id'] = int(sys.argv[3])
        input_params['width_position'] = float(sys.argv[4])
        input_params['step_size_percent'] = int(sys.argv[5])
        input_params['gof_threshold'] = float(sys.argv[6])
        input_params['min_segment_length_percent'] = float(sys.argv[7])
        input_params['keep_plots'] = int(sys.argv[8])
        input_params['output_file_path'] = sys.argv[9]
        input_params['output_plot_path'] = sys.argv[10]
        input_params['xlabel'] = sys.argv[11]
        input_params['ylabel'] = sys.argv[12]
        input_params['fit_width_bonus'] = float(sys.argv[13])

    if DEBUG: time_started = datetime.datetime.now()
    main(input_params)
    if DEBUG: print(f'processed in {datetime.datetime.now() - time_started}')

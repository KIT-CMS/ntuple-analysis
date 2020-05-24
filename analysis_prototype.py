from ntuple_processor import Histogram
from ntuple_processor import dataset_from_artusoutput
from ntuple_processor import Unit
from ntuple_processor import UnitManager
from ntuple_processor import GraphManager
from ntuple_processor import RunManager

from ntuple_config.binning import variables
from ntuple_config.legacy_smhtt_2017.channel_selection import channel_selection
from ntuple_config.legacy_smhtt_2017.file_names import nominal_files
from ntuple_config.legacy_smhtt_2017.process_selection import DY_process_selection, TT_process_selection, VV_process_selection, W_process_selection, ZTT_process_selection, ZL_process_selection, ZJ_process_selection, TTT_process_selection, TTL_process_selection, TTJ_process_selection, VVT_process_selection, VVJ_process_selection, VVL_process_selection, ggH125_process_selection, qqH125_process_selection
from ntuple_config.legacy_smhtt_2017.variations import same_sign, prefiring_variations, mc_tau_es_3prong_variations, mc_tau_es_1prong_variations, mc_tau_es_1prong1pizero_variations, tau_es_3prong_variations, tau_es_1prong_variations, tau_es_1prong1pizero_variations, jet_es_variations, met_unclustered_variations, recoil_resolution_variations, recoil_response_variations, jet_to_tau_fake_variations, mu_fake_es_1prong_variations, mu_fake_es_1prong1pizero_variations, lep_trigger_eff_variations_mt, btag_eff_variations, mistag_eff_variations, ggh_variations, zpt_variations, top_pt_variations

import argparse

import logging
logger = logging.getLogger("")


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Produce shapes for 2017 Standard Model analysis.")

    parser.add_argument(
        "--channels",
        default=[],
        type=lambda channellist: [channel for channel in channellist.split(',')],
        help="Channels to be considered, seperated by a comma without space")

    parser.add_argument(
        "--directory",
        required=True,
        type=str,
        help="Directory with Artus outputs.")

    parser.add_argument(
        "--et-friend-directory",
        type=str,
        default=[],
        nargs='+',
        help=
        "Directories arranged as Artus output and containing a friend tree for et."
    )

    parser.add_argument(
        "--mt-friend-directory",
        type=str,
        default=[],
        nargs='+',
        help=
        "Directories arranged as Artus output and containing a friend tree for mt."
    )

    parser.add_argument(
        "--tt-friend-directory",
        type=str,
        default=[],
        nargs='+',
        help=
        "Directories arranged as Artus output and containing a friend tree for tt."
    )

    parser.add_argument(
        "--em-friend-directory",
        type=str,
        default=[],
        nargs='+',
        help=
        "Directories arranged as Artus output and containing a friend tree for em."
    )

    parser.add_argument(
        "--optimization-level",
        default=2,
        type=int,
        help="Level of optimization for graph merging.")

    parser.add_argument(
        "--num-processes",
        default=1,
        type=int,
        help="Number of processes to be used.")

    parser.add_argument(
        "--num-threads",
        default=1,
        type=int,
        help="Number of threads to be used.")

    parser.add_argument(
        "--skip-systematic-variations",
        default=False,
        type=bool,
        help="Do not produce the systematic variations.")

    parser.add_argument(
        "--output-file",
        required=True,
        type=str,
        help="ROOT file where shapes will be stored.")

    return parser.parse_args()

def main(args):
    # Parse arguments
    channels = args.channels
    directory = args.directory
    friend_directories = {
            'et': args.et_friend_directory,
            'mt': args.mt_friend_directory,
            'tt': args.tt_friend_directory,
            'em': args.em_friend_directory
            }
    optimization_level = args.optimization_level
    processes = args.num_processes
    threads = args.num_threads
    skip_systematic_variations = args.skip_systematic_variations
    if '.root' in args.output_file:
        output_file = args.output_file
        log_file = args.output_file.replace('.root', '.log')
    else:
        output_file = '{}.root'.format(args.output_file)
        log_file = '{}.log'.format(args.output_file)

    # Nominals and useful functions
    nominals = {}
    nominals['2017'] = {}
    nominals['2017']['datasets'] = {}
    nominals['2017']['units'] = {}

    def get_nominal_datasets(channel):
        datasets = dict()
        for key, names in nominal_files.items():
            datasets[key] = dataset_from_artusoutput(
                    key, names, channel + '_nominal', directory, friend_directories[channel])
        return datasets

    def get_nominal_units(channel, datasets):
        return {
                'data' : Unit(
                    datasets['data'],[
                        channel_selection(channel)],
                        [v for v in variables[channel].values()]),
                'ztt' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZTT_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'zl' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZL_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'zj' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZJ_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'ttl' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TT_process_selection(channel),
                        TTL_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'ttt' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TT_process_selection(channel),
                        TTT_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'ttj' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TT_process_selection(channel),
                        TTJ_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'vvl' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        VV_process_selection(channel),
                        VVL_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'vvt' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        VV_process_selection(channel),
                        VVT_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'vvj' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        VV_process_selection(channel),
                        VVJ_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'w' : Unit(
                    datasets['W'], [
                        channel_selection(channel),
                        W_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'ggh' : Unit(
                    datasets['ggH'], [
                        channel_selection(channel),
                        ggH125_process_selection(channel)],
                        [v for v in variables[channel].values()]),
                'qqh' : Unit(
                    datasets['qqH'], [
                        channel_selection(channel),
                        qqH125_process_selection(channel)],
                        [v for v in variables[channel].values()])
                }

    # Step 1: create units and book actions
    for channel in channels:
        nominals['2017']['datasets'][channel] = get_nominal_datasets(channel)
        nominals['2017']['units'][channel] = get_nominal_units(channel, nominals['2017']['datasets'][channel])

    um = UnitManager()

    for channel in channels:
        if channel == 'mt':
            um.book([nominals['2017']['units']['mt'][d] for d in ['data', 'ztt', 'zl', 'zj', 'ttl', 'ttj', 'vvl', 'vvj', 'w']], [same_sign])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ttt', 'vvt', 'ggh', 'qqh']])
            if not skip_systematic_variations:
                um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zl', 'zj', 'ttl', 'ttt', 'ttj', 'vvl', 'vvj', 'vvt', 'w', 'ggh', 'qqh']], [*prefiring_variations, *jet_es_variations, *met_unclustered_variations, *lep_trigger_eff_variations_mt, *btag_eff_variations, *mistag_eff_variations])
                um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'ttt', 'ttl', 'vvl', 'vvt', 'ggh', 'qqh']], [*tau_es_3prong_variations, *tau_es_1prong_variations, *tau_es_1prong1pizero_variations, *mc_tau_es_3prong_variations, *mc_tau_es_1prong_variations, *mc_tau_es_1prong1pizero_variations])
                um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zj', 'zl', 'w', 'ggh', 'qqh']], [*recoil_resolution_variations, *recoil_response_variations])
                um.book([nominals['2017']['units']['mt'][d] for d in ['ttj', 'zj', 'vvj', 'w']], [*jet_to_tau_fake_variations])
                um.book([nominals['2017']['units']['mt']['zl']], [*mu_fake_es_1prong_variations, *mu_fake_es_1prong1pizero_variations])
                um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zl', 'zj']], [*zpt_variations])
                um.book([nominals['2017']['units']['mt'][d] for d in ['ttt', 'ttl', 'ttj']], [*top_pt_variations])
                um.book([nominals['2017']['units']['mt']['ggh']], [*ggh_variations])

    # Step 2: convert units to graphs and merge them
    g_manager = GraphManager(um.booked_units, True)
    g_manager.optimize(optimization_level)
    graphs = g_manager.graphs

    # Step 3: convert to RDataFrame and run the event loop
    r_manager = RunManager(graphs)
    r_manager.run_locally(output_file, processes, threads)


if __name__ == "__main__":
    args = parse_arguments()
    setup_logging('prototype.log', logging.INFO)
    main(args)

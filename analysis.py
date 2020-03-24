from itertools import product

from ntuple_processor import Histogram
from ntuple_processor import dataset_from_nameset
from ntuple_processor import Unit
from ntuple_processor import UnitManager
from ntuple_processor import GraphManager
from ntuple_processor import RunManager

import ntuple_config.legacy_smhtt_2017 as cfg17

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


def main():
    # Define histograms and counts
    # TODO: To be made nicer
    binning = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256]
    hists = [Histogram('m_vis', binning)]

    # Define nominal units
    ntuples_base = '/local/scratch/hdd/gallim/ntuples/'
    friends_base = []
    eras = ['2017']
    channels = ['mt']
    units = {era: {channel: {} for channel in channels} for era in eras}

    units['2017']['mt']['data'] = Unit(
            dataset_from_nameset('data', cfg17.datasets.files['singlemuon'], 'mt_nominal', ntuples_base, friends_base),
            [cfg17.channels.mt], hists)

    dy_dataset = dataset_from_nameset('dy', cfg17.datasets.files['DY'], 'mt_nominal', ntuples_base, friends_base)
    dy_base = [cfg17.channels.mt, cfg17.processes.dy('mt')]
    units['2017']['mt']['ztt'] = Unit(dy_dataset, dy_base + [cfg17.processes.ztt('mt')], hists)
    units['2017']['mt']['zl'] = Unit(dy_dataset, dy_base + [cfg17.processes.zl('mt')], hists)
    units['2017']['mt']['zj'] = Unit(dy_dataset, dy_base + [cfg17.processes.zj('mt')], hists)

    tt_dataset = dataset_from_nameset('tt', cfg17.datasets.files['TT'], 'mt_nominal', ntuples_base, friends_base)
    tt_base = [cfg17.channels.mt, cfg17.processes.tt('mt')]
    units['2017']['mt']['ttt'] = Unit(tt_dataset, tt_base + [cfg17.processes.ttt('mt')], hists)
    units['2017']['mt']['ttj'] = Unit(tt_dataset, tt_base + [cfg17.processes.ttj('mt')], hists)
    units['2017']['mt']['ttl'] = Unit(tt_dataset, tt_base + [cfg17.processes.ttl('mt')], hists)

    vv_dataset = dataset_from_nameset('vv', cfg17.datasets.files['VV'], 'mt_nominal', ntuples_base, friends_base)
    vv_base = [cfg17.channels.mt, cfg17.processes.vv('mt')]
    units['2017']['mt']['vvt'] = Unit(vv_dataset, vv_base + [cfg17.processes.vvt('mt')], hists)
    units['2017']['mt']['vvl'] = Unit(vv_dataset, vv_base + [cfg17.processes.vvl('mt')], hists)
    units['2017']['mt']['vvj'] = Unit(vv_dataset, vv_base + [cfg17.processes.vvj('mt')], hists)

    units['2017']['mt']['w'] = Unit(dataset_from_nameset('w', cfg17.datasets.files['W'], 'mt_nominal', ntuples_base, friends_base),
            [cfg17.channels.mt, cfg17.processes.w('mt')], hists)

    units['2017']['mt']['ggh'] = Unit(
            dataset_from_nameset('ggh', cfg17.datasets.files['ggH'], 'mt_nominal', ntuples_base, friends_base),
            [cfg17.channels.mt, cfg17.processes.ggh('mt')], hists)
    units['2017']['mt']['qqh'] = Unit(
            dataset_from_nameset('qqh', cfg17.datasets.files['qqH'], 'mt_nominal', ntuples_base, friends_base),
            [cfg17.channels.mt, cfg17.processes.qqh('mt')], hists)

    # Book units with variations
    um = UnitManager()
    um.book([units[era][channel][name] for era, channel, name in
        product(['2017'], ['mt'], ['data', 'ztt', 'zl', 'zj', 'ttt', 'ttj', 'ttl', 'vvt', 'vvj', 'vvl', 'w', 'ggh', 'qqh'])])
    um.book([units[era][channel][name] for era, channel, name in
        product(['2017'], ['mt'], ['data', 'ztt', 'zl', 'zj', 'ttt', 'ttj', 'ttl', 'vvt', 'vvj', 'vvl', 'w', 'ggh', 'qqh'])],
        [cfg17.variations.same_sign])
    um.book([units[era][channel][name] for era, channel, name in
        product(['2017'], ['mt'], ['ztt', 'zl', 'zj', 'ttl', 'ttt', 'ttj', 'vvl', 'vvj', 'vvt', 'w', 'ggh', 'qqh'])],
        [*cfg17.variations.prefiring,
         *cfg17.variations.jet_es,
         *cfg17.variations.met_unclustered,
         *cfg17.variations.lep_trigger_eff_mt,
         *cfg17.variations.btag_eff,
         *cfg17.variations.mistag_eff])
    um.book([units[era][channel][name] for era, channel, name in
        product(['2017'], ['mt'], ['ztt', 'ttt', 'ttl', 'vvl', 'vvt', 'ggh', 'qqh'])],
        [*cfg17.variations.tau_es_3prong,
         *cfg17.variations.tau_es_1prong,
         *cfg17.variations.tau_es_1prong1pizero,
         *cfg17.variations.mc_tau_es_3prong,
         *cfg17.variations.mc_tau_es_1prong,
         *cfg17.variations.mc_tau_es_1prong1pizero])
    um.book([units[era][channel][name] for era, channel, name in
        product(['2017'], ['mt'], ['ztt', 'zj', 'zl', 'w', 'ggh', 'qqh'])],
        [*cfg17.variations.recoil_resolution,
         *cfg17.variations.recoil_response])
    um.book([units[era][channel][name] for era, channel, name in product(['2017'], ['mt'], ['ttj', 'zj', 'vvj', 'w'])],
        [*cfg17.variations.jet_to_tau_fake])
    um.book([units[era][channel][name] for era, channel, name in product(['2017'], ['mt'], ['zl'])],
        [*cfg17.variations.mu_fake_es_1prong,
         *cfg17.variations.mu_fake_es_1prong1pizero])
    um.book([units[era][channel][name] for era, channel, name in product(['2017'], ['mt'], ['ttt', 'ttl', 'ttj'])],
        [*cfg17.variations.top_pt])
    um.book([units[era][channel][name] for era, channel, name in product(['2017'], ['mt'], ['ggh'])],
        [*cfg17.variations.ggh_theory])

    # Optimize graphs
    g_manager = GraphManager(um.booked_units, True)
    g_manager.optimize(1)
    graphs = g_manager.graphs

    # Run computations
    r_manager = RunManager(graphs)
    r_manager.run_locally('output.root', nworkers=6, nthreads=2)


if __name__ == "__main__":
    setup_logging('analysis.log', logging.INFO)
    main()

import ntuple_config
import ntuple_processor

from ntuple_config.legacy_smhtt_2017.channel_selection import channel_selection
from ntuple_config.legacy_smhtt_2017.queries import data_query, DY_query, tt_query, W_query, HTT_query, VV_query, ZTT_embedded_query, HWW_query, ggHWW_query, qqHWW_query, VH_query, WH_query, ZH_query, ggH_query, qqH_query
from ntuple_config.legacy_smhtt_2017.process_selection import DY_process_selection, TT_process_selection, VV_process_selection, W_process_selection, HTT_process_selection, HWW_process_selection, ZTT_process_selection, ZTT_embedded_process_selection, ZL_process_selection, ZJ_process_selection, TTT_process_selection, TTL_process_selection, TTJ_process_selection, VVT_process_selection, VVJ_process_selection, VVL_process_selection, VH_process_selection, WH_process_selection, ZH_process_selection, ttH_process_selection, ggH125_process_selection, qqH125_process_selection
from ntuple_config.legacy_smhtt_2017.variations import same_sign, prefiring_variations, mc_tau_es_3prong_variations, mc_tau_es_1prong_variations, mc_tau_es_1prong1pizero_variations, tau_es_3prong_variations, tau_es_1prong_variations, tau_es_1prong1pizero_variations, ele_es_variations, ele_es_variations, jet_es_variations, met_unclustered_variations, recoil_resolution_variations, recoil_response_variations, jet_to_tau_fake_variations, ele_fake_es_1prong_variations, ele_fake_es_1prong1pizero_variations, mu_fake_es_1prong_variations, mu_fake_es_1prong1pizero_variations, lep_trigger_eff_variations_mt, lep_trigger_eff_variations_mt_emb, lep_trigger_eff_variations_et, lep_trigger_eff_variations_et_emb, btag_eff_variations, mistag_eff_variations, ggh_variations, zpt_variations, top_pt_variations
from ntuple_processor import Histogram
from ntuple_processor import dataset_from_database
from ntuple_processor import Unit
from ntuple_processor import UnitManager
from ntuple_processor import GraphManager
from ntuple_processor import RunManager

import logging
logger = logging.getLogger("")

import ROOT

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
    db_path = '/home/gallim/KIT/benchmark-reference-shape-producer/datasets/datasets.json'

    #base_dir = '/ceph/htautau/deeptau_eoy/2017/'
    base_dir = '/local/scratch/hdd/gallim/'
    base_file = base_dir + 'ntuples/'
    base_friends = [base_dir + 'friends/' + f for f in ['SVFit/', 'MELA/', 'FakeFactors/']]


    # Hidden
    binning = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256]
    hist = Histogram('m_vis', binning)
    ###

##################################
    channels = ['mt']

    nominals = {}
    nominals['2017'] = {}
    nominals['2017']['datasets'] = {}
    nominals['2017']['units'] = {}

    def get_nominal_datasets(channel):
        datasets = dict()
        nominal_queries = {
                            'data': data_query,
                            'DY': DY_query,
                            'TT': tt_query,
                            'VV': VV_query,
                            'W': W_query,
                            'ggH': ggH_query,
                            'qqH': qqH_query
                            }
        for key, query in nominal_queries.items():
            datasets[key] = dataset_from_database(
                    key, db_path, query, channel + '_nominal', base_file, base_friends)
        return datasets

    def get_nominal_units(channel, datasets):
        return {
                'data' : Unit(
                    datasets['data'],[
                        channel_selection(channel)],
                        [hist]),
                'ztt' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZTT_process_selection(channel)],
                        [hist]),
                'zl' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZL_process_selection(channel)],
                        [hist]),
                'zj' : Unit(
                    datasets['DY'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        ZJ_process_selection(channel)],
                        [hist]),
                'ttl' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TT_process_selection(channel),
                        TTL_process_selection(channel)],
                        [hist]),
                'ttt' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TTT_process_selection(channel)],
                        [hist]),
                'ttj' : Unit(
                    datasets['TT'], [
                        channel_selection(channel),
                        TT_process_selection(channel),
                        TTJ_process_selection(channel)],
                        [hist]),
                'vvl' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        VVL_process_selection(channel)],
                        [hist]),
                'vvt' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        VVT_process_selection(channel)],
                        [hist]),
                'vvj' : Unit(
                    datasets['VV'], [
                        channel_selection(channel),
                        DY_process_selection(channel),
                        VVJ_process_selection(channel)],
                        [hist]),
                'w' : Unit(
                    datasets['W'], [
                        channel_selection(channel),
                        W_process_selection(channel)],
                        [hist]),
                'ggh' : Unit(
                    datasets['ggH'], [
                        channel_selection(channel),
                        ggH125_process_selection(channel)],
                        [hist]),
                'qqh' : Unit(
                    datasets['qqH'], [
                        channel_selection(channel),
                        qqH125_process_selection(channel)],
                        [hist])
                }

    for channel in channels:
        nominals['2017']['datasets'][channel] = get_nominal_datasets(channel)
        nominals['2017']['units'][channel] = get_nominal_units(channel, nominals['2017']['datasets'][channel])

    um = UnitManager()

    for channel in channels:
        if channel == 'mt':
            um.book([nominals['2017']['units']['mt'][d] for d in ['data', 'ztt', 'zl', 'zj', 'ttl', 'ttj', 'vvl', 'vvj', 'w']], [same_sign])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ttt', 'vvt']])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zl', 'zj', 'ttl', 'ttt', 'ttj', 'vvl', 'vvj', 'vvt', 'w', 'ggh', 'qqh']], [*prefiring_variations, *jet_es_variations, *met_unclustered_variations, *lep_trigger_eff_variations_mt, *btag_eff_variations, *mistag_eff_variations])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'ttt', 'ttl', 'vvl', 'vvt', 'ggh', 'qqh']], [*tau_es_3prong_variations, *tau_es_1prong_variations, *tau_es_1prong1pizero_variations, *mc_tau_es_3prong_variations, *mc_tau_es_1prong_variations, *mc_tau_es_1prong1pizero_variations])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zj', 'zl', 'w', 'ggh', 'qqh']], [*recoil_resolution_variations, *recoil_response_variations])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ttj', 'zj', 'vvj', 'w']], [*jet_to_tau_fake_variations])
            um.book([nominals['2017']['units']['mt']['zl']], [*mu_fake_es_1prong_variations, *mu_fake_es_1prong1pizero_variations])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ztt', 'zl', 'zj']], [*zpt_variations])
            um.book([nominals['2017']['units']['mt'][d] for d in ['ttt', 'ttl', 'ttj']], [*top_pt_variations])
            um.book([nominals['2017']['units']['mt']['ggh']], [*ggh_variations])
            um.book([nominals['2017']['units']['mt']['qqh']])

    g_manager = GraphManager(um.booked_units, True)
    #g_manager.optimize(0)
    #g_manager.optimize(1)
    g_manager.optimize(2)
    graphs = g_manager.graphs

    #r_manager = RunManager(graphs, True, 32)
    r_manager = RunManager(graphs)
    r_manager.run_locally('prototype.root')



if __name__ == "__main__":
    setup_logging('prototype.log', logging.INFO)
    main()

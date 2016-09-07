import ROOT
import shutil
import os
import logging
logging.basicConfig()
log = logging.getLogger('stitch')
log.setLevel(logging.INFO)

__all__ = [
    'update_file',
    'stitched_syst',
    'get_categories'
]

def get_categories(file_name):
    rfile = ROOT.TFile(file_name, 'read')
    keys = [k for k in rfile.GetListOfKeys()]
    cats = []
    for k in keys:
        if isinstance(k.ReadObj(), ROOT.TDirectoryFile):
            cats.append(k.GetName())
    return cats



def name_lookup(category, np_name, var='high'):

    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    cache_path = os.path.join(dir_name, '../cache')
    if np_name == 'fake_contamination':
        file_name = os.path.join(cache_path, 'fake_contamination.root')
        if 'vbf' in category:
            if var == 'high':
                hist_name = 'fake_contamination_up_vbf'
            else:
                hist_name = 'fake_contamination_do_vbf'
        else:
            if var == 'high':
                hist_name = 'fake_contamination_up_boost'
            else:
                hist_name = 'fake_contamination_do_boost'
            
    elif np_name == 'fake_extrapolation':
        file_name = os.path.join(cache_path, 'fake_extrapolation.root')
        if var == 'high':
            hist_name = 'fake_extrapolation_up'
        else:
            hist_name = 'fake_extrapolation_do'
    return file_name, hist_name


def fancy_clone(h, ext='clone'):
    hnew = h.Clone()
    hnew.SetName(h.GetName() + '_' + ext)
    hnew.SetTitle(h.GetTitle())
    hnew.GetXaxis().SetTitle(h.GetXaxis().GetTitle())
    hnew.GetYaxis().SetTitle(h.GetYaxis().GetTitle())
    return hnew

def make_var_hist(h, ratio_h):
    hvar = fancy_clone(h, 'var')
    if h.GetNbinsX() != ratio_h.GetNbinsX():
        log.error('nominal binning is {0}, ratio binning is {1}.'.format(
                h.GetNbinsX(), ratio_h.GetNbinsX()))
        raise ValueError('wrong binning')
    # should also check the edges
    for ibin in range(0, h.GetNbinsX() + 2):
        hvar.SetBinContent(ibin, h.GetBinContent(ibin) * ratio_h.GetBinContent(ibin))
    return hvar

def stitched_syst(
    hnom, r_high, r_low, 
    np_name='fake_extrap'):

    h_high = make_var_hist(hnom, r_high)
    h_high.SetName(np_name + '_high')

    h_low = make_var_hist(hnom, r_low)
    h_low.SetName(np_name + '_low')
    return h_high, h_low


def update_file(file_name, category, np_name, sample='Fake'):
    syst_file, name_high = name_lookup(
        category, np_name)
    _, name_low = name_lookup(
        category, np_name, var='low')
    ratio_file = ROOT.TFile(syst_file, 'read')
    r_high = ratio_file.Get(name_high)
    r_low = ratio_file.Get(name_low)
    ws_input_file = ROOT.TFile(file_name, 'update')
    hnom = ws_input_file.Get('{0}/{1}/nominal'.format(
            category, sample))
    h_high, h_low = stitched_syst(
        hnom, r_high, r_low,
        np_name=np_name)
    
    ws_input_file.cd('{0}/{1}'.format(
            category, sample))
    h_high.Write()
    h_low.Write()
    ws_input_file.Close()

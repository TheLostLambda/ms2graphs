import pandas as pd
from classes import Bio_Graph as BG
from classes import Helper_Funcs as hfunc
import decimal as dec
import networkx as nx
from classes import Byspec_Reader as BR
from classes import Charge_Mono_Caller as CMC


TestNL = r"C:\Users\Hyperion\Documents\GitHub\ms2_graph_tool\Test molecule NL.txt"
TestEL = r"C:\Users\Hyperion\Documents\GitHub\ms2_graph_tool\Test molecule EL.txt"
mass_table = r"C:\Users\Hyperion\Documents\GitHub\ms2_graph_tool\masses_table.csv"
mod_table = r"C:\Users\Hyperion\Documents\GitHub\ms2_graph_tool\mods_table.csv"
hf = hfunc.Helper_Funcs(TestNL,TestEL)
nodes_from_file = hf.nodes_df()
edges_from_file = hf.edges_df()
mass_dict = hf.generate_dict(dict_table_filepath=mass_table)
mod_dict = hf.generate_dict(dict_table_filepath=mod_table)



# test_graph = BG.Bio_Graph(nodes_from_file,edges_from_file,mass_dict,mod_dict)
# mg1 = test_graph.construct_graph()
# test_graph.draw_graph(mg1)

# output = test_graph.fragmentation(mg1,cut_limit=3)

# l1,l2,l3 = test_graph.sort_fragments(output)

# nlist = test_graph.monoisotopic_mass_calculator(graph_fragments=output,graph_IDs=l1)
# clist = test_graph.monoisotopic_mass_calculator(graph_fragments=output,graph_IDs=l2)
# ilist = test_graph.monoisotopic_mass_calculator(graph_fragments=output,graph_IDs=l3)
# enabled = ['y']
# mzlist_graph = test_graph.generate_mass_to_charge_masses(nlist,clist,ilist,enabled_ions=enabled,charge_limit=2)

# print(mzlist_graph)

data_file = r"C:\Users\ankur\Documents\MS Data\OT_190122_APatel_Efaecalis_EnpA_10mAU.raw.byspec2"
molecule_library = BG.Bio_Graph(nodes_from_file,edges_from_file,mass_dict,mod_dict)

def calculate_ppm_tolerance(mass,ppm_tol):
    return (mass*ppm_tol) / 1000000

def autosearch(intact_ppm_tol:str = '10', frag_ppm:str = '20'):
    molecules = {}
    molecule_IDs = []
    frag_structure = []
    matched_output = []


    NN_SIMPLE_CHARGE_WEIGHTS = r"C:\Users\Hyperion\Documents\Code\FOUR_APEX_OLD\Models\simple_weights.nn"
    NN_MONO_WEIGHTS = r"C:\Users\Hyperion\Documents\Code\FOUR_APEX_OLD\Models/"
    charge_mono_caller = CMC.Charge_Mono_Caller(NN_SIMPLE_CHARGE_WEIGHTS, NN_MONO_WEIGHTS)
    byspec_reader = BR.Byspec_Reader(data_file)
    scan_mz_charges = byspec_reader.get_scan_mz_charge()
    i_ppm = dec.Decimal(intact_ppm_tol)
    f_ppm = dec.Decimal(frag_ppm)

    master_graph = molecule_library.construct_graph()

    for components in nx.connected_components(master_graph):
        molecule = nx.subgraph(master_graph,components)
        molecule_hash = molecule_library.graph_hash(molecule)
        molecule_IDs.append(molecule_hash)
        molecules.update({molecule_hash:molecule}) 

    molecule_momo_mass = molecule_library.monoisotopic_mass_calculator(molecules,molecule_IDs)

    for (mass,graph_ID) in molecule_momo_mass:
        scans_to_search = []
        upper_mass_lim = mass[0] + calculate_ppm_tolerance(mass[0],i_ppm)
        lower_mass_lim = mass[0] - calculate_ppm_tolerance(mass[0],i_ppm)

        for scan_mz_charge_tuple in scan_mz_charges:
            scan = byspec_reader.get_scan_by_scan_number(scan_mz_charge_tuple[0])
            try:
                caller_result = charge_mono_caller.process(scan, scan_mz_charge_tuple[1])
                if caller_result['monoisotopic_mass'] > lower_limit:
                    if caller_result['monoisotopic_mass'] < upper_limit:
                        print('Valid scan added')
                        scans_to_search.append(scan_mz_charge_tuple[0])

            except:
                print('-' * 20)
                print('parent ion not found in scan')
                print(scan_mz_charge_tuple[0])
                print(scan_mz_charge_tuple[1])
                print(scan_mz_charge_tuple[2])
                print('#' * 20)

    
autosearch()
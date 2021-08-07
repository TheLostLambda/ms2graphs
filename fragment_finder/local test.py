from classes import Byspec_Reader as BR

br = BR.Byspec_Reader(r'C:\Users\Hyperion\Documents\GitHub\ms2_graph_tool\OT_190122_APatel_Efaecalis_EnpA_10mAU.raw.byspec2')

result = br.get_scan_by_scan_number(668)

print(br.scans_details.loc[br.scans_details.ScanNumber == 668])


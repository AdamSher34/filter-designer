from sys import exit
from os import system
from filter import FILTER_FAMILY, LowpassSallenKey as LPF_SK
from component import VALUE_SEQUENCE as SEQ

def clear_console() -> None:
    system("cls")

def get_family() -> FILTER_FAMILY:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Select the filter FAMILY:\n\n"
    printstr += "0.\tEXIT\n"
    printstr += "1.\tButterworth\n"
    printstr += "2.\tChebyshev (0.5 dB ripple)\n"
    printstr += "3.\tChebyshev (1.0 dB ripple)\n"
    printstr += "4.\tChebyshev (3.0 dB ripple)\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = int(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        if val == 1:
            return FILTER_FAMILY.BUTTERWORTH
        if val == 2:
            return FILTER_FAMILY.CHEBYSHEV_0_5dB
        if val == 3:
            return FILTER_FAMILY.CHEBYSHEV_1dB
        if val == 4:
            return FILTER_FAMILY.CHEBYSHEV_3dB

def get_order() -> int:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the filter ORDER:\n\n"
    printstr += "Valid:\t2-6\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = int(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        if val in range(2, 7):
            return val
        
def get_cutoff() -> float:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the CUTOFF FREQUENCY:\n\n"
    printstr += "Valid:\t<NUM> <UNIT>\n"
    printstr += "Num:\t>= 0\n"
    printstr += "Units:\tHz, kHz, MHz, GHz\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = input(printstr)
        valint = None
        try:
            valint = int(val)
        except:
            pass
        if valint == 0:
            exit()

        try:
            num, unit = val.split(" ")
            num = float(num)
            unit = unit.lower()
        except:
            continue

        if num < 0 or unit not in ("hz", "", "khz", "k", "mhz", "m", "ghz", "g"):
            continue
        if unit in ("hz", ""):
            return num
        elif unit in ("khz", "k"):
            return num * 10**3
        elif unit in ("mhz", "m"):
            return num * 10**6
        elif unit in ("ghz", "g"):
            return num * 10**9
    
def get_gain() -> float:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the DC GAIN in V/V:\n\n"
    printstr += "Valid:\t<NUM>\n"
    printstr += "Num:\t>= 1\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = float(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        if val >= 1:
            return val
        
def get_sequence_R() -> SEQ:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Select the RESISTOR TOLERANCE:\n\n"
    printstr += "0.\tEXIT\n"
    printstr += "1.\t40.0%  (E3)\n"
    printstr += "2.\t20.0%  (E6)\n"
    printstr += "3.\t10.0%  (E12)\n"
    printstr += "4.\t 5.0%  (E24)\n"
    printstr += "5.\t 2.0%  (E48)\n"
    printstr += "6.\t 1.0%  (E96)\n"
    printstr += "7.\t 0.5%  (E192)\n"
    printstr += "8.\t 0.0%  (EXACT)\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = int(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        sequences = {1: SEQ.E3, 2: SEQ.E6, 3: SEQ.E12, 4: SEQ.E24, 
                     5: SEQ.E48, 6: SEQ.E96, 7: SEQ.E192, 8: SEQ.EXACT}
        if val in sequences:
            return sequences[val]
        
def get_sequence_C() -> SEQ:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Select the CAPACITOR TOLERANCE:\n\n"
    printstr += "0.\tEXIT\n"
    printstr += "1.\t40.0%  (E3)\n"
    printstr += "2.\t20.0%  (E6)\n"
    printstr += "3.\t10.0%  (E12)\n"
    printstr += "4.\t 5.0%  (E24)\n"
    printstr += "5.\t 2.0%  (E48)\n"
    printstr += "6.\t 1.0%  (E96)\n"
    printstr += "7.\t 0.5%  (E192)\n"
    printstr += "8.\t 0.0%  (EXACT)\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = int(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        sequences = {1: SEQ.E3, 2: SEQ.E6, 3: SEQ.E12, 4: SEQ.E24, 
                     5: SEQ.E48, 6: SEQ.E96, 7: SEQ.E192, 8: SEQ.EXACT}
        if val in sequences:
            return sequences[val]
        
def ask_using_default_R() -> bool:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Select the DEFAULT PASSIVE:\n\n"
    printstr += "0.\tEXIT\n"
    printstr += "1.\tResistor\n"
    printstr += "2.\tCapacitor\n\n: "
    while True:
        clear_console()
        val = None
        try:
            val = int(input(printstr))
        except:
            continue
        if val == 0:
            exit()
        if val == 1:
            return True
        if val == 2:
            return False

def get_default_R() -> float:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the DEFAULT RESISTANCE:\n\n"
    printstr += "Valid:\t<NUM> <UNIT>\n"
    printstr += "Num:\t>= 1\n"
    printstr += "Units:\tR, K, M, G\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = input(printstr)
        valint = None
        try:
            valint = int(val)
        except:
            pass
        if valint == 0:
            exit()

        try:
            num, unit = val.split(" ")
            num = float(num)
            unit = unit.lower()
        except:
            continue

        if num < 0 or unit not in ("r", "", "k", "m", "g"):
            continue
        if unit in ("r", ""):
            return num
        elif unit == "k":
            return num * 10**3
        elif unit == "m":
            return num * 10**6
        elif unit == "g":
            return num * 10**9
        
def get_default_C() -> float:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the DEFAULT CAPACITANCE:\n\n"
    printstr += "Valid:\t<NUM> <UNIT>\n"
    printstr += "Num:\t>= 1\n"
    printstr += "Units:\tpF, nF, uF, mF, F\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = input(printstr)
        valint = None
        try:
            valint = int(val)
        except:
            pass
        if valint == 0:
            exit()

        try:
            num, unit = val.split(" ")
            num = float(num)
            unit = unit.lower()
        except:
            continue

        if num < 0 or unit not in ("pf", "p", "nf", "n", "uf", "u", "mf", "m", "f"):
            continue
        if unit in ("pf", "p"):
            return num
        elif unit in ("nf", "n"):
            return num * 10**3
        elif unit in ("uf", "u"):
            return num * 10**6
        elif unit in ("mf", "m"):
            return num * 10**9
        elif unit == "f":
            return num * 10**12
        
def get_default_Rfb() -> float:
    printstr =  "Low-Pass Filter Designer v1.0\n"
    printstr += "-----------------------------\n\n"
    printstr += "Enter the DEFAULT FEEDBACK RESISTANCE:\n\n"
    printstr += "Valid:\t<NUM> <UNIT>\n"
    printstr += "Num:\t>= 1\n"
    printstr += "Units:\tR, K, M, G\n"
    printstr += "Exit:\t0\n\n: "
    while True:
        clear_console()
        val = input(printstr)
        valint = None
        try:
            valint = int(val)
        except:
            pass
        if valint == 0:
            exit()

        try:
            num, unit = val.split(" ")
            num = float(num)
            unit = unit.lower()
        except:
            continue

        if num < 0 or unit not in ("r", "", "k", "m", "g"):
            continue
        if unit in ("r", ""):
            return num
        elif unit == "k":
            return num * 1000
        elif unit == "m":
            return num * 1_000_000
        elif unit == "g":
            return num * 1_000_000_000
        
def create_filter() -> LPF_SK:
    family = get_family()
    order = get_order()
    cutoff = get_cutoff()
    gain_dc = get_gain()
    sequence_R = get_sequence_R()
    sequence_C = get_sequence_C()
    default_R, default_C = None, None
    if (ask_using_default_R()):
        default_R = get_default_R()
        default_C = None
    else:
        default_R = None
        default_C = get_default_C()
    default_Rfb = get_default_Rfb()
    return LPF_SK(family, order, cutoff, gain_dc, sequence_R, sequence_C,
                  default_R, default_C, default_Rfb)

def format_value(value: float, units: tuple[str]):
    for i in range(0, len(units)-1):
        if value < 10**(3*(i+1)):
            value = round(value / 10**(3*i), 2)
            return f"{value} {units[i]}"
    value = round(value / 10**(3 * (len(units) - 1)), 2)
    return f"{value} {units[-1]}"    

def create_printstring(filter: LPF_SK) -> str:
    printstr = f"""Low-Pass Filter Designer v1.0
-----------------------------

FILTER SUMMARY:
-----------------------------
Family:\t\t{filter.family}
Order:\t\t{filter.order}
Stages:\t\t{filter.order // 2 + 1}
Cutoff Freq:\t{format_value(filter.cutoff, ("Hz", "kHz", "MHz", "GHz"))}
DC Gain:\t{filter.gain_dc:.2f} V/V
"""
    
    for stage_idx in range(filter.order // 2):
        printstr += f"""
STAGE {stage_idx+1}: Sallen-Key
-----------------------------
Natural Freq:\t{format_value(filter.natural_freqs[stage_idx], ("Hz", "kHz", "MHz", "GHz"))}
DC Gain:\t{filter.gains[stage_idx]:.2f} V/V
Q Factor:\t{1 / (3 - filter.gains[stage_idx]):.2f}
Filter R:\t{format_value(filter.R_filter[stage_idx], ("Ω", "kΩ", "MΩ", "GΩ"))}
Filter C:\t{format_value(filter.C_filter[stage_idx], ("pF", "nF", "uF", "mF", "F"))}
Feedback R1:\t{format_value(filter.R_feedback[stage_idx][0], ("Ω", "kΩ", "MΩ", "GΩ"))}
Feedback R2:\t{format_value(filter.R_feedback[stage_idx][1], ("Ω", "kΩ", "MΩ", "GΩ"))}
"""
        
    if filter.order % 2 == 0:
        printstr += f"""
STAGE {filter.order // 2 + 1}: Gain Stage
-----------------------------
DC Gain:\t{filter.gains[-1]:.2f} V/V
Feedback R1:\t{format_value(filter.R_feedback[-1][0], ("Ω", "kΩ", "MΩ", "GΩ"))}
Feedback R2:\t{format_value(filter.R_feedback[-1][1], ("Ω", "kΩ", "MΩ", "GΩ"))}\n\n"""
        
    else:
        printstr += f"""
STAGE {filter.order // 2 + 1}: Buffered RC
-----------------------------
Natural Freq:\t{format_value(filter.natural_freqs[-1], ("Hz", "kHz", "MHz", "GHz"))}
DC Gain:\t{filter.gains[-1]:.2f} V/V
Filter R:\t{format_value(filter.R_filter[-1], ("Ω", "kΩ", "MΩ", "GΩ"))}
Filter C:\t{format_value(filter.C_filter[-1], ("pF", "nF", "uF", "mF", "F"))}
Feedback R1:\t{format_value(filter.R_feedback[-1][0], ("Ω", "kΩ", "MΩ", "GΩ"))}
Feedback R2:\t{format_value(filter.R_feedback[-1][1], ("Ω", "kΩ", "MΩ", "GΩ"))}\n\n"""
    return printstr


def main():
    lpf = create_filter()
    printstr = create_printstring(lpf)
    clear_console()
    print(printstr)
    



        
if __name__ == "__main__":
    main()
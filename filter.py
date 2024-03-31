import math
from enum import Enum
import yaml
from component import VALUE_SEQUENCE as SEQ, find_match

DESIGN_TABLE = None
with open("design-table.yaml", 'r') as file:
    DESIGN_TABLE = yaml.safe_load(file)
    NAT_FREQS = DESIGN_TABLE["natural-frequency"]
    Q_FACTORS = DESIGN_TABLE["quality-factor"]

class FILTER_FAMILY(Enum):
    BUTTERWORTH = "butterworth"
    CHEBYSHEV_0_1dB = "chebyshev0.1dB"
    CHEBYSHEV_0_5dB = "chebyshev0.5dB"
    CHEBYSHEV_1dB = "chebyshev1.0dB"
    CHEBYSHEV_3dB = "chebyshev3.0dB"

class LowpassSallenKey:
    def __init__(self,
                 family: FILTER_FAMILY, 
                 order: int,
                 cutoff: float,                 # cutoff frequency fc in Hz
                 gain_dc: float,                # DC gain K in V/V
                 sequence_R: SEQ = SEQ.EXACT,
                 sequence_C: SEQ = SEQ.EXACT,
                 default_R: float = None,       # default filter resistance R in Ohms
                 default_C: float = 10_000,     # default filter capacitance C in pF
                 default_Rfb: float = 10_000,   # default feedback resistance Rfb in Ohms
                 ):
        self.family = family.value
        self.order = order
        self.cutoff = cutoff
        self.using_voltage_divider = False

        natural_freqs = [cutoff * ratio for ratio in NAT_FREQS[family.value][order]]
        gains = [3 - 1 / q for q in Q_FACTORS[family.value][order]]

        self.R_filter = []
        self.C_filter = []
        self.R_feedback = []

        for stage in range((order + 1) // 2):
            r, c = None, None
            if default_R is not None:
                r = find_match(default_R, sequence_R)
                c = find_match(10**12 / (2 * math.pi * natural_freqs[stage] * r), sequence_C)
            else:
                c = find_match(default_C, sequence_C)
                r = find_match(10**12 / (2 * math.pi * natural_freqs[stage] * c), sequence_R)
            self.R_filter.append(r)
            self.C_filter.append(c)
            natural_freqs[stage] = 10**12 / (2 * math.pi * r * c)

        for stage in range(order // 2):
            Rfb2 = find_match(default_Rfb, sequence_R)
            Rfb1 = find_match(Rfb2 * (gains[stage] - 1), sequence_R)
            self.R_feedback.append((Rfb1, Rfb2))

        gain_last_stage = gain_dc
        for Rfb1, Rfb2 in self.R_feedback:
            gain_last_stage /= Rfb1 / Rfb2 + 1
        Rfb2 = find_match(default_Rfb, sequence_R)
        Rfb1 = None
        if gain_last_stage > 1:
            Rfb1 = find_match(Rfb2 * (gain_last_stage - 1), sequence_R)
        else:
            Rfb1 = find_match(Rfb2 * (1 / gain_last_stage - 1), sequence_R)
            self.using_voltage_divider = True
        self.R_feedback.append((Rfb1, Rfb2))

        self.R_filter = tuple(self.R_filter)
        self.C_filter = tuple(self.C_filter)
        self.R_feedback = tuple(self.R_feedback)
        self.natural_freqs = tuple(natural_freqs)

        self.gains = [Rfb1 / Rfb2 + 1 for Rfb1, Rfb2 in self.R_feedback]
        if self.using_voltage_divider:
            self.gains[-1] = 1 / (self.R_feedback[-1][0] / self.R_feedback[-1][1] + 1)

        self.gain_dc = 1
        for gain in self.gains:
            self.gain_dc *= gain
        
        if family.value == "butterworth":
            self.cutoff = self.natural_freqs[0]

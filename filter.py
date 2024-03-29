import math
from enum import Enum
from component import VALUE_SEQUENCE as SEQ, find_match

class FILTER_FAMILY(Enum):
    BUTTERWORTH = "butterworth"
    CHEBYSHEV_0_5dB = "chebyshev0.5dB"
    CHEBYSHEV_1dB = "chebyshev1dB"
    CHEBYSHEV_3dB = "chebyshev3dB"

FREQUENCY_TABLE = {
    "butterworth":    {2: (1.0000,), 3: (1.0000, 1.0000), 4: (1.0000, 1.0000), 5: (1.0000, 1.0000, 1.0000), 6: (1.0000, 1.0000, 1.0000)},
    "chebyshev0.5dB": {2: (1.2313,), 3: (1.0689, 0.6265), 4: (0.5970, 1.0313), 5: (0.6905, 1.0177, 0.3623), 6: (0.3962, 0.7681, 1.0114)},
    "chebyshev1dB":   {2: (1.0500,), 3: (0.9771, 0.4942), 4: (0.5286, 0.9932), 5: (0.6552, 0.9941, 0.2895), 6: (0.3531, 0.7468, 0.9954)},
    "chebyshev3dB":   {2: (0.8414,), 3: (0.9161, 0.2986), 4: (0.4427, 0.9503), 5: (0.6140, 0.9675, 0.1775), 6: (0.2980, 0.7224, 0.9772)}
}

GAIN_TABLE = {
    "butterworth":    {2: (1.5858,), 3: (2.0000, None),   4: (1.1522, 2.2346), 5: (1.3819, 2.3820, None),   6: (1.0681, 1.5858, 2.4824)},
    "chebyshev0.5dB": {2: (1.8422,), 3: (2.4139, None),   4: (1.5818, 2.6599), 5: (2.1510, 2.7800, None),   6: (1.5372, 2.4476, 2.8465)},
    "chebyshev1dB":   {2: (1.9545,), 3: (2.5044, None),   4: (1.7254, 2.7190), 5: (2.2851, 2.8200, None),   6: (1.6857, 2.5450, 2.8751)},
    "chebyshev3dB":   {2: (2.2335,), 3: (2.6740, None),   4: (2.0711, 2.8208), 5: (2.5322, 2.8866, None),   6: (2.0425, 2.7108, 2.9218)}
}

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

        natural_freqs = [cutoff * ratio for ratio in FREQUENCY_TABLE[family.value][order]]
        gains = GAIN_TABLE[family.value][order]

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
        Rfb1 = find_match(Rfb2 * (gain_last_stage - 1), sequence_R)
        self.R_feedback.append((Rfb1, Rfb2))

        self.R_filter = tuple(self.R_filter)
        self.C_filter = tuple(self.C_filter)
        self.R_feedback = tuple(self.R_feedback)

        self.natural_freqs = tuple(natural_freqs)
        self.gains = tuple([Rfb1 / Rfb2 + 1 for Rfb1, Rfb2 in self.R_feedback])
        self.gain_dc = 1
        for gain in self.gains:
            self.gain_dc *= gain
        
        if family.value == "butterworth":
            self.cutoff = self.natural_freqs[0]

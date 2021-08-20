import numpy as np
import matplotlib.pyplot as plt

"""
This is an adapted version of rwinslow's surface script which can be found 
on https://github.com/rwinslow/surface. The adapted version was converted 
into a two-dimensional line evaluator instead of a three-dimensional surface
evaluator. Additionally, new metrics were implemented. Apart from this,
most of the code is unchanged.
"""


class Surface():

    def __init__(self, raw_data, cutoff=80, sample_width=643):
        self.cutoff = cutoff
        self.sample_width = sample_width
        self.primary = raw_data
        self.npr = len(self.primary)
        self.parse_waviness()
        self.parse_roughness()
        self.calculate_metrics()

    def __str__(self):
        return F"{self.metrics}"

    def parse_waviness(self):
        """ Parse waviness from each row of the primary profile

        Computes the FFT of the primary profile line-by-line.

        To prevent non-zero values at the boundaries, the primary profile is
        extended at the beginning and end by a flipped version of itself.

        The dataset is all real valued, so the FFT is symmetric. Thus, the
        signal strength must be doubled to fit the data correctly.

        For waviness, a low-pass filter is used (allows low frequencies/long
        wavelength signals) to allow the wavelengths longer than the cutoff
        wavelength to contribute to the final waviness profile. All values
        outside the range of allowed values are set to zero.

        """

        self.waviness = []

        for i in range(1):
            row = self.primary
            profile = []
            flipped = row[::-1]

            profile.extend(flipped)
            profile.extend(row)
            profile.extend(flipped)

            f = np.array(np.fft.fft(profile))
            f[1:-1] = f[1:-1] * 2
            self.wavelengths = []
            for j in range(1, len(self.primary)):
                wavelength = 2 * (3 * self.sample_width) / j
                self.wavelengths.extend([wavelength])
                # print(wavelength)

                if (wavelength <= self.cutoff):
                    stop_index = j
                    break

            filtered = f
            filtered[stop_index:-1] = 0

            self.waviness.append(np.real(np.fft.ifft(filtered))
                                 [self.npr:2 * self.npr].tolist())

    def parse_roughness(self):
        """ Parse roughness from  primary and waviness profiles

        Runs through each row in primary and waviness profiles and finds the
        difference between them to get the roughness

        """
        self.roughness = []
        for i in range(self.npr):
            self.roughness.append(self.primary[i] - self.waviness[0][i])

    def calculate_metrics(self):
        """ Calculate metrics for each row of waviness and roughness

        Calculates:
            Wa = Average waviness
            Ra = Average roughness

        """
        # calculate overall amplitude t
        pt = Surface.calculate_amplitude(self.primary)
        wt = Surface.calculate_amplitude(self.waviness[0])
        rt = Surface.calculate_amplitude(self.roughness)

        # calculate averages
        pa = Surface.calculate_average(self.primary)
        wa = Surface.calculate_average(self.waviness[0])
        ra = Surface.calculate_average(self.roughness)

        # calculate roughness values
        rz = Surface.calculate_rz(self.roughness)["Rz"]
        rz1max = Surface.calculate_rz(self.roughness)["Rz1max"]

        self.metrics = {
            'Pt': pt,
            'Pa': pa,
            'Wt': wt,
            'Wa': wa,
            'Rt': rt,
            'Ra': ra,
            'Rz': rz,
            'Rz1max': rz1max,
        }

    def plot(self):
        """ plot primary, waviness and roughness data
        
        """
        plt.subplot(3, 1, 1)
        plt.plot(self.primary)
        plt.title('Roughness analysis')
        plt.ylabel('Primary data')

        plt.subplot(3, 1, 2)
        plt.plot(self.waviness[0])
        plt.ylabel('waviness')

        plt.subplot(3, 1, 3)
        plt.plot(self.roughness)
        plt.xlabel('distance s')
        plt.ylabel('roughness')

        plt.show()

    @staticmethod
    def calculate_amplitude(arr):
        arr_min = min(arr)
        arr_max = max(arr)
        if (arr_min < 0 and arr_max < 0) or (arr_min > 0 and arr_max > 0):
            return max(arr) - min(arr)
        else:
            return max(arr) + np.abs(min(arr))

    @staticmethod
    def calculate_average(arr):
        res = 0
        for e in arr:
            res += np.abs(e)
        return res / len(arr)

    @staticmethod
    def calculate_rz(arr):
        segment_length = int(len(arr) / 5)
        first = 0
        last = segment_length
        res = []
        for i in range(5):
            res.append(Surface.calculate_amplitude(arr[first:last]))
            first += segment_length
            last += segment_length

        return {
            'Rz': Surface.calculate_average(res),
            'Rz1max': max(res)
        }


if __name__ == "__main__":
    pass

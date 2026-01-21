"""
LUXBIN Morse Light Language with Frequency Comb Enhancement
Combines Morse code timing with LUXBIN wavelength encoding
Enhanced with microresonator frequency comb generation for quantum communication
Creates a time-domain photonic communication protocol using nonlinear optics
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from luxbin_quantum_computer import text_to_luxbin, luxbin_to_wavelengths

# Frequency Comb Parameters (Microresonator-based)
PUMP_WAVELENGTH = 1550  # nm (typical telecom wavelength for Kerr nonlinearity)
COMB_SPACING = 0.1      # nm (frequency spacing between comb lines)
NUM_COMB_LINES = 20     # Number of comb lines generated per pulse
KERR_NONLINEARITY = 1.5 # Nonlinear coefficient for frequency doubling/comb generation

# Morse code timing (in milliseconds)
DOT_DURATION = 5      # Short pulse
DASH_DURATION = 15    # Long pulse (3x dot)
INTRA_CHAR_GAP = 5    # Gap between dots/dashes in same character
CHAR_GAP = 15         # Gap between characters
WORD_GAP = 35         # Gap between words (7x dot)

# LUXBIN to Morse mapping
# Each LUXBIN character gets a unique morse pattern
LUXBIN_TO_MORSE = {
    # Letters
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    # Numbers
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    # Punctuation
    ' ': ' ',     '.': '.-.-.-', ',': '--..--', '!': '-.-.--', '?': '..--..',
    ';': '-.-.-.', ':': '---...', '-': '-....-', '(': '-.--.', ')': '-.--.-',
    '[': '-.--.',  ']': '-.--.-', '{': '-.--.',  '}': '-.--.-', '@': '.--.-.',
    '#': '....--', '$': '...-..-', '%': '.--.--', '^': '.-...', '&': '.-...',
    '*': '-..-',   '+': '.-.-.',  '=': '-...-',  '_': '..--.-', '~': '.--..',
    '`': '.----.',  '<': '.-..-',  '>': '.-..-.', '"': '.-..-.', "'": '.----.',
    '|': '-..-.',  '\\': '.----'
}

class FrequencyCombGenerator:
    """Microresonator-based frequency comb generator using nonlinear optics"""

    def __init__(self, pump_wavelength=PUMP_WAVELENGTH, comb_spacing=COMB_SPACING,
                 num_lines=NUM_COMB_LINES, kerr_coeff=KERR_NONLINEARITY):
        self.pump_wavelength = pump_wavelength
        self.comb_spacing = comb_spacing
        self.num_lines = num_lines
        self.kerr_coeff = kerr_coeff

    def generate_comb(self, character_wavelength, morse_symbol):
        """
        Generate frequency comb using microresonator nonlinear optics
        Two photons combine to create distributed frequencies across comb
        """
        # Base frequency from character wavelength
        base_freq = 299792458 / (character_wavelength * 1e-9)  # Hz

        # Nonlinear frequency generation (parametric process)
        # Pump laser creates comb through four-wave mixing in resonator
        comb_lines = []

        for i in range(-self.num_lines//2, self.num_lines//2 + 1):
            # Frequency shift due to Kerr nonlinearity
            freq_shift = i * self.comb_spacing * 1e12  # Convert to Hz
            new_freq = base_freq + freq_shift

            # Convert back to wavelength
            wavelength = 299792458 / new_freq * 1e9  # nm

            # Intensity based on morse symbol (dots vs dashes)
            intensity = 1.0 if morse_symbol == '.' else 2.5  # Dashes are brighter

            # Phase matching condition for comb generation
            phase_match = np.exp(-abs(i) * self.kerr_coeff)

            comb_lines.append({
                'wavelength_nm': wavelength,
                'frequency_hz': new_freq,
                'intensity': intensity * phase_match,
                'comb_line': i,
                'morse_symbol': morse_symbol
            })

        return comb_lines

    def get_quantum_efficiency(self, comb_lines):
        """Calculate quantum efficiency of comb generation"""
        total_photons = sum(line['intensity'] for line in comb_lines)
        pump_photons = self.num_lines * 1.0  # Reference
        return total_photons / pump_photons if pump_photons > 0 else 0

class LuxbinMorseLight:
    """LUXBIN Morse Light Language Encoder/Decoder with Frequency Comb Enhancement"""

    def __init__(self):
        self.pulse_sequence = []
        self.time_axis = []
        self.wavelength_axis = []
        self.frequency_comb_gen = FrequencyCombGenerator()

    def encode_text_to_morse_light(self, text):
        """
        Convert text to LUXBIN Morse Light sequence using frequency comb generation
        Uses microresonator nonlinear optics to create quantum frequency combs
        Returns: List of pulse sequences with comb spectra
        """
        print(f"📝 Encoding: '{text}' with Frequency Comb Enhancement")

        # Step 1: Convert to LUXBIN
        luxbin, binary = text_to_luxbin(text)
        wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

        print(f"💎 LUXBIN: {luxbin}")
        print(f"🌈 Base wavelengths: {len(wavelengths)} photonic states")
        print(f"🔬 Microresonator: Generating {NUM_COMB_LINES} comb lines per pulse")

        # Step 2: Convert each LUXBIN character to Morse code with frequency comb
        morse_light_sequence = []

        for i, char in enumerate(luxbin):
            base_wavelength = wavelengths[i]['wavelength_nm']

            if char == ' ':
                # Space = gap with quantum wavelength (637nm) - no comb generation
                morse_light_sequence.append({
                    'wavelength_nm': 637,
                    'duration_ms': WORD_GAP,
                    'char': char,
                    'morse': 'SPACE',
                    'is_gap': True,
                    'frequency_comb': None,
                    'quantum_efficiency': 0
                })
            else:
                morse_pattern = LUXBIN_TO_MORSE.get(char, '....')  # Default to 'H' if not found

                # Convert morse pattern to frequency comb pulses
                for j, symbol in enumerate(morse_pattern):
                    if symbol in ['.', '-']:
                        # Generate frequency comb for this morse symbol
                        comb_lines = self.frequency_comb_gen.generate_comb(base_wavelength, symbol)
                        quantum_eff = self.frequency_comb_gen.get_quantum_efficiency(comb_lines)

                        duration = DOT_DURATION if symbol == '.' else DASH_DURATION

                        morse_light_sequence.append({
                            'wavelength_nm': base_wavelength,
                            'duration_ms': duration,
                            'char': char,
                            'morse': symbol,
                            'is_gap': False,
                            'frequency_comb': comb_lines,
                            'quantum_efficiency': quantum_eff,
                            'comb_center_line': base_wavelength,
                            'num_comb_lines': len(comb_lines)
                        })

                    # Add intra-character gap (except after last symbol)
                    if j < len(morse_pattern) - 1:
                        morse_light_sequence.append({
                            'wavelength_nm': 0,  # No light
                            'duration_ms': INTRA_CHAR_GAP,
                            'char': '',
                            'morse': '',
                            'is_gap': True,
                            'frequency_comb': None,
                            'quantum_efficiency': 0
                        })

                # Add gap between characters (except after last character)
                if i < len(luxbin) - 1 and luxbin[i+1] != ' ':
                    morse_light_sequence.append({
                        'wavelength_nm': 0,  # No light
                        'duration_ms': CHAR_GAP,
                        'char': '',
                        'morse': '',
                        'is_gap': True,
                        'frequency_comb': None,
                        'quantum_efficiency': 0
                    })

        self.pulse_sequence = morse_light_sequence

        # Calculate overall quantum efficiency
        total_efficiency = np.mean([p['quantum_efficiency'] for p in morse_light_sequence if p['quantum_efficiency'] > 0])
        print(f"⚛️  Average quantum efficiency: {total_efficiency:.3f}")

        return morse_light_sequence

    def visualize_morse_light(self, text):
        """Create visualization of LUXBIN Morse Light transmission with frequency combs"""

        sequence = self.encode_text_to_morse_light(text)

        # Build time and wavelength arrays
        current_time = 0
        times = []
        wavelengths = []
        colors = []
        labels = []
        comb_spectra = []  # Store comb spectra for detailed plot

        for pulse in sequence:
            duration = pulse['duration_ms']
            wavelength = pulse['wavelength_nm']

            # Add start and end points for pulse
            times.append(current_time)
            times.append(current_time + duration)

            wavelengths.append(wavelength)
            wavelengths.append(wavelength)

            # Color based on wavelength and comb information
            if wavelength == 0:
                colors.append('black')
                colors.append('black')
                label = 'GAP'
                comb_spectra.append(None)
                comb_spectra.append(None)
            elif wavelength == 637:
                colors.append('red')
                colors.append('red')
                label = f'SPACE (637nm)'
                comb_spectra.append(None)
                comb_spectra.append(None)
            else:
                hue = ((wavelength - 400) / 300) * 360
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                label = f"{pulse['char']} ({pulse['morse']}) - {wavelength:.1f}nm"
                if pulse['frequency_comb']:
                    label += f" + {len(pulse['frequency_comb'])} comb lines"
                comb_spectra.append(pulse['frequency_comb'])
                comb_spectra.append(pulse['frequency_comb'])

            labels.append(label)
            labels.append(label)

            current_time += duration

        # Create visualization with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12))

        # Top plot: Wavelength over time
        ax1.set_title(f'LUXBIN Morse Light Transmission with Frequency Combs: "{text}"', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Time (ms)', fontsize=12)
        ax1.set_ylabel('Wavelength (nm)', fontsize=12)
        ax1.set_ylim(-50, 750)
        ax1.grid(True, alpha=0.3)

        # Plot wavelength pulses
        for i in range(0, len(times), 2):
            if wavelengths[i] > 0:
                ax1.plot([times[i], times[i+1]], [wavelengths[i], wavelengths[i+1]],
                        linewidth=3, color='blue' if wavelengths[i] == 637 else 'green')
                ax1.fill_between([times[i], times[i+1]], 0, [wavelengths[i], wavelengths[i+1]],
                                alpha=0.3, color='blue' if wavelengths[i] == 637 else 'green')

        # Middle plot: Morse code pattern
        ax2.set_title('Morse Pattern (Dots and Dashes)', fontsize=14)
        ax2.set_xlabel('Time (ms)', fontsize=12)
        ax2.set_ylabel('Signal', fontsize=12)
        ax2.set_ylim(-0.5, 1.5)
        ax2.set_yticks([0, 1])
        ax2.set_yticklabels(['OFF', 'ON'])
        ax2.grid(True, alpha=0.3)

        # Plot morse pattern
        for i in range(0, len(times), 2):
            signal = 1 if wavelengths[i] > 0 else 0
            ax2.plot([times[i], times[i+1]], [signal, signal],
                    linewidth=4, color='red' if wavelengths[i] == 637 else 'blue')

        # Bottom plot: Frequency comb spectrum (showing one example comb)
        ax3.set_title('Frequency Comb Spectrum (Example)', fontsize=14)
        ax3.set_xlabel('Wavelength (nm)', fontsize=12)
        ax3.set_ylabel('Intensity (a.u.)', fontsize=12)
        ax3.grid(True, alpha=0.3)

        # Find first pulse with frequency comb and plot its spectrum
        example_comb = None
        for pulse in sequence:
            if pulse['frequency_comb']:
                example_comb = pulse['frequency_comb']
                char = pulse['char']
                morse = pulse['morse']
                break

        if example_comb:
            comb_wavelengths = [line['wavelength_nm'] for line in example_comb]
            comb_intensities = [line['intensity'] for line in example_comb]
            comb_lines = [line['comb_line'] for line in example_comb]

            ax3.bar(comb_wavelengths, comb_intensities, width=0.05, alpha=0.7, color='purple')
            ax3.set_title(f'Frequency Comb Spectrum for "{char}" ({morse}): {len(example_comb)} lines', fontsize=14)

            # Add vertical line at center wavelength
            center_wavelength = sum(comb_wavelengths) / len(comb_wavelengths)
            ax3.axvline(x=center_wavelength, color='red', linestyle='--', alpha=0.7,
                       label=f'Center: {center_wavelength:.2f}nm')
            ax3.legend()

        plt.tight_layout()
        plt.savefig('luxbin_morse_light.png', dpi=150, bbox_inches='tight')
        print(f"\n✅ Visualization saved: luxbin_morse_light.png")
        plt.show()

        return sequence

    def print_transmission_table(self):
        """Print detailed transmission table with frequency comb information"""
        print(f"\n📊 LUXBIN Morse Light Transmission Table with Frequency Combs")
        print("=" * 90)
        print(f"{'Time':>6} | {'Char':>4} | {'Morse':>5} | {'Wavelength':>10} | {'Duration':>8} | {'Comb':>4} | {'QE':>5} | Type")
        print("-" * 90)

        current_time = 0
        for pulse in self.pulse_sequence:
            char = pulse['char'] if pulse['char'] else '-'
            morse = pulse['morse'] if pulse['morse'] else '-'
            wavelength = f"{pulse['wavelength_nm']:.1f}nm" if pulse['wavelength_nm'] > 0 else "OFF"
            duration = f"{pulse['duration_ms']}ms"
            pulse_type = "GAP" if pulse['is_gap'] else "PULSE"

            # Frequency comb information
            comb_info = f"{pulse.get('num_comb_lines', 0)}" if pulse.get('frequency_comb') else "-"
            qe_info = f"{pulse.get('quantum_efficiency', 0):.2f}" if pulse.get('quantum_efficiency', 0) > 0 else "-"

            print(f"{current_time:6.0f} | {char:>4} | {morse:>5} | {wavelength:>10} | {duration:>8} | {comb_info:>4} | {qe_info:>5} | {pulse_type}")
            current_time += pulse['duration_ms']

        print("=" * 90)
        print(f"Total transmission time: {current_time:.0f}ms ({current_time/1000:.2f} seconds)")
        print(f"Microresonator: Pump @ {PUMP_WAVELENGTH}nm, {COMB_SPACING}nm spacing, Kerr coeff: {KERR_NONLINEARITY}")

def main():
    """Demo LUXBIN Morse Light Language with Frequency Comb Enhancement"""

    print("=" * 80)
    print("🌟 LUXBIN MORSE LIGHT LANGUAGE with FREQUENCY COMB ENHANCEMENT 🌟")
    print("=" * 80)
    print("\nCombines Morse code timing with LUXBIN quantum wavelengths + microresonator frequency combs!")
    print("Each character = unique wavelength + morse pattern + nonlinear frequency comb")
    print("\n🔬 Microresonator Technology:")
    print(f"   • Pump wavelength: {PUMP_WAVELENGTH}nm (telecom band)")
    print(f"   • Comb spacing: {COMB_SPACING}nm")
    print(f"   • Comb lines per pulse: {NUM_COMB_LINES}")
    print(f"   • Kerr nonlinearity coefficient: {KERR_NONLINEARITY}")
    print("\n📡 Enhanced Encoding scheme:")
    print("   • DOT (·) = 5ms pulse + frequency comb at character's wavelength")
    print("   • DASH (-) = 15ms pulse + brighter frequency comb at character's wavelength")
    print("   • SPACE = 35ms pulse at 637nm (diamond NV center) - no comb")
    print("   • Nonlinear optics: Two photons combine to create distributed frequencies")
    print("=" * 80)

    # Get input (with default for testing)
    default_text = "HELLO WORLD"
    try:
        text = input(f"\n💬 Enter message to transmit (default: '{default_text}'): ")
        if not text.strip():
            text = default_text
    except EOFError:
        # For automated testing
        text = default_text

    # Create encoder
    encoder = LuxbinMorseLight()

    # Encode and visualize
    print("\n🔄 Encoding message...")
    sequence = encoder.visualize_morse_light(text)

    # Print transmission table
    encoder.print_transmission_table()

    # Enhanced Statistics
    total_time = sum(p['duration_ms'] for p in sequence)
    num_pulses = sum(1 for p in sequence if not p['is_gap'])
    num_wavelengths = len(set(p['wavelength_nm'] for p in sequence if p['wavelength_nm'] > 0))
    total_comb_lines = sum(p.get('num_comb_lines', 0) for p in sequence if p.get('frequency_comb'))
    avg_quantum_efficiency = np.mean([p.get('quantum_efficiency', 0) for p in sequence if p.get('quantum_efficiency', 0) > 0])

    print(f"\n📈 Enhanced Transmission Statistics:")
    print(f"   • Total pulses: {num_pulses}")
    print(f"   • Unique wavelengths: {num_wavelengths}")
    print(f"   • Total frequency comb lines: {total_comb_lines}")
    print(f"   • Average quantum efficiency: {avg_quantum_efficiency:.3f}")
    print(f"   • Total time: {total_time:.0f}ms ({total_time/1000:.2f} seconds)")
    print(f"   • Data rate: {len(text) / (total_time/1000):.1f} chars/second")
    print(f"   • Spectral efficiency: {total_comb_lines / num_pulses:.1f} comb lines per pulse")
    print(f"   • Light speed transmission: INSTANT over any distance!")
    print(f"   • Nonlinear quantum enhancement: Kerr microresonator technology!")

    print(f"\n💡 Your message '{text}' is now encoded as timed light pulses")
    print(f"   with quantum frequency combs - ready for advanced photonic transmission! 🛰️✨🔬")

def test_frequency_comb():
    """Test the frequency comb functionality"""
    print("Testing Frequency Comb Generation...")

    encoder = LuxbinMorseLight()
    comb_gen = encoder.frequency_comb_gen

    # Test comb generation for a dot and dash
    test_wavelength = 650.0  # Red light
    dot_comb = comb_gen.generate_comb(test_wavelength, '.')
    dash_comb = comb_gen.generate_comb(test_wavelength, '-')

    print(f"Dot comb: {len(dot_comb)} lines, efficiency: {comb_gen.get_quantum_efficiency(dot_comb):.3f}")
    print(f"Dash comb: {len(dash_comb)} lines, efficiency: {comb_gen.get_quantum_efficiency(dash_comb):.3f}")

    # Show first few lines
    print("First 5 comb lines for dot:")
    for line in dot_comb[:5]:
        print(f"  λ={line['wavelength_nm']:.1f}nm, I={line['intensity']:.3f}, QE={line['morse_symbol']}")

    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_frequency_comb()
    else:
        main()

"""
LUXBIN Morse Light Language
Combines Morse code timing with LUXBIN wavelength encoding
Creates a time-domain photonic communication protocol
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from luxbin_quantum_computer import text_to_luxbin, luxbin_to_wavelengths

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

class LuxbinMorseLight:
    """LUXBIN Morse Light Language Encoder/Decoder"""

    def __init__(self):
        self.pulse_sequence = []
        self.time_axis = []
        self.wavelength_axis = []

    def encode_text_to_morse_light(self, text):
        """
        Convert text to LUXBIN Morse Light sequence
        Returns: List of (wavelength_nm, duration_ms, is_gap) tuples
        """
        print(f"📝 Encoding: '{text}'")

        # Step 1: Convert to LUXBIN
        luxbin, binary = text_to_luxbin(text)
        wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

        print(f"💎 LUXBIN: {luxbin}")
        print(f"🌈 Wavelengths: {len(wavelengths)} photonic states")

        # Step 2: Convert each LUXBIN character to Morse code with its wavelength
        morse_light_sequence = []

        for i, char in enumerate(luxbin):
            wavelength = wavelengths[i]['wavelength_nm']

            if char == ' ':
                # Space = gap with quantum wavelength (637nm)
                morse_light_sequence.append({
                    'wavelength_nm': 637,
                    'duration_ms': WORD_GAP,
                    'char': char,
                    'morse': 'SPACE',
                    'is_gap': True
                })
            else:
                morse_pattern = LUXBIN_TO_MORSE.get(char, '....')  # Default to 'H' if not found

                # Convert morse pattern to light pulses
                for j, symbol in enumerate(morse_pattern):
                    if symbol == '.':
                        # Dot = short pulse at character's wavelength
                        morse_light_sequence.append({
                            'wavelength_nm': wavelength,
                            'duration_ms': DOT_DURATION,
                            'char': char,
                            'morse': '.',
                            'is_gap': False
                        })
                    elif symbol == '-':
                        # Dash = long pulse at character's wavelength
                        morse_light_sequence.append({
                            'wavelength_nm': wavelength,
                            'duration_ms': DASH_DURATION,
                            'char': char,
                            'morse': '-',
                            'is_gap': False
                        })

                    # Add intra-character gap (except after last symbol)
                    if j < len(morse_pattern) - 1:
                        morse_light_sequence.append({
                            'wavelength_nm': 0,  # No light
                            'duration_ms': INTRA_CHAR_GAP,
                            'char': '',
                            'morse': '',
                            'is_gap': True
                        })

                # Add gap between characters (except after last character)
                if i < len(luxbin) - 1 and luxbin[i+1] != ' ':
                    morse_light_sequence.append({
                        'wavelength_nm': 0,  # No light
                        'duration_ms': CHAR_GAP,
                        'char': '',
                        'morse': '',
                        'is_gap': True
                    })

        self.pulse_sequence = morse_light_sequence
        return morse_light_sequence

    def visualize_morse_light(self, text):
        """Create visualization of LUXBIN Morse Light transmission"""

        sequence = self.encode_text_to_morse_light(text)

        # Build time and wavelength arrays
        current_time = 0
        times = []
        wavelengths = []
        colors = []
        labels = []

        for pulse in sequence:
            duration = pulse['duration_ms']
            wavelength = pulse['wavelength_nm']

            # Add start and end points for pulse
            times.append(current_time)
            times.append(current_time + duration)

            wavelengths.append(wavelength)
            wavelengths.append(wavelength)

            # Color based on wavelength
            if wavelength == 0:
                colors.append('black')
                colors.append('black')
                label = 'GAP'
            elif wavelength == 637:
                colors.append('red')
                colors.append('red')
                label = f'SPACE (637nm)'
            else:
                hue = ((wavelength - 400) / 300) * 360
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                colors.append(f'hsl({hue:.0f}, 70%, 60%)')
                label = f"{pulse['char']} ({pulse['morse']}) - {wavelength:.1f}nm"

            labels.append(label)
            labels.append(label)

            current_time += duration

        # Create visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

        # Top plot: Wavelength over time
        ax1.set_title(f'LUXBIN Morse Light Transmission: "{text}"', fontsize=16, fontweight='bold')
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

        # Bottom plot: Morse code pattern
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

        plt.tight_layout()
        plt.savefig('luxbin_morse_light.png', dpi=150, bbox_inches='tight')
        print(f"\n✅ Visualization saved: luxbin_morse_light.png")
        plt.show()

        return sequence

    def print_transmission_table(self):
        """Print detailed transmission table"""
        print(f"\n📊 LUXBIN Morse Light Transmission Table")
        print("=" * 80)
        print(f"{'Time':>6} | {'Char':>4} | {'Morse':>5} | {'Wavelength':>10} | {'Duration':>8} | Type")
        print("-" * 80)

        current_time = 0
        for pulse in self.pulse_sequence:
            char = pulse['char'] if pulse['char'] else '-'
            morse = pulse['morse'] if pulse['morse'] else '-'
            wavelength = f"{pulse['wavelength_nm']:.1f}nm" if pulse['wavelength_nm'] > 0 else "OFF"
            duration = f"{pulse['duration_ms']}ms"
            pulse_type = "GAP" if pulse['is_gap'] else "PULSE"

            print(f"{current_time:6.0f} | {char:>4} | {morse:>5} | {wavelength:>10} | {duration:>8} | {pulse_type}")
            current_time += pulse['duration_ms']

        print("=" * 80)
        print(f"Total transmission time: {current_time:.0f}ms ({current_time/1000:.2f} seconds)")

def main():
    """Demo LUXBIN Morse Light Language"""

    print("=" * 80)
    print("🌟 LUXBIN MORSE LIGHT LANGUAGE 🌟")
    print("=" * 80)
    print("\nCombines Morse code timing with LUXBIN quantum wavelengths!")
    print("Each character = unique wavelength + morse pattern")
    print("\n📡 Encoding scheme:")
    print("   • DOT (·) = 5ms pulse at character's wavelength")
    print("   • DASH (-) = 15ms pulse at character's wavelength")
    print("   • SPACE = 35ms pulse at 637nm (diamond NV center)")
    print("=" * 80)

    # Get input
    text = input("\n💬 Enter message to transmit: ")

    # Create encoder
    encoder = LuxbinMorseLight()

    # Encode and visualize
    print("\n🔄 Encoding message...")
    sequence = encoder.visualize_morse_light(text)

    # Print transmission table
    encoder.print_transmission_table()

    # Statistics
    total_time = sum(p['duration_ms'] for p in sequence)
    num_pulses = sum(1 for p in sequence if not p['is_gap'])
    num_wavelengths = len(set(p['wavelength_nm'] for p in sequence if p['wavelength_nm'] > 0))

    print(f"\n📈 Transmission Statistics:")
    print(f"   • Total pulses: {num_pulses}")
    print(f"   • Unique wavelengths: {num_wavelengths}")
    print(f"   • Total time: {total_time:.0f}ms ({total_time/1000:.2f} seconds)")
    print(f"   • Data rate: {len(text) / (total_time/1000):.1f} chars/second")
    print(f"   • Light speed transmission: INSTANT over any distance!")

    print(f"\n💡 Your message '{text}' is now encoded as timed light pulses")
    print(f"   at quantum wavelengths - ready for satellite transmission! 🛰️✨")

if __name__ == "__main__":
    main()

"""Convert script text to an mp3 audio file using edge-tts (free, no API key)."""

import asyncio
import edge_tts

# A few good voice options if you want to change the narrator:
#   "en-US-GuyNeural"      - male, warm/casual
#   "en-US-AriaNeural"     - female, clear/professional
#   "en-US-ChristopherNeural" - male, deep/news-anchor style
VOICE = "en-US-ChristopherNeural"


async def _generate(text: str, output_path: str, voice: str = VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_audio(text: str, output_path: str = "market_brief.mp3", voice: str = VOICE) -> str:
    asyncio.run(_generate(text, output_path, voice))
    return output_path


if __name__ == "__main__":
    generate_audio("This is a test of the market brief narrator voice.", "test.mp3")
    print("Saved test.mp3")

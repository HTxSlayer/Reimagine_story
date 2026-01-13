from pathlib import Path
import ollama
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Configuration
MODEL_NAME = "gemma2:2b"

BASE_DIR = Path(__file__).parent
PDF_PATH = BASE_DIR / "input_story1.pdf"

PROMPT_DIR = BASE_DIR / "prompts"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

DATA_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

SCHEMA_TXT_PATH = DATA_DIR / "story_schema.txt"
# SCHEMA_TXT_PATH = DATA_DIR / "story_schema_few_short.txt"

# LLM helpers
def load_prompt(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")

def call_llm(prompt: str, temperature: float = 0.7) -> str:
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={"temperature": temperature}
    )
    return response["response"].strip()

# Read PDF
print("Reading source PDF")

reader = PdfReader(str(PDF_PATH))
full_text = "\n\n".join(page.extract_text() or "" for page in reader.pages)

# Chunk text
print("Chunking text")

chunks = []
current = ""

for para in full_text.split("\n\n"):
    if len(current) + len(para) > 4000:
        chunks.append(current.strip())
        current = para
    else:
        current += "\n\n" + para

if current.strip():
    chunks.append(current.strip())

print(f"Created {len(chunks)} chunks")

# Schema Extraction 
print("Extracting narrative schema")

schema_prompt = load_prompt("schema_extraction.txt")
# schema_prompt = load_prompt("schema_extraction_few_shot.txt")

with open(SCHEMA_TXT_PATH, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks):
        prompt = schema_prompt.replace("{chunk}", chunk)
        response = call_llm(prompt, temperature=0)

        f.write(f"\n===== CHUNK {i + 1} START =====\n")
        f.write(response)
        f.write(f"\n===== CHUNK {i + 1} END =====\n")

        print(f"Processed chunk {i + 1}/{len(chunks)}")

print(f"\nSchema saved to {SCHEMA_TXT_PATH}")

# Ask for target world

target_world = input("\n Enter target world description:\n> ")

extracted_schema = SCHEMA_TXT_PATH.read_text(encoding="utf-8")

# Character Mapping
print("\nCharacter Mapping")

character_mapping = call_llm(
    load_prompt("world_mapping.txt").format(
        extracted_schema=extracted_schema,
        target_world=target_world
    ),
    temperature=0.3
)

print(character_mapping)


# Plot Transformation
print("\nPlot Transformation")

transformed_plot = call_llm(
    load_prompt("plot_transform.txt").format(
        extracted_schema=extracted_schema,
        character_mapping=character_mapping,
        target_world=target_world
    ),
    temperature=0.3
)

# Outline Creation
print("\nOutline Creation")

outline = call_llm(
    load_prompt("outline.txt").format(
        transformed_plot=transformed_plot
    ),
    temperature=0.3
)

# Story Generation
print("\n--- Story Generation ---")

story = call_llm(
    load_prompt("generation.txt").format(
        outline=outline
    ),
    temperature=0.7
)


# Title Generation
print("\nTitle Generation")

title = call_llm(
    load_prompt("title_generation.txt").format(
        story=story
    ),
    temperature=0.3
)

print("\nGENERATED TITLE")
print(title)

print("\nFINAL STORY\n")
print(story)

# Save to PDF
styles = getSampleStyleSheet()
file_path = DOCS_DIR / f"{title.replace(' ', '_')}.pdf"

doc = SimpleDocTemplate(str(file_path))
content = [
    Paragraph(title, styles["Title"]),
    Paragraph(story.replace("\n", "<br/>"), styles["BodyText"])
]

doc.build(content)

print(f"\nStory saved to: {file_path}")

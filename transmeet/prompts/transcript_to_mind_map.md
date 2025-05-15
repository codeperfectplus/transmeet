Given the following transcript, generate a hierarchical mind map in JSON format.

The map should include:
- Main topics as parent keys
- Subtopics and related points as child nodes
- Each topic/subtopic should be as specific and detailed as possible, while maintaining logical relationships.

TRANSCRIPT: {transcribed_text}

The output should be structured in JSON like:

{
    "Main Topic": {
    "Subtopic 1": ["Point 1", "Point 2"],
    "Subtopic 2": ["Point 1"]
    }
}
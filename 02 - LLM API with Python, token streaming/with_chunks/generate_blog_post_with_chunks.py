import os
from openai import OpenAI

default_model = "gpt-4o-mini"
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)


def make_request(messages, model=default_model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content.strip()


# Function to split the transcript into manageable chunks
def split_text_into_chunks(text, max_chars=10000):
    chunks = []
    while len(text) > max_chars:
        split_at = text.rfind('.', 0, max_chars)  # Split at the last full sentence
        if split_at == -1:
            split_at = max_chars  # If no period found, split at max_chars
        chunks.append(text[:split_at + 1])
        text = text[split_at + 1:]
    chunks.append(text)
    return chunks


def summarize_chunk(chunk):
    return make_request(
        [
            {"role": "system", "content": "You are an assistant that summarizes lecture transcripts."},
            {"role": "user", "content": f"Summarize the following lecture transcript chunk for a blog post:\n\n{chunk}"}
        ]
    )


def consolidate_summaries(summaries):
    consolidated_input = "\n".join(summaries)
    return make_request(
        messages=[
            {"role": "system", "content": "You are an assistant that combines summaries into a cohesive summary."},
            {"role": "user",
             "content": f"Combine the following summaries into one cohesive summary:\n\n{consolidated_input}"}
        ]
    )


# Function to generate a blog post
def generate_blog_post(summary):
    return make_request(
        messages=[
            {"role": "system", "content": "You are a skilled blog post writer."},
            {"role": "user", "content": f"Write a short blog post based on this lecture summary:\n\n{summary}"}
        ]
    )


def process_transcript(transcript):
    # Step 1: Split the transcript into chunks
    chunks = split_text_into_chunks(transcript)

    # Step 2: Summarize each chunk
    summaries = [summarize_chunk(chunk) for chunk in chunks]

    # Step 3: Consolidate the summaries
    consolidated_summary = consolidate_summaries(summaries)

    # Step 4: Generate the blog post
    blog_post = generate_blog_post(consolidated_summary)

    return blog_post


if __name__ == "__main__":
    with open("../lesson-1-transcript.txt", "r", encoding="utf-8") as file:
        transcript = file.read()

    # Generate the blog post
    blog_post = process_transcript(transcript)


    # Save the blog post to a file
    with open("../README.md", "w", encoding="utf-8") as file:
        file.write(blog_post)

    print("Blog post has been generated and saved as 'README.md'.")

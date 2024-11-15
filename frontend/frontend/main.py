# import openai
import os
import click


def get_answer(question):
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=question,
    #     max_tokens=50
    # )
    # return response.choices[0].text.strip()
    return "HI"

# Main
@click.group()
@click.version_option()
def cli():
    """The CLI tool."""

@cli.command()
def answer(question):
    """CLI bot that answers questions."""
    answer = get_answer(question)
    click.echo(f"Question: {question}")
    click.echo(f"Answer: {answer}")

if __name__ == "__main__":
    cli()

import typer
from rich import print
from src.query_engine import ask_question

app = typer.Typer(
    add_completion=False,
    help="AI Sales Insight Assistant (conversational analytics over sales data)"
)

@app.callback(invoke_without_command=True)
def main(
    q: str = typer.Argument(
        ...,
        help="Enter your question, e.g. 'profit by region this year'"
    ),
    csv_path: str = typer.Option(
        "data/Sample - Superstore.csv",
        "--csv",
        help="Path to your Superstore CSV"
    )
):
    """
    Ask a natural-language question about sales or profit.
    Examples:
      python -m src.chatbot "total sales last month in California"
      python -m src.chatbot "profit by region this year"
      python -m src.chatbot "top 3 categories by sales in 2017"
    """
    print("[grey]Thinking → Parsing your question...[/]")
    answer = ask_question(q, csv_path)
    print(f"[bold cyan]{answer}[/]")

if __name__ == "__main__":
    app()

